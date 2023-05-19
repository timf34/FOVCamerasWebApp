import React, { useState, useEffect } from 'react';
import { signInWithEmailAndPassword, onAuthStateChanged } from "firebase/auth";
import { auth } from './firebase';
import io from 'socket.io-client';

function App() {
    const [status, setStatus] = useState(null);
    const [user, setUser] = useState(null);
    const [email, setEmail] = useState('');  // Add these lines
    const [password, setPassword] = useState('');  // Add these lines
  
    useEffect(() => {
      const socket = io('http://localhost:5000');
  
      socket.on('connect', () => {
        console.log('connected to websocket');
      });
  
      socket.on('status', (data) => {
        setStatus(data);
      });
  
      return () => socket.disconnect();
    }, []);
  
    useEffect(() => {
      onAuthStateChanged(auth, (currentUser) => {
        setUser(currentUser);
      });
    }, []);
  
    const handleLogin = async () => { // remove email and password parameters
      try {
        await signInWithEmailAndPassword(auth, email, password); // use state values
      } catch (error) {
        console.error('Failed to sign in:', error);
      }
    };
  
    return (
      <div className="App">
        {!user ? (
          <div>
            <input type="email" placeholder="Email" onChange={e => setEmail(e.target.value)} /> {/* Add onChange handler */}
            <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} /> {/* Add onChange handler */}
            <button onClick={handleLogin}>Sign In</button> {/* Remove hardcoded values */}
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
