import React, {useState, useEffect} from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
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
      <div>
        <NavBar 
          isAuthenticated={isAuthenticated}
          userEmail={userEmail}
          handleLogout={handleLogout}
        />
        <Routes>
          <Route path="/" component={HomePage} />
          <Route path="/rooms">
            {isAuthenticated ? (
              <RoomsPage />
            ) : (
              <Redirect to='/login' />
            )}
          </Route>
          <Route path="/resources">
            {isAuthenticated ? (
              <ResourcesPage />
            ) : (
              <Redirect to='/login' />
            )}
          </Route>
          <Route path="/reservations">
            {isAuthenticated ? (
              <ReservationsPage />
            ) : (
              <Redirect to='/login' />
            )}
          </Route>
          <Route path="/users">
            {isAuthenticated ? (
              <UsersPage />
            ) : (
              <Redirect to='/login' />
            )}
          </Route>
          <Route path="/login">
            {isAuthenticated ? (
              <Redirect to='/' />
            ) : (
              <LoginPage handleLogin={handleLogin} />
            )}
          </Route>
          <Route path="/register" >
            {isAuthenticated ? (
              <Redirect to='/' />
            ) : (
              <RegistrationPage handleLogin={handleLogin} />
            )}
          </Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
