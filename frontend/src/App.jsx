import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import LandingPage from './pages/LandingPage';
import CarCatalog from './pages/CarCatalog';
import AIAssistant from './pages/AIAssistant';
import RecommendQuiz from './pages/RecommendQuiz';
import CarCompare from './pages/CarCompare';
import CarDetail from './pages/CarDetail';
import Showrooms from './pages/Showrooms';
import Login from './pages/Login';
import Register from './pages/Register';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/cars" element={<CarCatalog />} />
            <Route path="/cars/:id" element={<CarDetail />} />
            <Route path="/ai-assistant" element={<AIAssistant />} />
            <Route path="/recommend" element={<RecommendQuiz />} />
            <Route path="/compare" element={<CarCompare />} />
            <Route path="/showrooms" element={<Showrooms />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
