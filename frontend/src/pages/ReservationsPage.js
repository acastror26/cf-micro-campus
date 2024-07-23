import React, { useState, useEffect } from 'react';
import axios from 'axios';
import config from '../config';

const ReservationsPage = () => {
  const [reservations, setReservations] = useState([]);

  useEffect(() => {
    axios.get(config.reservationServiceReservationsUrl)
      .then(response => {
        setReservations(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the reservations!', error);
      });
  }, []);

  return (
    <div>
      <h1>Reservations</h1>
      <ul>
        {reservations.map(reservation => (
          <li key={reservation.id}>
            <strong>ID:</strong> {reservation.id}<br />
            <strong>Status:</strong> {reservation.status}<br />
            <strong>Start Time:</strong> {new Date(reservation.start_time).toLocaleString()}<br />
            <strong>End Time:</strong> {new Date(reservation.end_time).toLocaleString()}<br />
            <strong>Requesting User Email:</strong> {reservation.requesting_user_information_metadata.email}<br />
            <strong>Room:</strong> {reservation.room}<br />
            <strong>Approver User:</strong> {reservation.approver_user ? reservation.approver_user : 'N/A'}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ReservationsPage;
