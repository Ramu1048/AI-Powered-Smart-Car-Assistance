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
            docs = vector_store.similarity_search(query, k=k)
            return [doc.page_content for doc in docs]
        except Exception as e:
            print(f"Vector retriever lookup failed: {e}. Using SQL-based keyword fallback context.")
            db = SessionLocal()
            context = []
            try:
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

        response_text = self._mock_chat_response(message, context_chunks)
        return {
            "response": response_text,
            "sources": [c[:100] + "..." for c in context_chunks]
        }

    def voice_chat(self, message: str) -> Dict[str, Any]:
        """Generates concise, natural, voice-friendly response specifically formatted for Text-to-Speech (TTS)."""
        context_chunks = self.get_rag_context(message)
        context_str = "\n".join(context_chunks)

        system_prompt = (
            "You are Antigravity Smart Car AI Assistant. Answer the user's automotive query.\n"
            "CRITICAL: Keep the response extremely short, conversational, and voice-friendly (under 3 sentences).\n"
            "DO NOT use any markdown characters (no asterisks, bold, bullet points, hashtags, or bracketed links).\n"
            "Use natural phrases suitable for direct Text-to-Speech (TTS) reading. Example: 'The Hyundai Creta SX costs 14.5 Lakhs and offers 17.4 kmpl mileage. Would you like to compare it with the Kia Seltos?'\n\n"
            f"Context:\n{context_str}"
        )

        response_text = ""
        if self.llm:
            try:
                from langchain_core.messages import SystemMessage, HumanMessage
                response = self.llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=message)])
                response_text = response.content
            except Exception as e:
                print(f"Gemini voice response generation failed: {e}.")

        if not response_text:
            # Fallback voice generator matching key terms
            db = SessionLocal()
            try:
                msg_lower = message.lower()
                cars = db.query(Car).all()
                matched = None
                for car in cars:
                    if car.brand.lower() in msg_lower or car.model.lower() in msg_lower:
                        matched = car
                        break
                if matched:
                    price_lakh = matched.price / 100000.0
                    response_text = f"The {matched.brand} {matched.model} costs {price_lakh:.1f} Lakhs, offers {matched.mileage} kmpl mileage, and features {matched.transmission} transmission. Would you like to compare it with its alternatives?"
                else:
                    response_text = "I can assist you with comparing and choosing cars in India. Let me know which brand or budget you want to hear about!"
            finally:
                db.close()

        # Strip any accidental markdown markup
        response_text = response_text.replace("**", "").replace("*", "").replace("#", "").replace("`", "").strip()
        ssml = f"<speak>{response_text}</speak>"
        return {
            "response_text": response_text,
            "ssml": ssml
        }

    def recommend(self, preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        budget = preferences.get("budget", 2000000.0)
        family_size = preferences.get("family_size", 4)
        commute = preferences.get("commute_distance", 20.0)
        fuel = preferences.get("fuel_preference", "Petrol")
        priorities = [p.lower() for p in preferences.get("priorities", [])]

        db = SessionLocal()
        try:
            query = db.query(Car)
            query = query.filter(Car.price <= (budget * 1.15))
            cars = query.all()
            if not cars:
                cars = db.query(Car).limit(3).all()

            recommendation_candidates = []
            for car in cars:
                score = 60.0
                matches = []
                if fuel and car.fuel_type.lower() == fuel.lower():
                    score += 15
                    matches.append(f"Fuel match ({car.fuel_type})")
                safety_str = " ".join(car.safety_features or []).lower()
                if "safety" in priorities:
                    if "5-star" in safety_str or "airbags" in safety_str or (car.ncap_rating and car.ncap_rating >= 4.0):
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
                if family_size >= 5 and (car.seating_capacity and car.seating_capacity >= 6):
                    score += 10
                    matches.append("Spacious cabin suited for larger families")
                recommendation_candidates.append({
                    "car": car,
                    "score": min(score, 99.0),
                    "matches": matches
                })

            recommendation_candidates.sort(key=lambda x: x["score"], reverse=True)
            top_candidates = recommendation_candidates[:3]

            if self.llm:
                try:
                    prompt = (
                        "You are a smart car recommender. Generate explainable recommendations for a buyer with these preferences:\n"
                        f"- Budget: {budget} INR\n- Family Size: {family_size}\n- Commute: {commute} km/day\n- Fuel: {fuel}\n- Priorities: {', '.join(priorities)}\n\n"
                        "Available candidates matched from database:\n"
                    )
                    for cand in top_candidates:
                        c = cand["car"]
                        prompt += f"- ID: {c.id}, Brand: {c.brand}, Model: {c.model}, Variant: {c.variant}, Price: {c.price} INR, NCAP: {c.ncap_rating}, Tech: {c.tech_features}.\n"
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
                    cleaned_content = response.content.strip().replace("```json", "").replace("```", "")
                    return json.loads(cleaned_content)
                except Exception as e:
                    print(f"Gemini recommendation generation failed: {e}. Falling back to programmatic JSON.")

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
        db = SessionLocal()
        try:
            cars = db.query(Car).filter(Car.id.in_(car_ids)).all()
            if not cars:
                return {"comparison_summary": "No matching cars found for comparison.", "specs_table": {}}

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

            aspect_str = f"focusing on {aspect}" if aspect else "overall performance"
            comparison_summary = ""
            if self.llm:
                try:
                    prompt = f"Write a side-by-side comparison summary {aspect_str} for these cars:\n"
                    for car_name, specs in specs_table.items():
                        prompt += f"- {car_name}: Price {specs['price']}, Fuel {specs['fuel_type']}, Safety {specs['safety']}, Tech {specs['tech']}.\n"
                    prompt += "\nCompare them directly and explain which car is better for specific customer needs. Keep it under 150 words."
                    response = self.llm.invoke(prompt)
                    comparison_summary = response.content
                except Exception as e:
                    print(f"Gemini comparison summary failed: {e}. Using local fallback summary.")

            if not comparison_summary:
                car_names = list(specs_table.keys())
                comparison_summary = f"Comparing {', '.join(car_names)} {aspect_str}. "
                if len(car_names) >= 2:
                    c1, c2 = car_names[0], car_names[1]
                    p1, p2 = specs_table[c1]["price"], specs_table[c2]["price"]
                    comparison_summary += f"The {c1} is priced at {p1} INR while the {c2} is priced at {p2} INR. {' '.join(summaries)}"
                else:
                    comparison_summary += "Add more cars to generate a side-by-side evaluation summary."

            return {
                "comparison_summary": comparison_summary,
                "specs_table": specs_table
            }
        finally:
            db.close()

    def smart_compare(self, car_id: int, budget_range: Optional[List[float]] = None, required_features: Optional[List[str]] = None) -> Dict[str, Any]:
        """Automatically retrieves competitors matching budget limits and key tech/safety parameters, returning side-by-side specs."""
        db = SessionLocal()
        try:
            base_car = db.query(Car).filter(Car.id == car_id).first()
            if not base_car:
                raise ValueError("Base car not found")

            # Determine budget boundaries
            if budget_range and len(budget_range) == 2:
                min_b, max_b = budget_range[0], budget_range[1]
            else:
                # Default +/- 25% budget bracket
                min_b = base_car.price * 0.75
                max_b = base_car.price * 1.25

            # Find matching competitors
            query = db.query(Car).filter(Car.id != car_id, Car.price >= min_b, Car.price <= max_b)
            candidates = query.all()

            # Rank and filter by features if specified
            competitors = []
            for c in candidates:
                match_count = 0
                all_feats = [f.lower() for f in (c.safety_features or []) + (c.tech_features or []) + (c.adas_features or [])]
                if required_features:
                    for req in required_features:
                        if any(req.lower() in f for f in all_feats):
                            match_count += 1
                competitors.append((c, match_count))

            # Sort by feature match count and select top 3
            competitors.sort(key=lambda x: x[1], reverse=True)
            selected_cars = [base_car] + [pair[0] for pair in competitors[:3]]

            comparison_matrix = {}
            for car in selected_cars:
                dims = car.dimensions or {}
                eng = car.engine_details or {}
                comfort = car.comfort_features or {}
                
                car_label = f"{car.brand} {car.model} ({car.variant})"
                comparison_matrix[car_label] = {
                    "id": car.id,
                    "price_inr": car.price,
                    "mileage_kmpl": car.mileage,
                    "ncap_rating": car.ncap_rating,
                    "boot_space_litres": dims.get("boot_space_litres"),
                    "ground_clearance_mm": dims.get("ground_clearance_mm"),
                    "power_bhp": eng.get("max_power_bhp"),
                    "torque_nm": eng.get("max_torque_nm"),
                    "fuel_type": car.fuel_type,
                    "transmission": car.transmission,
                    "touchscreen_size": comfort.get("touchscreen_size_inches"),
                    "sunroof": comfort.get("sunroof_type"),
                    "adas": len(car.adas_features or []) > 0
                }

            # Generate natural language summary
            comparison_summary = ""
            if self.llm:
                try:
                    prompt = (
                        "Generate a highly objective, side-by-side comparison summary evaluating the value proposition of these cars. "
                        "Highlight the direct trade-offs in price, safety NCAP rating, cabin/boot space, and engine performance. Keep it under 150 words.\n\n"
                    )
                    for label, matrix in comparison_matrix.items():
                        prompt += f"- {label}: Price ₹{matrix['price_inr']/100000:.1f}L, NCAP: {matrix['ncap_rating']}, Power: {matrix['power_bhp']} bhp, Boot: {matrix['boot_space_litres']}L, Sunroof: {matrix['sunroof']}.\n"
                    response = self.llm.invoke(prompt)
                    comparison_summary = response.content
                except Exception as e:
                    print(f"Gemini smart comparison summary failed: {e}.")

            if not comparison_summary:
                comp_names = [c.model for c in selected_cars[1:]]
                comparison_summary = f"Comparing the {base_car.brand} {base_car.model} against key competitors: {', '.join(comp_names)}. "
                if comp_names:
                    comparison_summary += f"The {base_car.model} is positioned at ₹{base_car.price/100000:.1f} Lakhs. Competitors match this segment with variations in engine outputs and safety ratings."
                else:
                    comparison_summary += "No clear competitors found within the exact budget segment."

            return {
                "base_car_id": car_id,
                "comparison_summary": comparison_summary,
                "comparison_matrix": comparison_matrix
            }
        finally:
            db.close()

    def _mock_chat_response(self, message: str, context_chunks: List[str]) -> str:
        msg_lower = message.lower()
        db = SessionLocal()
        try:
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
                if sentiment:
                    response += f"\n\nComment sentiment analysis shows **{sentiment.positive_percentage}% positive** feedback."
                return response

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
