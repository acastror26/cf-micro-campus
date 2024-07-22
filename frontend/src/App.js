import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import HomePage from './pages/HomePage';
import RoomsPage from './pages/RoomsPage';
import ResourcesPage from './pages/ResourcesPage';
import ReservationsPage from './pages/ReservationsPage';
import UsersPage from './pages/UsersPage';
import LoginPage from './pages/LoginPage';
import RegistrationPage from './pages/RegistrationPage';
import NavBar from './components/NavBar';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userEmail, setUserEmail] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    const email = localStorage.getItem('email');

    if (token && email) {
      setIsAuthenticated(true);
      setUserEmail(email);
    }
  }, []);

  const handleLogin = (email, token) => {
    setIsAuthenticated(true);
    setUserEmail(email);
    localStorage.setItem('token', token);
    localStorage.setItem('email', email);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setUserEmail('');
    localStorage.removeItem('token');
    localStorage.removeItem('email');
  };

  return (
    <Router>
      <NavBar isAuthenticated={isAuthenticated} handleLogout={handleLogout} />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/rooms" element={isAuthenticated ? <RoomsPage /> : <Navigate to="/login" />} />
        <Route path="/resources" element={isAuthenticated ? <ResourcesPage /> : <Navigate to="/login" />} />
        <Route path="/reservations" element={isAuthenticated ? <ReservationsPage /> : <Navigate to="/login" />} />
        <Route path="/users" element={isAuthenticated ? <UsersPage /> : <Navigate to="/login" />} />
        <Route path="/login" element={<LoginPage handleLogin={handleLogin} />} />
        <Route path="/register" element={<RegistrationPage />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;