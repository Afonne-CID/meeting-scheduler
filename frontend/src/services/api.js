import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to add token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle response
api.interceptors.response.use(
  (response) => {
    // If the response was successful, there's no need to do anything
    return response;
  },
  (error) => {
    // If the server responds with a 401 Unauthorized and we've got a token, clear
    if (error.response.status === 401 && localStorage.getItem('token')) {
      throw new Error('Unauthorized');
    }
    return Promise.reject(error);
  }
);

const handleApiCall = async (apiCall) => {
  try {
    const response = await apiCall;
    return response.data;
  } catch (error) {
    if (error.response && error.response.data.error) {
      error.message = error.response.data.error;
    }
    console.error('API call failed:', error);
    throw error;
  }
};

const login = async (user) => handleApiCall(api.post('/users/login', user));
const register = async (user) => handleApiCall(api.post('/users', user));
const getUser = async () => handleApiCall(api.get('/user'));
const getMeeting = async (id) => handleApiCall(api.get(`/meetings/${id}`));
const getMeetings = async () => handleApiCall(api.get('/meetings'));
const createMeeting = async (meeting) => handleApiCall(api.post('/meetings', meeting));
const updateMeeting = async (id, updates) => handleApiCall(api.put(`/meetings/${id}`, updates));
const deleteMeeting = async (id) => handleApiCall(api.delete(`/meetings/${id}`));
const createVote = async (vote) => handleApiCall(api.post('/votes', vote));
const deleteVote = async (id) => handleApiCall(api.delete(`/votes/${id}`));
const createTimeSlot = async (timeslot) => handleApiCall(api.post('/timeslots', timeslot));
const updateTimeSlot = async (id, updates) => handleApiCall(api.put(`/timeslots/${id}`, updates));
const deleteTimeSlot = async (id) => handleApiCall(api.delete(`/timeslots/${id}`));

export {
  login,
  register,
  getUser,
  getMeeting,
  getMeetings,
  createMeeting,
  updateMeeting,
  deleteMeeting,
  createVote,
  deleteVote,
  createTimeSlot,
  updateTimeSlot,
  deleteTimeSlot,
};