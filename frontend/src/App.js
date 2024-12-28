import React, { useState } from 'react';
import './stiluri/login.css';
import Login from './componente/login';
import { BrowserRouter as Router, Route, Navigate, Routes } from 'react-router-dom';
import AdminPage from './componente/admin'; 
import ProfesorPage from './componente/profesor'; 
import StudentPage from './componente/student'; 

function App() {
  const [token, setToken] = useState(null); 
  const [role, setRole] = useState(null); 

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={
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
          } />

          <Route path="/admin" element={
            token && role === 'admin' ? (
              <AdminPage />
            ) : (
              <Navigate to="/" />
            )
          } />
          
          <Route path="/profesor" element={
            token && role === 'profesor' ? (
              <ProfesorPage />
            ) : (
              <Navigate to="/" />
            )
          } />
          
          <Route path="/student" element={
            token && role === 'student' ? (
              <StudentPage />
            ) : (
              <Navigate to="/" />
            )
          } />

          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
