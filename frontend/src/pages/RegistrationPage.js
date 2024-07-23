import React, { useState } from 'react';
import axios from 'axios';
import config from '../config';

const RegistrationPage = () => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [phone, setPhone] = useState('');
  const [country, setCountry] = useState('');
  const [city, setCity] = useState('');

  const handleRegister = () => {
    axios.post(config.userServiceUsersUrl, {
      first_name: firstName,
      last_name: lastName,
      email: email,
      password: password,
      phone_number: phone,
      country: country,
      city: city
    })
    .then(response => {
      // Handle successful registration
      // Store user data locally
      localStorage.setItem('user', JSON.stringify({
        user_service_id: response.data.id,
        first_name: firstName,
        last_name: lastName,
        email: email
      }));
      // Redirect or update the UI
    })
    .catch(error => {
      console.error('There was an error registering!', error);
    });
  };

  return (
    <div>
      <h1>Register</h1>
      <input
        type="text"
        value={firstName}
        onChange={e => setFirstName(e.target.value)}
        placeholder="First Name"
      />
      <input
        type="text"
        value={lastName}
        onChange={e => setLastName(e.target.value)}
        placeholder="Last Name"
      />
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
      <input
        type="text"
        value={phone}
        onChange={e => setPhone(e.target.value)}
        placeholder="Phone Number (optional)"
      />
      <input
        type="text"
        value={country}
        onChange={e => setCountry(e.target.value)}
        placeholder="Country (optional)"
      />
      <input
        type="text"
        value={city}
        onChange={e => setCity(e.target.value)}
        placeholder="City (optional)"
      />
      <button onClick={handleRegister}>Register</button>
    </div>
  );
};

export default RegistrationPage;
