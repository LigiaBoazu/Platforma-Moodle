// src/componente/login.js
import React, { useState } from 'react';

function Login({ setToken, setUserRole }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:8000/api/academia/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: email,
          password: password,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        setToken(data.access_token);
        const decodedToken = JSON.parse(atob(data.access_token.split('.')[1]));
        setUserRole(decodedToken.role);
      } else {
        setError('Email sau parolă incorectă!');
      }
    } catch (error) {
      setError('Eroare la conectare. Te rugăm să încerci din nou!');
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Parolă</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
