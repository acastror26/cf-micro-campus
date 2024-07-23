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
          <li key={reservation.id}>{reservation.status}</li>
        ))}
      </ul>
    </div>
  );
};

export default ReservationsPage;
