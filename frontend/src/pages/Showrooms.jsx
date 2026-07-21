import React, { useState, useEffect } from 'react';
import { api } from '../api';
import BookingModal from '../components/BookingModal';

export default function Showrooms() {
  const [showrooms, setShowrooms] = useState([]);
  const [selectedShowroom, setSelectedShowroom] = useState(null);
  const [inventory, setInventory] = useState([]);
  const [inventoryLoading, setInventoryLoading] = useState(false);
  const [loading, setLoading] = useState(true);
  const [showBooking, setShowBooking] = useState(false);
  const [bookingCar, setBookingCar] = useState(null);

  useEffect(() => {
    // Read coordinates from localStorage
    const lat = parseFloat(localStorage.getItem('lat')) || 12.9716;
    const lng = parseFloat(localStorage.getItem('lng')) || 77.5946;

    api.getNearbyShowrooms(lat, lng, 100)
      .then((res) => {
        if (res.success) {
          setShowrooms(res.data);
          if (res.data[0]) setSelectedShowroom(res.data[0]);
        }
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!selectedShowroom) return;
    
    setInventoryLoading(true);
    api.getShowroomInventory(selectedShowroom.id)
      .then((res) => {
        if (res.success) setInventory(res.data);
      })
      .catch(console.error)
      .finally(() => setInventoryLoading(false));
  }, [selectedShowroom]);

  const handleBookCar = (carItem) => {
    setBookingCar(carItem);
    setShowBooking(true);
  };

  return (
    <div className="fade-in" style={{ display: 'grid', gridTemplateColumns: '1fr 400px', gap: '30px' }}>
      
      {/* LEFT PANEL: Interactive Showroom details & Mock Map */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        <h2 style={{ fontSize: '24px', color: 'white' }}>Nearby Showrooms</h2>
        
        {/* Mock Map Frame */}
        <div style={{
          height: '350px',
          borderRadius: '16px',
          overflow: 'hidden',
          background: '#0f172a',
          border: '1px solid rgba(255, 255, 255, 0.08)',
          position: 'relative',
        }}>
          {/* Embedded Leaflet map rendering openstreet map or detailed SVG */}
          <iframe 
            title="Showroom Location Map"
            src={`https://maps.google.com/maps?q=${selectedShowroom ? selectedShowroom.latitude : 12.9716},${selectedShowroom ? selectedShowroom.longitude : 77.5946}&z=14&output=embed`}
            style={{
              width: '100%',
              height: '100%',
              border: 0,
              filter: 'invert(90%) hue-rotate(180deg)', // Premium Dark theme map override!
            }}
          />
          <div style={{
            position: 'absolute',
            bottom: '16px',
            left: '16px',
            background: 'rgba(15, 23, 42, 0.95)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            padding: '10px 14px',
            borderRadius: '8px',
            fontSize: '11px',
            color: 'var(--text-secondary)',
          }}>
            📍 Map showing location for: <strong>{selectedShowroom?.name}</strong>
          </div>
        </div>

        {/* Showrooms Listing list */}
        {loading ? (
          <p style={{ color: 'var(--text-secondary)' }}>Loading showrooms...</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {showrooms.map(s => (
              <div 
                key={s.id}
                onClick={() => setSelectedShowroom(s)}
                className="glass-card"
                style={{
                  cursor: 'pointer',
                  borderColor: selectedShowroom?.id === s.id ? 'var(--glow-blue)' : 'rgba(255,255,255,0.06)',
                  background: selectedShowroom?.id === s.id ? 'rgba(56, 189, 248, 0.04)' : 'var(--bg-card)',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                  <h3 style={{ fontSize: '16px', color: 'white' }}>{s.name}</h3>
                  <span style={{ fontSize: '11px', color: 'var(--glow-blue)', background: 'rgba(56, 189, 248, 0.1)', padding: '2px 8px', borderRadius: '10px' }}>
                    Active
                  </span>
                </div>
                <p style={{ color: 'var(--text-secondary)', fontSize: '13px', marginTop: '6px' }}>📍 {s.address}</p>
                <p style={{ color: 'var(--text-muted)', fontSize: '12px', marginTop: '6px' }}>📞 {s.contact_number}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* RIGHT PANEL: Live Car Inventory stock */}
      <div className="glass-card" style={{ height: 'fit-content' }}>
        <h3 style={{ fontSize: '18px', color: 'white', marginBottom: '16px', borderBottom: '1px solid rgba(255,255,255,0.06)', paddingBottom: '12px' }}>
          Live Stock Inventory
        </h3>
        
        {inventoryLoading ? (
          <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>Loading stock details...</p>
        ) : inventory.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)', fontSize: '13px' }}>No models currently available at this location.</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {inventory.map(item => (
              <div key={item.id} style={{
                background: 'rgba(255, 255, 255, 0.02)',
                padding: '12px',
                borderRadius: '8px',
                border: '1px solid rgba(255,255,255,0.05)',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
              }}>
                <div>
                  <div style={{ color: 'white', fontSize: '14px', fontWeight: 600 }}>{item.brand} {item.model}</div>
                  <div style={{ color: 'var(--text-secondary)', fontSize: '11px', marginTop: '2px' }}>{item.variant}</div>
                  <div style={{ marginTop: '6px' }}>
                    <span className="status-badge status-instock">In Stock</span>
                  </div>
                </div>
                <button onClick={() => handleBookCar(item)} className="btn-primary" style={{ padding: '6px 12px', fontSize: '11px' }}>
                  Book
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {showBooking && bookingCar && (
        <BookingModal 
          car={bookingCar}
          onClose={() => setShowBooking(false)}
        />
      )}
    </div>
  );
}
