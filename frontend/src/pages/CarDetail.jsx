import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../api';
import BookingModal from '../components/BookingModal';

export default function CarDetail() {
  const { id } = useParams();
  const [car, setCar] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [sentiment, setSentiment] = useState(null);
  const [activeTab, setActiveTab] = useState('performance');
  const [showBooking, setShowBooking] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCarDetails = async () => {
      setLoading(true);
      try {
        const res = await api.getCar(id);
        if (res.success) {
          setCar(res.data);
          
          // Sentiment and Youtube summary details are preloaded in details
          if (res.data.customer_sentiments && res.data.customer_sentiments[0]) {
            setSentiment(res.data.customer_sentiments[0]);
          }
        }

        // Fetch regular reviews
        const revRes = await api.getReviews(id);
        if (revRes.success) {
          setReviews(revRes.data);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchCarDetails();
  }, [id]);

  if (loading) {
    return <div style={{ color: 'var(--text-secondary)' }}>Loading car specifications...</div>;
  }

  if (!car) {
    return <div style={{ color: 'var(--text-secondary)' }}>Car details not found.</div>;
  }

  // Find corresponding YouTube summary metrics
  const ytSummary = car.youtube_review_summaries && car.youtube_review_summaries[0];

  return (
    <div className="fade-in" style={{ display: 'grid', gridTemplateColumns: '1fr 380px', gap: '30px' }}>
      
      {/* LEFT PANEL: Spec Tabs and Gallery */}
      <div>
        <div style={{ display: 'flex', gap: '20px', marginBottom: '24px', alignItems: 'baseline' }}>
          <h1 style={{ fontSize: '32px', color: 'white' }}>{car.brand} {car.model}</h1>
          <span style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>{car.variant}</span>
        </div>

        {/* Gallery */}
        <div style={{
          height: '400px',
          borderRadius: '16px',
          overflow: 'hidden',
          background: '#0f172a',
          border: '1px solid rgba(255, 255, 255, 0.08)',
          marginBottom: '32px',
        }}>
          <img 
            src={car.images && car.images[0] ? car.images[0] : 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?q=80&w=600'} 
            alt={`${car.brand} ${car.model}`}
            onError={(e) => { e.currentTarget.src = 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?q=80&w=600'; }}
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          />
        </div>

        {/* Spec Tabs */}
        <div className="tab-container">
          <button onClick={() => setActiveTab('performance')} className={activeTab === 'performance' ? "tab-btn active" : "tab-btn"}>Performance</button>
          <button onClick={() => setActiveTab('safety')} className={activeTab === 'safety' ? "tab-btn active" : "tab-btn"}>Safety</button>
          <button onClick={() => setActiveTab('technology')} className={activeTab === 'technology' ? "tab-btn active" : "tab-btn"}>Technology</button>
        </div>

        <div className="glass-card" style={{ marginBottom: '32px' }}>
          {activeTab === 'performance' && (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', fontSize: '14px' }}>
              <div>🏎️ <strong>Engine:</strong> {car.engine_specs || '1.2L Revotron'}</div>
              <div>🚗 <strong>Transmission:</strong> {car.transmission}</div>
              <div>⚡ <strong>Fuel Type:</strong> {car.fuel_type}</div>
              <div>⛽ <strong>ARAI Mileage:</strong> {car.mileage} kmpl</div>
            </div>
          )}

          {activeTab === 'safety' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <h4 style={{ color: 'white', fontSize: '15px' }}>Safety Features List</h4>
              <ul style={{ listStyleType: 'none', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {car.safety_features?.map((f, i) => (
                  <li key={i} style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)' }}>
                    🛡️ <span>{f}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {activeTab === 'technology' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <h4 style={{ color: 'white', fontSize: '15px' }}>Infotainment & Convenience</h4>
              <ul style={{ listStyleType: 'none', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {car.tech_features?.map((f, i) => (
                  <li key={i} style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)' }}>
                    ⚡ <span>{f}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Regular Customer Reviews */}
        <div className="glass-card">
          <h3 style={{ fontSize: '18px', color: 'white', marginBottom: '16px' }}>Customer Feedback</h3>
          {reviews.length === 0 ? (
            <p style={{ color: 'var(--text-secondary)', fontSize: '13px' }}>No regular customer reviews written yet.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {reviews.map(r => (
                <div key={r.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.06)', paddingBottom: '12px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '4px' }}>
                    <strong style={{ color: 'white' }}>{r.user_name}</strong>
                    <span style={{ color: 'var(--glow-blue)' }}>⭐ {r.rating} / 5</span>
                  </div>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '13px' }}>{r.comment}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* RIGHT PANEL: YouTube Summary & Book Actions */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        
        {/* Call-to-action details */}
        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Ex-Showroom Price</span>
            <div style={{ fontSize: '28px', color: 'white', fontWeight: 800, marginTop: '4px' }}>
              ₹{(car.price / 100000).toFixed(2)} Lakh
            </div>
          </div>
          
          <button onClick={() => setShowBooking(true)} className="btn-primary" style={{ width: '100%', justifyContent: 'center', padding: '14px 0' }}>
            🗓️ Schedule Test Drive
          </button>
        </div>

        {/* YouTube Video Summary Card */}
        {ytSummary && (
          <div className="glass-card" style={{ borderColor: 'rgba(56, 189, 248, 0.15)' }}>
            <h3 style={{ fontSize: '16px', color: 'white', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              🎬 Expert YouTube Reviews
            </h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '13px', lineHeight: '1.5', marginBottom: '16px' }}>
              {ytSummary.summary_text}
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '16px' }}>
              <div>
                <strong style={{ display: 'block', fontSize: '12px', color: 'var(--accent-green)', marginBottom: '4px' }}>PROS</strong>
                <ul style={{ listStyleType: 'none', display: 'flex', flexDirection: 'column', gap: '4px', fontSize: '12px' }}>
                  {ytSummary.pros?.map((p, i) => <li key={i}>✅ {p}</li>)}
                </ul>
              </div>
              <div>
                <strong style={{ display: 'block', fontSize: '12px', color: 'var(--accent-red)', marginBottom: '4px' }}>CONS</strong>
                <ul style={{ listStyleType: 'none', display: 'flex', flexDirection: 'column', gap: '4px', fontSize: '12px' }}>
                  {ytSummary.cons?.map((c, i) => <li key={i}>❌ {c}</li>)}
                </ul>
              </div>
            </div>

            <div style={{
              background: 'rgba(255, 255, 255, 0.02)',
              padding: '10px',
              borderRadius: '8px',
              fontSize: '12px',
              color: 'var(--text-secondary)',
              display: 'flex',
              flexDirection: 'column',
              gap: '6px',
            }}>
              <div>📏 <strong>Real Mileage:</strong> {ytSummary.mileage_observed}</div>
              <div>🚘 <strong>Ride Quality:</strong> {ytSummary.ride_quality}</div>
              {ytSummary.common_complaints && ytSummary.common_complaints[0] && (
                <div>⚠️ <strong>Complaints:</strong> {ytSummary.common_complaints[0]}</div>
              )}
            </div>
          </div>
        )}

        {/* Customer Sentiment Score Gauge */}
        {sentiment && (
          <div className="glass-card">
            <h3 style={{ fontSize: '15px', color: 'white', marginBottom: '10px' }}>📊 Social Sentiment Score</h3>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '6px' }}>
              <span>Positive: {sentiment.positive_percentage}%</span>
              <span>Negative: {sentiment.negative_percentage}%</span>
            </div>

            {/* Sentiment progress bar */}
            <div style={{
              width: '100%',
              height: '8px',
              borderRadius: '4px',
              background: 'rgba(255,255,255,0.06)',
              overflow: 'hidden',
              display: 'flex',
              marginBottom: '12px',
            }}>
              <div style={{ width: `${sentiment.positive_percentage}%`, background: 'var(--accent-green)' }} />
              <div style={{ width: `${sentiment.neutral_percentage}%`, background: 'var(--text-muted)' }} />
              <div style={{ width: `${sentiment.negative_percentage}%`, background: 'var(--accent-red)' }} />
            </div>

            <p style={{ color: 'var(--text-secondary)', fontSize: '12px', lineHeight: '1.4' }}>
              {sentiment.sentiment_summary}
            </p>
          </div>
        )}
      </div>

      {/* Booking Wizard Modal Portal */}
      {showBooking && (
        <BookingModal 
          car={car}
          onClose={() => setShowBooking(false)}
        />
      )}
    </div>
  );
}
