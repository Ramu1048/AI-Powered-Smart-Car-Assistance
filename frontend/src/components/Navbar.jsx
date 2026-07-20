import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { api } from '../api';

export default function Navbar() {
  const [user, setUser] = useState(null);
  const [coords, setCoords] = useState(null);
  const [locLoading, setLocLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Check auth
    const token = localStorage.getItem('token');
    if (token) {
      api.getMe()
        .then((res) => {
          if (res.success) setUser(res.data);
        })
        .catch(() => {
          localStorage.removeItem('token');
        });
    }

    // Check location
    const lat = localStorage.getItem('lat');
    const lng = localStorage.getItem('lng');
    if (lat && lng) {
      setCoords({ lat: parseFloat(lat), lng: parseFloat(lng) });
    }
  }, []);

  const handleLogout = () => {
    api.logout();
    setUser(null);
    navigate('/');
  };

  const requestLocation = () => {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser.");
      return;
    }
    setLocLoading(true);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        localStorage.setItem('lat', latitude.toString());
        localStorage.setItem('lng', longitude.toString());
        setCoords({ lat: latitude, lng: longitude });
        setLocLoading(false);
      },
      (error) => {
        console.error("Error getting location: ", error);
        // Fallback to Bangalore Central Showroom location
        const fallbackLat = 12.9716;
        const fallbackLng = 77.5946;
        localStorage.setItem('lat', fallbackLat.toString());
        localStorage.setItem('lng', fallbackLng.toString());
        setCoords({ lat: fallbackLat, lng: fallbackLng });
        setLocLoading(false);
      }
    );
  };

  return (
    <nav style={{
      background: 'rgba(15, 23, 42, 0.75)',
      backdropFilter: 'blur(16px)',
      borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
      padding: '16px 24px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      position: 'sticky',
      top: 0,
      zIndex: 100,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '32px' }}>
        <Link to="/" style={{
          fontFamily: 'var(--font-title)',
          fontWeight: 800,
          fontSize: '22px',
          color: 'var(--glow-blue)',
          textDecoration: 'none',
          letterSpacing: '-0.03em',
        }}>
          ANTIGRAVITY <span style={{ color: 'white', fontWeight: 400 }}>SmartCar</span>
        </Link>
        <div style={{ display: 'flex', gap: '20px' }}>
          <Link to="/cars" style={{ color: 'var(--text-secondary)', textDecoration: 'none', fontSize: '14px', fontWeight: 500 }}>Explore Cars</Link>
          <Link to="/ai-assistant" style={{ color: 'var(--text-secondary)', textDecoration: 'none', fontSize: '14px', fontWeight: 500 }}>AI Chatbot</Link>
          <Link to="/recommend" style={{ color: 'var(--text-secondary)', textDecoration: 'none', fontSize: '14px', fontWeight: 500 }}>AI Recommendation</Link>
          <Link to="/showrooms" style={{ color: 'var(--text-secondary)', textDecoration: 'none', fontSize: '14px', fontWeight: 500 }}>Showrooms</Link>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        {/* Geolocation Button */}
        <button 
          onClick={requestLocation}
          className="btn-secondary"
          style={{
            padding: '8px 14px',
            fontSize: '12px',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            borderColor: coords ? 'rgba(52, 211, 153, 0.3)' : 'rgba(255,255,255,0.1)',
            color: coords ? 'var(--accent-green)' : 'var(--text-primary)',
          }}
        >
          {locLoading ? "Locating..." : coords ? `📍 ${coords.lat.toFixed(2)}, ${coords.lng.toFixed(2)}` : "📍 Set Location"}
        </button>

        {user ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
              Hi, <strong style={{ color: 'white' }}>{user.name}</strong>
            </span>
            <button onClick={handleLogout} className="btn-secondary" style={{ padding: '6px 12px', fontSize: '12px' }}>
              Logout
            </button>
          </div>
        ) : (
          <div style={{ display: 'flex', gap: '10px' }}>
            <Link to="/login" className="btn-secondary" style={{ padding: '8px 16px', fontSize: '13px' }}>Login</Link>
            <Link to="/register" className="btn-primary" style={{ padding: '8px 16px', fontSize: '13px' }}>Register</Link>
          </div>
        )}
      </div>
    </nav>
  );
}
