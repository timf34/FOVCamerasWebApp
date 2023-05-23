import React, { useState, useEffect } from 'react';
import { signInWithEmailAndPassword, onAuthStateChanged } from "firebase/auth";
import { auth } from './firebase';
import io from 'socket.io-client';

function App() {
    const [status, setStatus] = useState([]);
    const [user, setUser] = useState(null);
    const [email, setEmail] = useState('');  
    const [password, setPassword] = useState(''); 
    const [errorMessage, setErrorMessage] = useState(null);
    const [useFirebase, setUseFirebase] = useState(false);  // set to true to use firebase database listening, false to use websocket listening
  
    useEffect(() => {
        const socket = io('http://localhost:5000');
    
        socket.on('connect', () => {
            console.log('connected to websocket dawg');
        });
    
        socket.on('status', (data) => {
            setStatus(oldStatuses => {
                const newStatuses = [...oldStatuses];
                const deviceId = Object.keys(data)[0];
                const status = data[deviceId];
                const index = newStatuses.findIndex(status => status.deviceId === deviceId);
                if (index === -1) {
                    newStatuses.push(status);
                } else {
                    newStatuses[index] = status;
                }
                return newStatuses;
            });
        });
    
        return () => socket.disconnect();
    }, []);
    
  
    useEffect(() => {
      onAuthStateChanged(auth, (currentUser) => {
        setUser(currentUser);
      });
    }, []);
  
    const handleLogin = async () => {
        try {
          await signInWithEmailAndPassword(auth, email, password);
          setErrorMessage(null);
        } catch (error) {
          console.error('Failed to sign in:', error);
          setErrorMessage('Failed to sign in');
        }
      };
  
    return (
      <div className="App">
        {!user ? (
          <div>
            <input type="email" placeholder="Email" onChange={e => setEmail(e.target.value)} />
            <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
            <button onClick={handleLogin}>Sign In</button>
            {errorMessage && <p>{errorMessage}</p>}
          </div>
        ) : status.length ? (
          <div>
            {status.map(deviceStatus => (
              <div key={deviceStatus.deviceId}>
                <p>Device ID: {deviceStatus.deviceId}</p>
                <p>WiFi Status: {deviceStatus.wifiStatus ? 'Connected' : 'Disconnected'}</p>
                <p>Battery Level: {deviceStatus.batteryLevel}</p>
                <p>Temperature: {deviceStatus.temperature}</p>
              </div>
            ))}
          </div>
        ) : (
          <p>Loading status...</p>
        )}
      </div>
    );
  }
  
export default App;
