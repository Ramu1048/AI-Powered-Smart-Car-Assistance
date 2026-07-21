import React, { useState } from 'react';
import { api } from '../api';

export default function RecommendQuiz() {
  const [budget, setBudget] = useState(1500000);
  const [familySize, setFamilySize] = useState(4);
  const [commuteDistance, setCommuteDistance] = useState(30);
  const [fuelPreference, setFuelPreference] = useState('Petrol');
  const [priorities, setPriorities] = useState(['Safety', 'Mileage']);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState('quiz'); // 'quiz' or 'results'

  const handlePriorityCheckbox = (p) => {
    setPriorities(prev => 
      prev.includes(p) ? prev.filter(item => item !== p) : [...prev, p]
    );
  };

  const handleRecommend = async () => {
    setLoading(true);
    try {
      const res = await api.recommendAI({
        budget,
        family_size: familySize,
        commute_distance: commuteDistance,
        fuel_preference: fuelPreference,
        priorities
      });
      if (res.success) {
        setResults(res.data);
        setStep('results');
      }
    } catch (err) {
      console.error(err);
      alert("Failed to compute recommendations. Please make sure the server is active.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fade-in" style={{ maxWidth: '720px', margin: '0 auto', padding: '20px 0' }}>
      
      {/* STEP 1: Interactive Preference Quiz */}
      {step === 'quiz' && (
        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '22px' }}>
          <div style={{ borderBottom: '1px solid rgba(255,255,255,0.06)', paddingBottom: '12px' }}>
            <h2 style={{ fontSize: '22px', color: 'white' }}>AI Smart Car Recommendation</h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: '13px', marginTop: '4px' }}>
              Fill in your driving priorities and budget to let our RAG AI evaluate options.
            </p>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '8px' }}>
              Target Budget: <strong>₹{(budget/100000).toFixed(1)} Lakh</strong>
            </label>
            <input 
              type="range"
              min={500000}
              max={3000000}
              step={50000}
              value={budget}
              onChange={(e) => setBudget(parseInt(e.target.value))}
              style={{ width: '100%', accentColor: 'var(--glow-blue)' }}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '8px' }}>Family Size / Capacity</label>
              <select value={familySize} onChange={(e) => setFamilySize(parseInt(e.target.value))} className="form-select">
                <option value={2}>2 Passengers</option>
                <option value={4}>4 Passengers</option>
                <option value={5}>5 Passengers</option>
                <option value={7}>7 Passengers</option>
              </select>
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '8px' }}>Daily Commute (km)</label>
              <input 
                type="number"
                value={commuteDistance}
                onChange={(e) => setCommuteDistance(parseInt(e.target.value) || 0)}
                className="form-input"
              />
            </div>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '8px' }}>Fuel Type Preference</label>
            <div style={{ display: 'flex', gap: '10px' }}>
              {['Petrol', 'Diesel', 'Hybrid', 'Electric'].map(fuel => (
                <button 
                  key={fuel}
                  onClick={() => setFuelPreference(fuel)}
                  className={fuelPreference === fuel ? "btn-primary" : "btn-secondary"}
                  style={{ flex: 1, fontSize: '12px', justifyContent: 'center' }}
                >
                  {fuel}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '8px' }}>Top Priorities</label>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
              {['Safety', 'Mileage', 'Performance', 'Features'].map(p => (
                <label key={p} style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  fontSize: '13px',
                  color: 'white',
                  cursor: 'pointer',
                  padding: '10px',
                  background: 'rgba(255,255,255,0.02)',
                  borderRadius: '6px',
                  border: '1px solid rgba(255,255,255,0.04)'
                }}>
                  <input 
                    type="checkbox"
                    checked={priorities.includes(p)}
                    onChange={() => handlePriorityCheckbox(p)}
                    style={{ accentColor: 'var(--glow-blue)' }}
                  />
                  {p === 'Safety' ? '🛡️' : p === 'Mileage' ? '⛽' : p === 'Performance' ? '🏎️' : '⚡'} {p}
                </label>
              ))}
            </div>
          </div>

          <button 
            onClick={handleRecommend} 
            disabled={loading}
            className="btn-primary" 
            style={{ width: '100%', justifyContent: 'center', padding: '12px 0', fontSize: '15px' }}
          >
            {loading ? "Matching specs with AI..." : "Generate AI Recommendation"}
          </button>
        </div>
      )}

      {/* STEP 2: Recommended Results List */}
      {step === 'results' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h2 style={{ fontSize: '22px', color: 'white' }}>Your AI Recommended Vehicles</h2>
            <button onClick={() => setStep('quiz')} className="btn-secondary">
              ← Restart Quiz
            </button>
          </div>

          {results.map((rec, idx) => (
            <div key={idx} className="glass-card" style={{
              background: 'linear-gradient(135deg, rgba(56, 189, 248, 0.04) 0%, rgba(15, 23, 42, 0.4) 100%)',
              border: idx === 0 ? '1px solid rgba(56, 189, 248, 0.3)' : '1px solid var(--border-card)',
            }}>
              {/* Header Match Score */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '14px' }}>
                <h3 style={{ fontSize: '20px', color: 'white' }}>
                  {idx === 0 && <span style={{ color: 'var(--glow-blue)', marginRight: '6px' }}>🏆 Best Match:</span>}
                  {rec.brand} {rec.model} ({rec.variant})
                </h3>
                <span style={{ fontSize: '13px', fontWeight: 'bold', color: 'var(--accent-green)', background: 'rgba(52, 211, 153, 0.1)', padding: '4px 10px', borderRadius: '12px' }}>
                  {rec.match_score.toFixed(0)}% Match
                </span>
              </div>

              {/* Match Explanation */}
              <p style={{ color: 'var(--text-secondary)', fontSize: '14px', lineHeight: '1.6', marginBottom: '16px' }}>
                {rec.explanation}
              </p>

              {/* Pros & Cons lists */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', background: 'rgba(255,255,255,0.01)', padding: '16px', borderRadius: '8px', marginBottom: '16px' }}>
                <div>
                  <strong style={{ fontSize: '12px', color: 'var(--accent-green)', display: 'block', marginBottom: '6px' }}>Pros</strong>
                  <ul style={{ listStyleType: 'none', display: 'flex', flexDirection: 'column', gap: '4px', fontSize: '12px' }}>
                    {rec.pros?.map((p, i) => <li key={i}>✅ {p}</li>)}
                  </ul>
                </div>
                <div>
                  <strong style={{ fontSize: '12px', color: 'var(--accent-red)', display: 'block', marginBottom: '6px' }}>Cons</strong>
                  <ul style={{ listStyleType: 'none', display: 'flex', flexDirection: 'column', gap: '4px', fontSize: '12px' }}>
                    {rec.cons?.map((c, i) => <li key={i}>❌ {c}</li>)}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
