import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { api } from '../api';

export default function Register() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [phone, setPhone] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    if (!name || !email || !password || !phone) return;
    setLoading(true);
    try {
      const res = await api.register(name, email, password, phone);
      if (res.success) {
        alert("Registration successful! Please login.");
        navigate('/login');
      }
    } catch (err) {
      console.error(err);
      alert("Registration failed: " + (err.response?.data?.detail || "Make sure you use a unique email."));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fade-in" style={{ maxWidth: '400px', margin: '60px auto', padding: '0 20px' }}>
      <div className="glass-card">
        <h2 style={{ fontSize: '22px', color: 'white', marginBottom: '24px', textAlign: 'center' }}>Create Account</h2>
        
        <form onSubmit={handleRegister} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '6px' }}>Full Name</label>
            <input 
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Rohan Sharma"
              className="form-input"
              required
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '6px' }}>Email Address</label>
            <input 
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@example.com"
              className="form-input"
              required
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '6px' }}>Phone Number</label>
            <input 
              type="text"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="e.g. +919876543210"
              className="form-input"
              required
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '6px' }}>Password</label>
            <input 
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Min 6 characters"
              className="form-input"
              required
            />
          </div>

          <button type="submit" disabled={loading} className="btn-primary" style={{ justifyContent: 'center', marginTop: '10px' }}>
            {loading ? "Registering..." : "Sign Up"}
          </button>
        </form>

        <p style={{ marginTop: '20px', textAlign: 'center', fontSize: '13px', color: 'var(--text-secondary)' }}>
          Already have an account? <Link to="/login" style={{ color: 'var(--glow-blue)', textDecoration: 'none' }}>Login</Link>
        </p>
      </div>
    </div>
  );
}
