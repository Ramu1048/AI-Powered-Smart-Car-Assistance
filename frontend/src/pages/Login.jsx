import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { api } from '../api';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!email || !password) return;
    setLoading(true);
    try {
      const res = await api.login(email, password);
      if (res.success) {
        // reload navbar status by navigating to /
        window.location.href = '/';
      }
    } catch (err) {
      console.error(err);
      alert("Login failed: " + (err.response?.data?.detail || "Invalid email or password."));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fade-in" style={{ maxWidth: '400px', margin: '60px auto', padding: '0 20px' }}>
      <div className="glass-card">
        <h2 style={{ fontSize: '22px', color: 'white', marginBottom: '24px', textAlign: 'center' }}>Account Login</h2>
        
        <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
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
            <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '6px' }}>Password</label>
            <input 
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="form-input"
              required
            />
          </div>

          <button type="submit" disabled={loading} className="btn-primary" style={{ justifyContent: 'center', marginTop: '10px' }}>
            {loading ? "Authenticating..." : "Login"}
          </button>
        </form>

        <p style={{ marginTop: '20px', textAlign: 'center', fontSize: '13px', color: 'var(--text-secondary)' }}>
          Don't have an account? <Link to="/register" style={{ color: 'var(--glow-blue)', textDecoration: 'none' }}>Register</Link>
        </p>
      </div>
    </div>
  );
}
