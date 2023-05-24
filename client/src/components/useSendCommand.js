import React, { useState } from 'react';
import { auth } from './firebase'; // Assuming firebase.js and CommandButton.js are in the same directory

export default function CommandButton() {
  const [deviceId, setDeviceId] = useState('device1'); // Set to your device's ID
  const [command, setCommand] = useState('print hello world');

  const sendCommand = async () => {
    const token = await auth.currentUser.getIdToken();

    const response = await fetch('http://localhost:5000/api/command', { 
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ deviceId, command }) 
    });

    if (!response.ok) {
      console.error('Failed to send command:', response.statusText);
      return;
    }

    const responseBody = await response.json();
    console.log(responseBody.message);
  };

  return (
    <button onClick={sendCommand}>
      Send Command
    </button>
  );
}
