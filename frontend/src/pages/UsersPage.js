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
          <li key={user.id}>{user.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default UsersPage;
