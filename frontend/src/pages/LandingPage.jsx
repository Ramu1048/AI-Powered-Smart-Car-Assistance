import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { api } from '../api';
import CarCard from '../components/CarCard';

export default function LandingPage() {
  const [search, setSearch] = useState('');
  const [cars, setCars] = useState([]);
  const [wishlist, setWishlist] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // Load cars
    api.getCars()
      .then((res) => {
        if (res.success) setCars(res.data);
      })
      .catch(console.error)
      .finally(() => setLoading(false));

    // Load wishlist if logged in
    const token = localStorage.getItem('token');
    if (token) {
      api.getWishlist()
        .then((res) => {
          if (res.success) setWishlist(res.data.map(item => item.id));
        })
        .catch(console.error);
    }
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (search.trim()) {
      navigate(`/cars?search=${encodeURIComponent(search)}`);
    }
  };

  const handleQuickFilter = (tag) => {
    navigate(`/cars?filter=${encodeURIComponent(tag)}`);
  };

  return (
    <div className="fade-in">
      {/* Hero Section */}
      <div style={{
        textAlign: 'center',
        padding: '80px 20px',
        background: 'radial-gradient(ellipse at center, rgba(56, 189, 248, 0.08) 0%, transparent 60%)',
        marginBottom: '40px',
      }}>
        <h1 style={{
          fontSize: '48px',
          fontWeight: 800,
          background: 'linear-gradient(to right, #ffffff, #94a3b8)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          marginBottom: '16px',
        }}>
          Find the Perfect Car with AI
        </h1>
        <p style={{
          color: 'var(--text-secondary)',
          fontSize: '18px',
          maxWidth: '600px',
          margin: '0 auto 32px auto',
          lineHeight: '1.6',
        }}>
          Search specs, compare variants, explore nearby showrooms, and talk to our AI Assistant to secure personalized recommendations.
        </p>

        {/* Search Bar */}
        <form onSubmit={handleSearch} style={{
          maxWidth: '560px',
          margin: '0 auto 24px auto',
          display: 'flex',
          gap: '10px',
          background: 'rgba(30, 41, 59, 0.45)',
          padding: '8px',
          borderRadius: '12px',
          border: '1px solid rgba(255, 255, 255, 0.08)',
        }}>
          <input 
            type="text" 
            placeholder="Search by brand or model (e.g. Nexon, Creta)..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{
              flex: 1,
              background: 'none',
              border: 'none',
              outline: 'none',
              padding: '8px 12px',
              color: 'white',
              fontFamily: 'var(--font-body)',
              fontSize: '15px',
            }}
          />
          <button type="submit" className="btn-primary" style={{ padding: '8px 20px' }}>
            Search
          </button>
        </form>

        {/* Quick Filter Pills */}
        <div style={{ display: 'flex', justifyContent: 'center', gap: '10px', flexWrap: 'wrap' }}>
          {['SUVs', 'High Mileage', 'Petrol', 'Automatic', 'Under ₹15 Lakhs'].map(tag => (
            <button 
              key={tag}
              onClick={() => handleQuickFilter(tag)}
              className="btn-secondary"
              style={{ padding: '6px 14px', borderRadius: '20px', fontSize: '12px' }}
            >
              {tag}
            </button>
          ))}
        </div>
      </div>

      {/* Featured Cars Section */}
      <div style={{ padding: '0 20px 60px 20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '24px' }}>
          <h2 style={{ fontSize: '24px', color: 'white' }}>Trending Models</h2>
          <Link to="/cars" style={{ color: 'var(--glow-blue)', fontSize: '13px', textDecoration: 'none', fontWeight: 600 }}>
            View All Explore →
          </Link>
        </div>

        {loading ? (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '24px' }}>
            {[1, 2, 3].map(i => (
              <div key={i} className="glass-card" style={{ height: '340px', opacity: 0.3 }}>
                Loading skeleton...
              </div>
            ))}
          </div>
        ) : (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
            gap: '24px',
          }}>
            {cars.slice(0, 3).map(car => (
              <CarCard 
                key={car.id} 
                car={car} 
                initialWishlisted={wishlist.includes(car.id)} 
              />
            ))}
          </div>
        )}
      </div>

      {/* AI Assistant Banner */}
      <div className="glass-card" style={{
        background: 'linear-gradient(135deg, rgba(3, 105, 161, 0.2) 0%, rgba(15, 23, 42, 0.4) 100%)',
        border: '1px solid rgba(56, 189, 248, 0.2)',
        padding: '40px',
        textAlign: 'center',
        margin: '0 20px 80px 20px',
        borderRadius: '20px',
      }}>
        <h2 style={{ fontSize: '28px', color: 'white', marginBottom: '12px' }}>Stuck on choosing?</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '15px', maxWidth: '500px', margin: '0 auto 24px auto', lineHeight: '1.6' }}>
          Take our quick recommendation quiz or chat with our RAG AI Assistant to find matches tailored specifically to your family size, budget, and driving habits.
        </p>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '16px' }}>
          <Link to="/recommend" className="btn-primary" style={{ padding: '12px 28px' }}>
            🎯 Start Preference Quiz
          </Link>
          <Link to="/ai-assistant" className="btn-secondary" style={{ padding: '12px 28px' }}>
            💬 Chat with Assistant
          </Link>
        </div>
      </div>
    </div>
  );
}
