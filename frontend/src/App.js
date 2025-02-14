import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Navigate, Routes } from 'react-router-dom';
import Login from './components/Login';
import AdminPage from './components/AdminPage';
import ProfesorPage from './components/ProfesorPage';
import StudentPage from './components/StudentPage';
import LecturePage from './components/LecturePage';

function App() {
  const [token, setToken] = useState(null);
  const [role, setRole] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedToken = localStorage.getItem('token');
    const savedRole = localStorage.getItem('role');
    if (savedToken) {
      setToken(savedToken);
      setRole(savedRole);
    }
    setLoading(false);
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route
            path="/"
            element={
              token ? (
                role === 'admin' ? (
                  <Navigate to="/admin" />
                ) : role === 'profesor' ? (
                  <Navigate to="/profesor" />
                ) : role === 'student' ? (
                  <Navigate to="/student" />
                ) : null
              ) : (
                <Login setToken={setToken} setUserRole={setRole} />
              )
            }
          />
          <Route
            path="/admin"
            element={
              token && role === 'admin' ? <AdminPage /> : <Navigate to="/" />
            }
          />
          <Route
            path="/profesor"
            element={
              token && role === 'profesor' ? <ProfesorPage /> : <Navigate to="/" />
            }
          />
          <Route
            path="/student"
            element={
              token && role === 'student' ? <StudentPage /> : <Navigate to="/" />
            }
          />
          <Route
            path="/lecture/:lectureId"
            element={
              token && role === 'profesor' ? <LecturePage /> : <Navigate to="/" />
            }
          />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;