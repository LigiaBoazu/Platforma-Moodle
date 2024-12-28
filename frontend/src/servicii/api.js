import axios from 'axios';

const API_URL = 'http://localhost:8000'; 

export const login = async (credentials) => {
  try {
    const response = await axios.post(`${API_URL}/api/academia/login`, credentials);
    return response.data.access_token; 
  } catch (error) {
    console.error('Login failed:', error);
    throw error; 
  }
};

export const fetchProfessors = async (token, filters = {}) => {
  try {
    const response = await axios.get(`${API_URL}/api/academia/professors`, {
      headers: {
        Authorization: `Bearer ${token}`, 
      },
      params: filters, 
    });
    return response.data; 
  } catch (error) {
    console.error('Error fetching professors:', error);
    throw error;
  }
};

export const fetchStudents = async (token, filters = {}) => {
  try {
    const response = await axios.get(`${API_URL}/api/academia/students`, {
      headers: {
        Authorization: `Bearer ${token}`, 
      },
      params: filters, 
    });
    return response.data; 
  } catch (error) {
    console.error('Error fetching students:', error);
    throw error;
  }
};

export const fetchLectures = async (token, filters = {}) => {
  try {
    const response = await axios.get(`${API_URL}/api/academia/lectures`, {
      headers: {
        Authorization: `Bearer ${token}`, 
      },
      params: filters, 
    });
    return response.data; 
  } catch (error) {
    console.error('Error fetching lectures:', error);
    throw error;
  }
};