import React, { useState, useRef, useEffect } from 'react';
import { api } from '../api';

export default function AIAssistant() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I am your Antigravity Smart Car AI Assistant. Ask me anything about car configurations, specifications, YouTube review summaries, user sentiments, or showroom availabilities in India!'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const suggestionChips = [
    "Recommend a petrol SUV under 15 lakhs",
    "Compare Nexon vs Creta",
    "What do YouTube reviews say about Tata Nexon?",
    "Showrooms in Bangalore Indiranagar"
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (messageText) => {
    if (!messageText.trim()) return;
    
    // Add user message
    const userMsg = { role: 'user', content: messageText };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      // Compile history
      const history = messages.map(m => ({
        role: m.role,
        content: m.content
      }));

      const res = await api.chatAI(messageText, history);
      if (res.success) {
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: res.data.response,
          sources: res.data.sources
        }]);
      }
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'I apologize, but I encountered an error connecting to the AI core. Please check that the server is active.'
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fade-in" style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '20px', maxWidth: '900px', margin: '0 auto', padding: '20px 0' }}>
      <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '16px', padding: '24px' }}>
        <div style={{ borderBottom: '1px solid rgba(255,255,255,0.06)', paddingBottom: '16px' }}>
          <h2 style={{ fontSize: '20px', color: 'white' }}>Smart Car Conversational RAG AI</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '12px', marginTop: '4px' }}>
            Powered by LangChain & Google Gemini. Restrained to automotive domains.
          </p>
        </div>

        {/* Messages list */}
        <div style={{ height: '420px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '14px', paddingRight: '6px' }}>
          {messages.map((m, idx) => (
            <div 
              key={idx} 
              className={m.role === 'user' ? 'message-bubble message-user' : 'message-bubble message-assistant'}
            >
              {/* Parse text markdown bold/italic tags briefly */}
              <div style={{ whiteSpace: 'pre-wrap', fontSize: '14px' }}>
                {m.content}
              </div>

              {/* Renders Sources citations if available */}
              {m.sources && m.sources.length > 0 && (
                <div style={{
                  marginTop: '10px',
                  paddingTop: '8px',
                  borderTop: '1px solid rgba(255,255,255,0.06)',
                  fontSize: '11px',
                  color: 'var(--text-muted)',
                }}>
                  <strong>Sources:</strong> {m.sources.map((s, i) => <span key={i} style={{ display: 'block', fontStyle: 'italic', marginTop: '2px' }}>- {s}</span>)}
                </div>
              )}
            </div>
          ))}
          {loading && (
            <div className="message-bubble message-assistant" style={{ fontStyle: 'italic', color: 'var(--text-muted)' }}>
              Assistant is thinking...
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Suggestion Chips */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '14px' }}>
          {suggestionChips.map((chip, idx) => (
            <button 
              key={idx}
              onClick={() => handleSend(chip)}
              className="chip"
              disabled={loading}
            >
              {chip}
            </button>
          ))}
        </div>

        {/* Input Bar */}
        <form 
          onSubmit={(e) => {
            e.preventDefault();
            handleSend(input);
          }}
          style={{ display: 'flex', gap: '10px' }}
        >
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your query (e.g. which car has the best safety features?)..."
            className="form-input"
            disabled={loading}
          />
          <button type="submit" className="btn-primary" disabled={loading} style={{ padding: '0 24px' }}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
