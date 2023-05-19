import React, { useState, useEffect } from 'react';
import { signInWithEmailAndPassword, onAuthStateChanged } from "firebase/auth";
import { auth } from './firebase';
import io from 'socket.io-client';

function App() {
  const [status, setStatus] = useState(null);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const socket = io('http://localhost:5000');

    socket.on('connect', () => {
      console.log('connected to websocket');
    });

    socket.on('status', (data) => {
      setStatus(data);
    });

    // Clean up on unmount
    return () => socket.disconnect();
  }, []);

  useEffect(() => {
    onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
    });
  }, []);

  const handleLogin = async (email, password) => {
    try {
      await signInWithEmailAndPassword(auth, email, password);
    } catch (error) {
      console.error('Failed to sign in:', error);
    }
  };

  return (
    <div className="App">
      {!user ? (
        <div>
          <input type="email" placeholder="Email" />
          <input type="password" placeholder="Password" />
          <button onClick={() => handleLogin('tim@fov.ie', 'password here!')}>Sign In</button>
        </div>
      ) : status ? (
        <div>
          <p>Device ID: {status.deviceId}</p>
          <p>WiFi Status: {status.wifiStatus ? 'Connected' : 'Disconnected'}</p>
          <p>Battery Level: {status.batteryLevel}</p>
          <p>Temperature: {status.temperature}</p>
        </div>
      ) : (
        <p>Loading status...</p>
      )}
    </div>
  );
}

export default App;
