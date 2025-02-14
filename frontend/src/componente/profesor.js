import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function ProfesorPage() {
  const [lectures, setLectures] = useState([]);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  useEffect(() => {
    const fetchLectures = async () => {
      try {
        const userData = JSON.parse(atob(token.split('.')[1]));
        console.log('Decoded token:', userData);
        
        const professorId = userData.id;
        console.log('Making request for professor ID:', professorId);

        const response = await axios.get(
          `http://localhost:8000/api/academia/professors/${professorId}/lectures`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        console.log('Raw API response:', response);
        console.log('Response data:', response.data);

        if (Array.isArray(response.data)) {
          setLectures(response.data);
        } else {
          console.error('Unexpected data format:', response.data);
          setError('Received invalid data format from server');
        }
      } catch (err) {
        console.error('Full error object:', err);
        if (err.response) {
          console.error('Error response:', err.response.data);
          setError(typeof err.response.data === 'string' 
            ? err.response.data 
            : 'Server error occurred');
        } else if (err.request) {
          console.error('Error request:', err.request);
          setError('No response received from server');
        } else {
          console.error('Error message:', err.message);
          setError('Failed to send request');
        }
      }
    };

    if (token) {
      fetchLectures();
    }
  }, [token]);

  const handleLectureClick = (lectureCod) => {
    navigate(`/lecture/${lectureCod}`);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Professor Dashboard</h1>
      <h2 className="text-xl mb-4">Your Lectures</h2>
      {error && <p className="text-red-500 mb-4">
        {typeof error === 'string' ? error : 'An error occurred'}
      </p>}
      <div className="space-y-4">
        {Array.isArray(lectures) && lectures.length > 0 ? (
          lectures.map((lecture) => {
            if (!lecture || typeof lecture !== 'object') {
              console.error('Invalid lecture object:', lecture);
              return null;
            }
            
            return (
              <button
                key={lecture.cod}
                onClick={() => handleLectureClick(lecture.cod)}
                className="w-full p-4 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
              >
                {lecture.nume_disciplina || 'Unnamed Lecture'}
              </button>
            );
          })
        ) : (
          <p>No lectures available.</p>
        )}
      </div>
    </div>
  );
}

export default ProfesorPage;