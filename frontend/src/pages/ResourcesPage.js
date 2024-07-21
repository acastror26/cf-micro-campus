import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ResourcesPage = () => {
  const [resources, setResources] = useState([]);

  useEffect(() => {
    axios.get('/api/resources/')
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
          <li key={resource.id}>{resource.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default ResourcesPage;
