import React, { useState, useEffect } from 'react';
import axios from 'axios';

const RoomsPage = () => {
  const [rooms, setRooms] = useState([]);

  useEffect(() => {
    axios.get('/api/rooms/')
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
          <li key={room.id}>{room.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default RoomsPage;
