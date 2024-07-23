import axios from 'axios';

const getAuthHeaders = (headers = {}) => {
  const token = localStorage.getItem('token');
  if (token) {
    return {
      ...headers,
      Authorization: `Bearer ${token}`
    };
  }
  return headers;
};

const getRequest = (url, headers = {}, onSuccess, onFailure) => {
  axios.get(url, { headers: getAuthHeaders(headers) })
    .then(response => {
      if (onSuccess) onSuccess(response);
    })
    .catch(error => {
      if (onFailure) onFailure(error);
    });
};

const postRequest = (url, data, headers = {}, onSuccess, onFailure) => {
  axios.post(url, data, { headers: getAuthHeaders(headers) })
    .then(response => {
      if (onSuccess) onSuccess(response);
    })
    .catch(error => {
      if (onFailure) onFailure(error);
    });
};

const putRequest = (url, data, headers = {}, onSuccess, onFailure) => {
  axios.put(url, data, { headers: getAuthHeaders(headers) })
    .then(response => {
      if (onSuccess) onSuccess(response);
    })
    .catch(error => {
      if (onFailure) onFailure(error);
    });
};

const patchRequest = (url, data, headers = {}, onSuccess, onFailure) => {
  axios.patch(url, data, { headers: getAuthHeaders(headers) })
    .then(response => {
      if (onSuccess) onSuccess(response);
    })
    .catch(error => {
      if (onFailure) onFailure(error);
    });
};

const deleteRequest = (url, headers = {}, onSuccess, onFailure) => {
  axios.delete(url, { headers: getAuthHeaders(headers) })
    .then(response => {
      if (onSuccess) onSuccess(response);
    })
    .catch(error => {
      if (onFailure) onFailure(error);
    });
};

export { getRequest, postRequest, putRequest, patchRequest, deleteRequest };