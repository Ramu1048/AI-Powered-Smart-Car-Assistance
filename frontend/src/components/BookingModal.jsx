import React, { useState, useEffect } from 'react';
import { api } from '../api';

export default function BookingModal({ car, onClose }) {
  const [step, setStep] = useState(1);
  const [showrooms, setShowrooms] = useState([]);
  const [selectedShowroom, setSelectedShowroom] = useState(null);
  const [bookingType, setBookingType] = useState('test_drive'); // or 'purchase'
  const [date, setDate] = useState('');
  const [timeSlot, setTimeSlot] = useState('10:30 AM');
  const [contactName, setContactName] = useState('');
  const [contactPhone, setContactPhone] = useState('');
  const [loadingShowrooms, setLoadingShowrooms] = useState(false);
  const [bookingLoading, setBookingLoading] = useState(false);
  const [bookingResult, setBookingResult] = useState(null);

  useEffect(() => {
    // Get default user credentials
    const token = localStorage.getItem('token');
    if (token) {
      api.getMe().then((res) => {
        if (res.success) {
          setContactName(res.data.name);
          setContactPhone(res.data.phone || '');
        }
      }).catch(console.error);
    }

    // Get showrooms list
    setLoadingShowrooms(true);
    api.getNearbyShowrooms(12.9716, 77.5946, 100)
      .then((res) => {
        if (res.success) {
          setShowrooms(res.data);
          if (res.data[0]) setSelectedShowroom(res.data[0]);
        }
      })
      .catch(console.error)
      .finally(() => setLoadingShowrooms(false));
  }, []);

  const handleBooking = async () => {
    if (!date) {
      alert("Please select a date.");
      return;
    }
    setBookingLoading(true);
    try {
      const scheduledDate = `${date}T${timeSlot === '10:30 AM' ? '10:30:00' : timeSlot === '02:00 PM' ? '14:00:00' : '16:30:00'}`;
      const res = await api.createBooking(
        car.id,
        selectedShowroom ? selectedShowroom.id : 1,
        bookingType,
        scheduledDate
      );
      if (res.success) {
        setBookingResult(res.data);
        setStep(5); // Show confirmation
      }
    } catch (err) {
      console.error(err);
      alert("Booking failed: " + (err.response?.data?.detail || "Make sure you are logged in."));
    } finally {
      setBookingLoading(false);
    }
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0, left: 0, right: 0, bottom: 0,
      background: 'rgba(2, 6, 23, 0.85)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 1000,
      padding: '20px',
    }}>
      <div className="glass-card" style={{
        maxWidth: '500px',
        width: '100%',
        background: 'var(--bg-secondary)',
        borderRadius: '20px',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        padding: '32px',
        position: 'relative',
      }}>
        {/* Close Button */}
        <button 
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            background: 'none',
            border: 'none',
            color: 'var(--text-secondary)',
            fontSize: '20px',
            cursor: 'pointer',
          }}
        >
          ✕
        </button>

        {/* Step Indicator Header */}
        {step < 5 && (
          <div style={{ display: 'flex', gap: '8px', marginBottom: '24px' }}>
            {[1, 2, 3, 4].map(s => (
              <div key={s} style={{
                flex: 1,
                height: '4px',
                borderRadius: '2px',
                background: s <= step ? 'var(--glow-blue)' : 'rgba(255,255,255,0.1)',
                transition: 'background 0.3s ease',
              }} />
            ))}
          </div>
        )}

        {/* STEP 1: Select Booking Type & Variant */}
        {step === 1 && (
          <div>
            <h2 style={{ fontSize: '20px', color: 'white', marginBottom: '10px' }}>Book Showroom Visit</h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: '13px', marginBottom: '20px' }}>{car.brand} {car.model} ({car.variant})</p>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', marginBottom: '24px' }}>
              <label style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Select Booking Type</label>
              <div style={{ display: 'flex', gap: '12px' }}>
                <button 
                  onClick={() => setBookingType('test_drive')}
                  className={bookingType === 'test_drive' ? "btn-primary" : "btn-secondary"}
                  style={{ flex: 1, justifyContent: 'center' }}
                >
                  🚗 Test Drive
                </button>
                <button 
                  onClick={() => setBookingType('purchase')}
                  className={bookingType === 'purchase' ? "btn-primary" : "btn-secondary"}
                  style={{ flex: 1, justifyContent: 'center' }}
                >
                  💳 Showroom Purchase
                </button>
              </div>
            </div>

            <button onClick={() => setStep(2)} className="btn-primary" style={{ width: '100%', justifyContent: 'center' }}>
              Continue
            </button>
          </div>
        )}

        {/* STEP 2: Select Showroom */}
        {step === 2 && (
          <div>
            <h2 style={{ fontSize: '20px', color: 'white', marginBottom: '16px' }}>Select Nearby Showroom</h2>
            {loadingShowrooms ? (
              <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>Loading showrooms...</p>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxHeight: '200px', overflowY: 'auto', marginBottom: '24px' }}>
                {showrooms.map(s => (
                  <div 
                    key={s.id}
                    onClick={() => setSelectedShowroom(s)}
                    style={{
                      padding: '12px',
                      borderRadius: '8px',
                      border: '1px solid',
                      borderColor: selectedShowroom?.id === s.id ? 'var(--glow-blue)' : 'rgba(255,255,255,0.06)',
                      background: selectedShowroom?.id === s.id ? 'rgba(56, 189, 248, 0.05)' : 'rgba(255,255,255,0.02)',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease',
                    }}
                  >
                    <div style={{ color: 'white', fontSize: '14px', fontWeight: 600 }}>{s.name}</div>
                    <div style={{ color: 'var(--text-secondary)', fontSize: '11px', marginTop: '4px' }}>📍 {s.address}</div>
                  </div>
                ))}
              </div>
            )}
            
            <div style={{ display: 'flex', gap: '10px' }}>
              <button onClick={() => setStep(1)} className="btn-secondary" style={{ flex: 1 }}>Back</button>
              <button onClick={() => setStep(3)} className="btn-primary" style={{ flex: 1, justifyContent: 'center' }}>Next</button>
            </div>
          </div>
        )}

        {/* STEP 3: Choose Date & Time */}
        {step === 3 && (
          <div>
            <h2 style={{ fontSize: '20px', color: 'white', marginBottom: '16px' }}>Pick Date & Time</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', marginBottom: '24px' }}>
              <div>
                <label style={{ fontSize: '12px', color: 'var(--text-secondary)', display: 'block', marginBottom: '6px' }}>Select Date</label>
                <input 
                  type="date"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  className="form-input"
                  min={new Date().toISOString().split('T')[0]}
                />
              </div>
              <div>
                <label style={{ fontSize: '12px', color: 'var(--text-secondary)', display: 'block', marginBottom: '6px' }}>Select Time Slot</label>
                <div style={{ display: 'flex', gap: '10px' }}>
                  {['10:30 AM', '02:00 PM', '04:30 PM'].map(slot => (
                    <button 
                      key={slot}
                      onClick={() => setTimeSlot(slot)}
                      className={timeSlot === slot ? "btn-primary" : "btn-secondary"}
                      style={{ flex: 1, fontSize: '12px', padding: '8px 4px', justifyContent: 'center' }}
                    >
                      {slot}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '10px' }}>
              <button onClick={() => setStep(2)} className="btn-secondary" style={{ flex: 1 }}>Back</button>
              <button onClick={() => setStep(4)} className="btn-primary" style={{ flex: 1, justifyContent: 'center' }}>Next</button>
            </div>
          </div>
        )}

        {/* STEP 4: Confirm Contact Details & Book */}
        {step === 4 && (
          <div>
            <h2 style={{ fontSize: '20px', color: 'white', marginBottom: '16px' }}>Contact Information</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', marginBottom: '24px' }}>
              <div>
                <label style={{ fontSize: '12px', color: 'var(--text-secondary)', display: 'block', marginBottom: '6px' }}>Full Name</label>
                <input 
                  type="text"
                  value={contactName}
                  onChange={(e) => setContactName(e.target.value)}
                  placeholder="Enter name"
                  className="form-input"
                />
              </div>
              <div>
                <label style={{ fontSize: '12px', color: 'var(--text-secondary)', display: 'block', marginBottom: '6px' }}>Phone Number</label>
                <input 
                  type="text"
                  value={contactPhone}
                  onChange={(e) => setContactPhone(e.target.value)}
                  placeholder="Enter contact phone"
                  className="form-input"
                />
              </div>
            </div>

            <div style={{ display: 'flex', gap: '10px' }}>
              <button onClick={() => setStep(3)} className="btn-secondary" style={{ flex: 1 }}>Back</button>
              <button 
                onClick={handleBooking} 
                disabled={bookingLoading}
                className="btn-primary" 
                style={{ flex: 1, justifyContent: 'center' }}
              >
                {bookingLoading ? "Booking..." : "Confirm Booking"}
              </button>
            </div>
          </div>
        )}

        {/* STEP 5: Success Confirmation Screen */}
        {step === 5 && (
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '48px', marginBottom: '16px' }}>🎉</div>
            <h2 style={{ fontSize: '22px', color: 'white', marginBottom: '10px' }}>Booking Confirmed!</h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '20px' }}>
              Your {bookingType === 'test_drive' ? 'test drive' : 'purchase appointment'} for the <strong>{car.brand} {car.model}</strong> has been successfully scheduled.
            </p>

            <div style={{
              background: 'rgba(255, 255, 255, 0.02)',
              border: '1px dashed rgba(255, 255, 255, 0.1)',
              padding: '16px',
              borderRadius: '10px',
              textAlign: 'left',
              fontSize: '13px',
              color: 'var(--text-secondary)',
              display: 'flex',
              flexDirection: 'column',
              gap: '8px',
              marginBottom: '24px',
            }}>
              <div>📍 <strong>Showroom:</strong> {selectedShowroom?.name}</div>
              <div>📅 <strong>Date:</strong> {date}</div>
              <div>⏰ <strong>Time:</strong> {timeSlot}</div>
              {bookingResult && (
                <div>🎟️ <strong>Booking Reference:</strong> #{bookingResult.id}</div>
              )}
            </div>

            <button onClick={onClose} className="btn-primary" style={{ width: '100%', justifyContent: 'center' }}>
              Done
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
