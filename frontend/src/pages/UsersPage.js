import React, { useState, useEffect } from 'react';
import axios from 'axios';
import config from '../config';
import ErrorMessage from '../components/ErrorMessage';
import { getRequest } from '../utils/request_maker';

const UsersPage = () => {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    getRequest(config.reservationServiceReservationsUsersUrl, {}, response => {
      setUsers(response.data);
      setError(null);
    }, error => {
      console.error('There was an error fetching the users!', error);
      setError(error);
    });
  }, [])

  useEffect(() => {
    axios.get(config.reservationServiceReservationsUsersUrl)
      .then(response => {
        setUsers(response.data);
        setError(null);
      })
      .catch(error => {
        console.error('There was an error fetching the users!', error);
        setError(error);
      });
  }, []);

  return (
    <div>
      <h1>Users</h1>
      {error && <ErrorMessage error={error} />}
      <ul>
        {users.map(user => (
          <li key={user.id}>
            <strong>{user.first_name} {user.last_name}</strong><br />
            ID: {user.id}<br />
            Email: {user.email}<br />
            Staff: {user.is_staff ? 'Yes' : 'No'}<br />
            Admin: {user.is_admin ? 'Yes' : 'No'}<br />
            User Service ID: {user.user_service_id}<br />
            City: {user.city ? user.city : 'N/A'}<br />
            State: {user.state ? user.state : 'N/A'}<br />
            Country: {user.country ? user.country : 'N/A'}<br />
            Phone Number: {user.phone_number ? user.phone_number : 'N/A'}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UsersPage;
