import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api';

export default function CarCard({ car, initialWishlisted, onWishlistToggle }) {
  const [wishlisted, setWishlisted] = useState(initialWishlisted);
  const [loading, setLoading] = useState(false);

  const handleWishlist = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    const token = localStorage.getItem('token');
    if (!token) {
      alert("Please login first to bookmark cars!");
      return;
    }
    setLoading(true);
    try {
      const res = await api.toggleWishlist(car.id);
      if (res.success) {
        setWishlisted(!wishlisted);
        if (onWishlistToggle) onWishlistToggle(car.id, !wishlisted);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const formattedPrice = (car.price / 100000).toFixed(2);

  return (
    <div className="glass-card fade-in" style={{
      position: 'relative',
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      justifyContent: 'space-between',
      gap: '16px',
    }}>
      {/* Wishlist button */}
      <button 
        onClick={handleWishlist}
        disabled={loading}
        style={{
          position: 'absolute',
          top: '16px',
          right: '16px',
          background: 'rgba(15, 23, 42, 0.65)',
          border: '1px solid rgba(255,255,255,0.08)',
          width: '36px',
          height: '36px',
          borderRadius: '50%',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          cursor: 'pointer',
          color: wishlisted ? 'var(--accent-red)' : 'var(--text-secondary)',
          fontSize: '18px',
          transition: 'all 0.2s ease',
          zIndex: 5,
        }}
      >
        {wishlisted ? '❤️' : '🤍'}
      </button>

      <div>
        {/* Car Image */}
        <div style={{
          height: '180px',
          borderRadius: '12px',
          overflow: 'hidden',
          background: '#1e293b',
          marginBottom: '16px',
        }}>
          <img 
            src={car.images && car.images[0] ? car.images[0] : 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?q=80&w=600'} 
            alt={`${car.brand} ${car.model}`}
            onError={(e) => { e.currentTarget.src = 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?q=80&w=600'; }}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              transition: 'transform 0.5s ease',
            }}
            onMouseOver={(e) => e.currentTarget.style.transform = 'scale(1.06)'}
            onMouseOut={(e) => e.currentTarget.style.transform = 'scale(1)'}
          />
        </div>

        {/* Title */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '6px' }}>
          <h3 style={{ fontSize: '18px', color: 'white' }}>{car.brand} {car.model}</h3>
          <span style={{ fontSize: '13px', color: 'var(--glow-blue)', fontWeight: 'bold' }}>₹{formattedPrice} Lakh</span>
        </div>
        <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '12px' }}>{car.variant}</div>

        {/* Specs summary */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '8px 16px',
          fontSize: '12px',
          color: 'var(--text-secondary)',
          background: 'rgba(255, 255, 255, 0.02)',
          padding: '10px',
          borderRadius: '8px',
          marginBottom: '14px',
        }}>
          <div>⛽ {car.fuel_type}</div>
          <div>⚙️ {car.transmission}</div>
          <div>📏 {car.engine_specs || '1.2L Engine'}</div>
          <div>🚗 {car.mileage} kmpl</div>
        </div>

        {/* Priorities highlights */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '14px' }}>
          {car.safety_features && car.safety_features[0] && (
            <span style={{ fontSize: '10px', background: 'rgba(52, 211, 153, 0.1)', color: 'var(--accent-green)', padding: '2px 8px', borderRadius: '4px' }}>
              🛡️ {car.safety_features[0]}
            </span>
          )}
          {car.tech_features && car.tech_features[0] && (
            <span style={{ fontSize: '10px', background: 'rgba(56, 189, 248, 0.1)', color: 'var(--glow-blue)', padding: '2px 8px', borderRadius: '4px' }}>
              ⚡ {car.tech_features[0]}
            </span>
          )}
        </div>
      </div>

      <div style={{ display: 'flex', gap: '8px', width: '100%' }}>
        <Link to={`/cars/${car.id}`} className="btn-secondary" style={{ flex: 1, textAlign: 'center', padding: '8px 0', fontSize: '12px' }}>
          Specs
        </Link>
        <Link to="/ai-assistant" className="btn-primary" style={{ flex: 1, justifyContent: 'center', padding: '8px 0', fontSize: '12px' }}>
          Talk to AI
        </Link>
      </div>
    </div>
  );
}
