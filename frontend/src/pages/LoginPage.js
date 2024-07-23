import React, { useState } from 'react';
import axios from 'axios';
import config from '../config';
import { useNavigate } from 'react-router-dom';

const LoginPage = ({ handleLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const callLogin = () => {
    axios.post(config.generateTokenUrl, { email, password })
      .then(response => {
        // Store the token in local storage or state
        handleLogin(response.data.email, response.data.access_token);
        console.info('Response', response.data.access_token);
        console.info('Logged in successfully! Redirecting...');
        // Redirect or update the UI
        navigate('/');
      })
      .catch(error => {
        console.error('There was an error logging in!', error);
      });
  };

  return (
    <div>
      <h1>Login</h1>
      <input
        type="email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button onClick={callLogin}>Login</button>
    </div>
  );
};

export default LoginPage;
