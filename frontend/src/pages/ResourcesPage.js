import React, { useState, useEffect } from 'react';
import axios from 'axios';
import config from '../config';

const ResourcesPage = () => {
  const [resources, setResources] = useState([]);

  useEffect(() => {
    axios.get(config.reservationServiceResourcesUrl)
      .then(response => {
        setResources(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the resources!', error);
      });
  }, []);

  return (
    <div>
      <h1>Resources</h1>
      <ul>
        {resources.map(resource => (
          <li key={resource.id}>
            id: {resource.id}<br />
            SKU: {resource.sku}<br />
            Name: {resource.name ? resource.name : 'N/A'}<br />
            Room: {resource.room}<br />
            Type: {resource.type}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ResourcesPage;
