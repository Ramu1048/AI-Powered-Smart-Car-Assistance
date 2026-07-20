import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { api } from '../api';
import CarCard from '../components/CarCard';

export default function CarCatalog() {
  const [searchParams] = useSearchParams();
  const [cars, setCars] = useState([]);
  const [wishlist, setWishlist] = useState([]);
  const [selectedForCompare, setSelectedForCompare] = useState([]);
  const [brandFilter, setBrandFilter] = useState('');
  const [fuelFilter, setFuelFilter] = useState('');
  const [transFilter, setTransFilter] = useState('');
  const [priceMax, setPriceMax] = useState(3000000);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // Extract query parameters from URL
    const search = searchParams.get('search') || '';
    const quickFilter = searchParams.get('filter') || '';
    
    // Set matching filters initially
    if (quickFilter === 'SUVs') setBrandFilter('');
    if (quickFilter === 'Petrol') setFuelFilter('Petrol');
    if (quickFilter === 'Automatic') setTransFilter('Automatic');
    if (quickFilter === 'Under ₹15 Lakhs') setPriceMax(1500000);

    const apiParams = {};
    if (search) apiParams.search = search;

    // Fetch cars
    api.getCars(apiParams)
      .then((res) => {
        if (res.success) setCars(res.data);
      })
      .catch(console.error)
      .finally(() => setLoading(false));

    // Load wishlist
    const token = localStorage.getItem('token');
    if (token) {
      api.getWishlist()
        .then((res) => {
          if (res.success) setWishlist(res.data.map(item => item.id));
        })
        .catch(console.error);
    }
  }, [searchParams]);

  // Filter cars locally for immediate interactivity
  const filteredCars = cars.filter(c => {
    if (brandFilter && c.brand.toLowerCase() !== brandFilter.toLowerCase()) return false;
    if (fuelFilter && c.fuel_type.toLowerCase() !== fuelFilter.toLowerCase()) return false;
    if (transFilter && c.transmission.toLowerCase() !== transFilter.toLowerCase()) return false;
    if (c.price > priceMax) return false;
    return true;
  });

  const handleCompareCheckbox = (carId) => {
    setSelectedForCompare(prev => {
      if (prev.includes(carId)) {
        return prev.filter(id => id !== carId);
      } else {
        if (prev.length >= 3) {
          alert("You can compare up to 3 cars at the same time.");
          return prev;
        }
        return [...prev, carId];
      }
    });
  };

  const handleCompareNavigate = () => {
    if (selectedForCompare.length < 1) {
      alert("Please select at least 1 car to compare.");
      return;
    }
    navigate(`/compare?ids=${selectedForCompare.join(',')}`);
  };

  return (
    <div className="fade-in" style={{ display: 'grid', gridTemplateColumns: '260px 1fr', gap: '30px' }}>
      {/* Sidebar Filter Drawer */}
      <div className="glass-card" style={{ height: 'fit-content', padding: '20px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <h3 style={{ fontSize: '18px', color: 'white', borderBottom: '1px solid rgba(255,255,255,0.06)', paddingBottom: '10px' }}>Filters</h3>
        
        <div>
          <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '8px' }}>Brand</label>
          <select value={brandFilter} onChange={(e) => setBrandFilter(e.target.value)} className="form-select">
            <option value="">All Brands</option>
            <option value="Tata">Tata</option>
            <option value="Hyundai">Hyundai</option>
            <option value="Maruti Suzuki">Maruti Suzuki</option>
            <option value="Mahindra">Mahindra</option>
            <option value="Toyota">Toyota</option>
          </select>
        </div>

        <div>
          <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '8px' }}>Fuel Type</label>
          <select value={fuelFilter} onChange={(e) => setFuelFilter(e.target.value)} className="form-select">
            <option value="">All Fuels</option>
            <option value="Petrol">Petrol</option>
            <option value="Diesel">Diesel</option>
            <option value="Hybrid">Hybrid</option>
          </select>
        </div>

        <div>
          <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '8px' }}>Transmission</label>
          <select value={transFilter} onChange={(e) => setTransFilter(e.target.value)} className="form-select">
            <option value="">All Transmissions</option>
            <option value="Manual">Manual</option>
            <option value="Automatic">Automatic</option>
          </select>
        </div>

        <div>
          <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '8px' }}>Max Price: ₹{(priceMax/100000).toFixed(1)} Lakh</label>
          <input 
            type="range"
            min={500000}
            max={3000000}
            step={50000}
            value={priceMax}
            onChange={(e) => setPriceMax(parseInt(e.target.value))}
            style={{ width: '100%', accentColor: 'var(--glow-blue)' }}
          />
        </div>
      </div>

      {/* Car Grid list */}
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
          <h2 style={{ fontSize: '22px', color: 'white' }}>Available Vehicles ({filteredCars.length})</h2>
          {selectedForCompare.length > 0 && (
            <button onClick={handleCompareNavigate} className="btn-primary">
              ⚡ Compare Selected ({selectedForCompare.length})
            </button>
          )}
        </div>

        {loading ? (
          <p style={{ color: 'var(--text-secondary)' }}>Loading catalog...</p>
        ) : filteredCars.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No cars match the selected filters.</p>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '24px' }}>
            {filteredCars.map(car => (
              <div key={car.id} style={{ position: 'relative' }}>
                <CarCard 
                  car={car} 
                  initialWishlisted={wishlist.includes(car.id)}
                />
                
                {/* Compare Checkbox */}
                <label style={{
                  position: 'absolute',
                  bottom: '68px',
                  left: '24px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  fontSize: '11px',
                  color: 'var(--text-secondary)',
                  cursor: 'pointer',
                  zIndex: 5,
                  background: 'rgba(15, 23, 42, 0.85)',
                  padding: '4px 8px',
                  borderRadius: '4px',
                }}>
                  <input 
                    type="checkbox"
                    checked={selectedForCompare.includes(car.id)}
                    onChange={() => handleCompareCheckbox(car.id)}
                    style={{ accentColor: 'var(--glow-blue)' }}
                  />
                  Compare
                </label>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
