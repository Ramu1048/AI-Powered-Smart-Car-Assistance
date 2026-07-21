import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { api } from '../api';

export default function CarCompare() {
  const [searchParams] = useSearchParams();
  const [aspect, setAspect] = useState('');
  const [comparison, setComparison] = useState(null);
  const [loading, setLoading] = useState(true);

  const carIds = searchParams.get('ids')?.split(',').map(Number) || [];

  const fetchComparison = async (currentAspect) => {
    if (carIds.length === 0) return;
    setLoading(true);
    try {
      const res = await api.compareAI(carIds, currentAspect || null);
      if (res.success) {
        setComparison(res.data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchComparison(aspect);
  }, [searchParams, aspect]);

  if (carIds.length === 0) {
    return <div style={{ color: 'var(--text-secondary)' }}>Please select cars from catalog to compare.</div>;
  }

  const specKeys = [
    { label: "Variant", key: "variant" },
    { label: "Price (INR)", key: "price", formatter: (v) => `₹${(v/100000).toFixed(2)} Lakh` },
    { label: "Mileage (kmpl)", key: "mileage" },
    { label: "Fuel Type", key: "fuel_type" },
    { label: "Transmission", key: "transmission" },
    { label: "Engine Specs", key: "engine" },
    { label: "Sentiment Index", key: "positive_sentiment_pct", formatter: (v) => `${v}% Positive` }
  ];

  const renderHighlight = (specKey, value, allSpecs) => {
    const values = Object.values(allSpecs).map(s => s[specKey]);
    
    // Highlight Price (lower is win)
    if (specKey === 'price') {
      const minVal = Math.min(...values);
      const maxVal = Math.max(...values);
      if (values.length > 1 && minVal !== maxVal) {
        if (value === minVal) return "compare-highlight-win";
        if (value === maxVal) return "compare-highlight-loss";
      }
    }
    
    // Highlight Mileage or Sentiment (higher is win)
    if (specKey === 'mileage' || specKey === 'positive_sentiment_pct') {
      const maxVal = Math.max(...values);
      const minVal = Math.min(...values);
      if (values.length > 1 && minVal !== maxVal) {
        if (value === maxVal) return "compare-highlight-win";
        if (value === minVal) return "compare-highlight-loss";
      }
    }
    
    return "";
  };

  return (
    <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 style={{ fontSize: '24px', color: 'white' }}>Side-by-Side Car Comparison</h2>
        
        {/* Aspect Filter Selector */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Focus Aspect:</span>
          <select 
            value={aspect} 
            onChange={(e) => setAspect(e.target.value)} 
            className="form-select"
            style={{ width: '160px', padding: '8px' }}
          >
            <option value="">Overall Summary</option>
            <option value="safety">Safety Focus</option>
            <option value="mileage">Mileage Focus</option>
            <option value="features">Features Focus</option>
          </select>
        </div>
      </div>

      {loading ? (
        <p style={{ color: 'var(--text-secondary)' }}>Generating side-by-side analysis...</p>
      ) : !comparison ? (
        <p style={{ color: 'var(--text-secondary)' }}>Comparison failed to load.</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          
          {/* AI Comparison Summary Card */}
          <div className="glass-card" style={{
            background: 'linear-gradient(135deg, rgba(56, 189, 248, 0.05) 0%, rgba(15, 23, 42, 0.4) 100%)',
            borderColor: 'rgba(56, 189, 248, 0.15)',
          }}>
            <h3 style={{ fontSize: '16px', color: 'var(--glow-blue)', marginBottom: '10px' }}>🤖 Smart AI Evaluation</h3>
            <p style={{ color: 'white', fontSize: '14px', lineHeight: '1.6' }}>{comparison.comparison_summary}</p>
          </div>

          {/* Specifications Matrix Table */}
          <div className="glass-card" style={{ padding: '0px', overflowX: 'auto' }}>
            <table className="comparison-matrix">
              <thead>
                <tr>
                  <th>Specification</th>
                  {Object.keys(comparison.specs_table).map(carName => (
                    <th key={carName}>{carName}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {specKeys.map(({ label, key, formatter }) => (
                  <tr key={key}>
                    <td style={{ fontWeight: 500, color: 'var(--text-secondary)' }}>{label}</td>
                    {Object.entries(comparison.specs_table).map(([carName, specs]) => {
                      const val = specs[key];
                      const displayVal = formatter ? formatter(val) : val;
                      return (
                        <td key={carName} className={renderHighlight(key, val, comparison.specs_table)}>
                          {displayVal}
                        </td>
                      );
                    })}
                  </tr>
                ))}
                {/* Lists of Safety and Tech Features */}
                <tr>
                  <td style={{ fontWeight: 500, color: 'var(--text-secondary)' }}>Safety Features</td>
                  {Object.values(comparison.specs_table).map((specs, idx) => (
                    <td key={idx} style={{ fontSize: '12px' }}>
                      <ul style={{ listStyleType: 'none', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                        {specs.safety.map((f, i) => <li key={i}>🛡️ {f}</li>)}
                      </ul>
                    </td>
                  ))}
                </tr>
                <tr>
                  <td style={{ fontWeight: 500, color: 'var(--text-secondary)' }}>Dashboard Tech</td>
                  {Object.values(comparison.specs_table).map((specs, idx) => (
                    <td key={idx} style={{ fontSize: '12px' }}>
                      <ul style={{ listStyleType: 'none', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                        {specs.tech.map((f, i) => <li key={i}>⚡ {f}</li>)}
                      </ul>
                    </td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
