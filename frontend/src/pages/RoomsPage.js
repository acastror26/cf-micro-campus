import React, { useState, useEffect } from 'react';
import axios from 'axios';
import config from '../config';

const RoomsPage = () => {
  const [rooms, setRooms] = useState([]);

  useEffect(() => {
    axios.get(config.reservationServiceRoomsUrl)
      .then(response => {
        setRooms(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the rooms!', error);
      });
  }, []);

  return (
    <div>
      <h1>Rooms</h1>
      <ul>
        {rooms.map(room => (
          <li key={room.id}>
            <strong>{room.name}</strong><br />
            ID: {room.id}<br />
            Address: {room.address}<br />
            Open Time: {room.open_time ? room.open_time : 'N/A'}<br />
            Close Time: {room.close_time ? room.close_time : 'N/A'}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RoomsPage;
