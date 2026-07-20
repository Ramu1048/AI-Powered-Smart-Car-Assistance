import os
import json
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.database.postgres import SessionLocal
from app.models.sql_models import Car, YoutubeReviewSummary, CustomerSentiment
from app.database.vector_store import get_vector_store

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class AIService:
    def __init__(self):
        self.llm = None
        if GEMINI_API_KEY:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                self.llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    google_api_key=GEMINI_API_KEY,
                    temperature=0.2
                )
                print("Gemini LLM initialized successfully.")
            except Exception as e:
                print(f"Failed to initialize Gemini LLM: {e}. Falling back to local NLP engine.")
                self.llm = None

    def get_rag_context(self, query: str, k: int = 3) -> List[str]:
        """Queries the vector store to fetch relevant automotive context chunks."""
        try:
            vector_store = get_vector_store("car_specifications")
            # Query vector store
            docs = vector_store.similarity_search(query, k=k)
            return [doc.page_content for doc in docs]
        except Exception as e:
            print(f"Vector retriever lookup failed: {e}. Using SQL-based keyword fallback context.")
            # SQL fallback context
            db = SessionLocal()
            context = []
            try:
                # Basic brand keyword matching
                cars = db.query(Car).all()
                for car in cars:
                    if car.brand.lower() in query.lower() or car.model.lower() in query.lower():
                        context.append(
                            f"Car details: {car.brand} {car.model} {car.variant}. Price: {car.price} INR. "
                            f"Fuel: {car.fuel_type}. Transmission: {car.transmission}. Specs: {car.engine_specs}. "
                            f"Safety: {', '.join(car.safety_features or [])}. Features: {', '.join(car.tech_features or [])}."
                        )
                        summary = db.query(YoutubeReviewSummary).filter(YoutubeReviewSummary.car_id == car.id).first()
                        if summary:
                            context.append(f"Expert YouTube reviews: {summary.summary_text} Pros: {', '.join(summary.pros or [])}. Cons: {', '.join(summary.cons or [])}.")
            finally:
                db.close()
            return context[:k]

    def chat(self, message: str, history: List[Dict[str, str]]) -> Dict[str, Any]:
        """Handles multi-turn conversational RAG assistance."""
        context_chunks = self.get_rag_context(message)
        context_str = "\n".join(context_chunks)

        system_prompt = (
            "You are Antigravity Smart Car AI Assistant, a professional automotive consultant in India.\n"
            "Your sole focus is to help users select, compare, and learn about cars available in Indian showrooms.\n"
            "You must ONLY answer queries related to cars, showrooms, specs, mileage, and customer sentiments.\n"
            "For any non-automotive query, politely decline to answer, redirecting back to smart car assistance.\n\n"
            "Context retrieved from specification database and YouTube expert reviews:\n"
            f"{context_str}\n\n"
            "Using the context above and the conversation history, provide a helpful, natural, and concise response. "
            "Cite details from specifications or YouTube reviews when appropriate."
        )

        if self.llm:
            try:
                from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
                messages = [SystemMessage(content=system_prompt)]
                
                # Append last 6 turns of history to prevent token bloat
                for turn in history[-6:]:
                    if turn["role"] == "user":
                        messages.append(HumanMessage(content=turn["content"]))
                    else:
                        messages.append(AIMessage(content=turn["content"]))
                        
                messages.append(HumanMessage(content=message))
                response = self.llm.invoke(messages)
                return {
                    "response": response.content,
                    "sources": [c[:100] + "..." for c in context_chunks]
                }
            except Exception as e:
                print(f"Gemini chat request failed: {e}. Using local NLP fallback.")

        # Local NLP Conversational Fallback
        response_text = self._mock_chat_response(message, context_chunks)
        return {
            "response": response_text,
            "sources": [c[:100] + "..." for c in context_chunks]
        }

    def recommend(self, preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handles structured preference matching using SQL specs + LLM reasoning."""
        budget = preferences.get("budget", 2000000.0)
        family_size = preferences.get("family_size", 4)
        commute = preferences.get("commute_distance", 20.0)
        fuel = preferences.get("fuel_preference", "Petrol")
        priorities = [p.lower() for p in preferences.get("priorities", [])]

        db = SessionLocal()
        try:
            # Hybrid Query: Fetch all cars within budget + same fuel (if specified)
            query = db.query(Car)
            # Fetch cars within budget (or up to 15% above budget stretch)
            query = query.filter(Car.price <= (budget * 1.15))
            cars = query.all()
            
            if not cars:
                # Fallback to general list if no matches
                cars = db.query(Car).limit(3).all()

            recommendation_candidates = []
            for car in cars:
                score = 60.0 # base score
                matches = []
                
                # Check fuel preference
                if fuel and car.fuel_type.lower() == fuel.lower():
                    score += 15
                    matches.append(f"Fuel match ({car.fuel_type})")
                    
                # Check priorities
                safety_str = " ".join(car.safety_features or []).lower()
                tech_str = " ".join(car.tech_features or []).lower()
                
                if "safety" in priorities:
                    if "5-star" in safety_str or "airbags" in safety_str:
                        score += 10
                        matches.append("Excellent safety ratings")
                if "mileage" in priorities:
                    if car.mileage and car.mileage >= 17.0:
                        score += 10
                        matches.append("High fuel economy")
                if "features" in priorities or "technology" in priorities:
                    if len(car.tech_features or []) >= 3:
                        score += 10
                        matches.append("Feature-rich dashboard package")
                        
                # Check family size
                if family_size >= 5 and car.brand.lower() in ["mahindra", "toyota"] or car.model.lower() in ["creta", "xuv700", "hycross"]:
                    score += 10
                    matches.append("Spacious cabin suited for larger families")
                else:
                    score += 5
                    
                recommendation_candidates.append({
                    "car": car,
                    "score": min(score, 99.0),
                    "matches": matches
                })
                
            # Sort by match score
            recommendation_candidates.sort(key=lambda x: x["score"], reverse=True)
            top_candidates = recommendation_candidates[:3]

            # If Gemini is available, let it write personalized explainable text
            if self.llm:
                try:
                    prompt = (
                        "You are a smart car recommender. Generate explainable recommendations for a buyer with these preferences:\n"
                        f"- Budget: {budget} INR\n- Family Size: {family_size}\n- Commute: {commute} km/day\n- Fuel: {fuel}\n- Priorities: {', '.join(priorities)}\n\n"
                        "Available candidates matched from database:\n"
                    )
                    for cand in top_candidates:
                        c = cand["car"]
                        prompt += f"- ID: {c.id}, Brand: {c.brand}, Model: {c.model}, Variant: {c.variant}, Price: {c.price} INR, Pros: {c.safety_features}, Tech: {c.tech_features}.\n"
                        
                    prompt += (
                        "\nOutput a valid JSON array of recommendations matching EXACTLY this structure:\n"
                        "[\n"
                        "  {\n"
                        "    \"car_id\": 1,\n"
                        "    \"brand\": \"Tata\",\n"
                        "    \"model\": \"Nexon\",\n"
                        "    \"variant\": \"Creative Plus\",\n"
                        "    \"match_score\": 95.0,\n"
                        "    \"explanation\": \"Provide a personalized explanation citing their commute and priorities.\",\n"
                        "    \"pros\": [\"Pro 1\", \"Pro 2\"],\n"
                        "    \"cons\": [\"Con 1\"]\n"
                        "  }\n"
                        "]"
                    )
                    
                    response = self.llm.invoke(prompt)
                    # Parse JSON content
                    cleaned_content = response.content.strip().replace("```json", "").replace("```", "")
                    return json.loads(cleaned_content)
                except Exception as e:
                    print(f"Gemini recommendation generation failed: {e}. Falling back to programmatic JSON.")

            # Programmatic Fallback JSON
            result = []
            for cand in top_candidates:
                c = cand["car"]
                yt = db.query(YoutubeReviewSummary).filter(YoutubeReviewSummary.car_id == c.id).first()
                pros = yt.pros[:2] if yt and yt.pros else (c.safety_features[:2] if c.safety_features else ["Reliable package"])
                cons = yt.cons[:1] if yt and yt.cons else ["Base styling can feel plain"]
                
                explanation = f"The {c.brand} {c.model} is a perfect match ({cand['score']}%). "
                if cand["matches"]:
                    explanation += "It stands out due to: " + ", ".join(cand["matches"]) + "."
                else:
                    explanation += f"It matches your budget of {c.price} INR and provides good utility."
                    
                result.append({
                    "car_id": c.id,
                    "brand": c.brand,
                    "model": c.model,
                    "variant": c.variant,
                    "match_score": cand["score"],
                    "explanation": explanation,
                    "pros": pros,
                    "cons": cons
                })
            return result
        finally:
            db.close()

    def compare(self, car_ids: List[int], aspect: Optional[str] = None) -> Dict[str, Any]:
        """Provides dynamic side-by-side evaluations using PostgreSQL specs and vectors."""
        db = SessionLocal()
        try:
            cars = db.query(Car).filter(Car.id.in_(car_ids)).all()
            if not cars:
                return {"comparison_summary": "No matching cars found for comparison.", "specs_table": {}}

            # Compile side-by-side spec table
            specs_table = {}
            summaries = []
            
            for car in cars:
                yt = db.query(YoutubeReviewSummary).filter(YoutubeReviewSummary.car_id == car.id).first()
                sentiment = db.query(CustomerSentiment).filter(CustomerSentiment.car_id == car.id).first()
                
                car_key = f"{car.brand} {car.model}"
                specs_table[car_key] = {
                    "variant": car.variant,
                    "price": car.price,
                    "mileage": car.mileage,
                    "fuel_type": car.fuel_type,
                    "transmission": car.transmission,
                    "engine": car.engine_specs,
                    "safety": car.safety_features or [],
                    "tech": car.tech_features or [],
                    "positive_sentiment_pct": sentiment.positive_percentage if sentiment else 50.0
                }
                
                summary_chunk = f"**{car_key}** has pros like {', '.join(yt.pros[:2] if yt else ['reliable drive'])}, and complaints about {', '.join(yt.common_complaints[:1] if yt else ['cabin noise'])}."
                summaries.append(summary_chunk)

            # Generate natural language summary
            aspect_str = f"focusing on {aspect}" if aspect else "overall performance"
            comparison_summary = ""
            
            if self.llm:
                try:
                    prompt = (
                        f"Write a side-by-side comparison summary {aspect_str} for these cars:\n"
                    )
                    for car_name, specs in specs_table.items():
                        prompt += f"- {car_name}: Price {specs['price']}, Fuel {specs['fuel_type']}, Safety {specs['safety']}, Tech {specs['tech']}.\n"
                    prompt += "\nCompare them directly and explain which car is better for specific customer needs. Keep it under 150 words."
                    
                    response = self.llm.invoke(prompt)
                    comparison_summary = response.content
                except Exception as e:
                    print(f"Gemini comparison summary failed: {e}. Using local fallback summary.")

            if not comparison_summary:
                # Fallback generator
                car_names = list(specs_table.keys())
                comparison_summary = f"Comparing {', '.join(car_names)} {aspect_str}. "
                if len(car_names) >= 2:
                    c1, c2 = car_names[0], car_names[1]
                    p1, p2 = specs_table[c1]["price"], specs_table[c2]["price"]
                    comparison_summary += (
                        f"The {c1} is priced at {p1} INR while the {c2} is priced at {p2} INR. "
                        f"For drivers seeking feature abundance and brand values, both offer strong packages. "
                        f"{' '.join(summaries)}"
                    )
                else:
                    comparison_summary += "Add more cars to generate a side-by-side evaluation summary."

            return {
                "comparison_summary": comparison_summary,
                "specs_table": specs_table
            }
        finally:
            db.close()

    def _mock_chat_response(self, message: str, context_chunks: List[str]) -> str:
        """Simulates conversational NLP matching key tokens."""
        msg_lower = message.lower()
        db = SessionLocal()
        try:
            # 1. Search for matches in database
            cars = db.query(Car).all()
            matched_car = None
            for car in cars:
                if car.brand.lower() in msg_lower or car.model.lower() in msg_lower:
                    matched_car = car
                    break
            
            if matched_car:
                car_name = f"{matched_car.brand} {matched_car.model}"
                yt = db.query(YoutubeReviewSummary).filter(YoutubeReviewSummary.car_id == matched_car.id).first()
                sentiment = db.query(CustomerSentiment).filter(CustomerSentiment.car_id == matched_car.id).first()
                
                response = f"Sure! The **{car_name}** ({matched_car.variant}) is priced at approximately **₹{matched_car.price/100000:.2f} Lakhs**. "
                response += f"It has a **{matched_car.fuel_type}** engine with **{matched_car.transmission}** transmission. "
                
                if matched_car.mileage:
                    response += f"It delivers an estimated mileage of **{matched_car.mileage} kmpl**. "
                    
                if matched_car.safety_features:
                    response += f"Key safety specs include: *{', '.join(matched_car.safety_features[:3])}*. "
                    
                if yt:
                    response += f"\n\nAccording to YouTube expert review summaries: {yt.summary_text} "
                    response += f"\n* **Pros**: {', '.join(yt.pros or [])}"
                    response += f"\n* **Cons**: {', '.join(yt.cons or [])}"
                    if yt.mileage_observed:
                        response += f"\n* **Real-world Mileage**: {yt.mileage_observed}"
                        
                if sentiment:
                    response += f"\n\nComment sentiment analysis shows **{sentiment.positive_percentage}% positive** feedback."
                return response

            # 2. General greeting or query fallback
            if "hello" in msg_lower or "hi" in msg_lower:
                return (
                    "Hello! I am Antigravity Smart Car AI Assistant. I can help you select the best car, "
                    "compare specifications side-by-side, check showroom locations, or summarize YouTube user reviews. "
                    "What car or budget range are you looking for?"
                )
            elif "budget" in msg_lower or "under" in msg_lower or "lakh" in msg_lower:
                return (
                    "To find the best car in your budget, you can use our personalized recommendation system. "
                    "Simply provide your budget target, preferred fuel type, and passenger capacity requirements!"
                )
            
            # Default RAG context response
            if context_chunks:
                return (
                    "Based on my car database: " + context_chunks[0][:300] + "... "
                    "Please let me know if you would like detailed comparisons, reviews, or showroom availabilities for this model!"
                )
                
            return (
                "I'm here to assist with car selections, showroom bookings, specifications, and review analysis in India. "
                "Could you specify what brand, model, or budget range you are interested in?"
            )
        finally:
            db.close()
