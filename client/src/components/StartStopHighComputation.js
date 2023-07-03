import React, { useState } from 'react';
import { auth } from './firebase';

export default function HighComputationForm() {
  const [deviceId, setDeviceId] = useState('jetson1');
  const [action, setAction] = useState('start');

  const handleActionChange = (event) => {
    setAction(event.target.value);
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();

    if (!auth.currentUser) {
      console.error('User not logged in');
      return;
    } else {
      console.log('User logged in:', auth.currentUser.email);
    }

    const token = await auth.currentUser.getIdToken();
    const apiUrl = action === 'start' ? `${process.env.REACT_APP_URL}/api/start-high-computation` : `${process.env.REACT_APP_URL}/api/stop-high-computation`;

    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ deviceId, action }),
    });

    if (!response.ok) {
      console.error('Failed to send high computation command:', response.statusText);
      return;
    }

    const responseBody = await response.json();
    console.log(responseBody.message);
  };

  return (
    <form onSubmit={handleFormSubmit}>
      <label>
        Select action:
        <select value={action} onChange={handleActionChange}>
          <option value="start">Start High Computation Script</option>
          <option value="stop">Stop High Computation Script</option>
        </select>
      </label>
      <label>
        Select Device:
        <select onChange={e => setDeviceId(e.target.value)} value={deviceId}>
          <option value="jetson1">Jetson 1</option>
          <option value="jetson2">Jetson 2</option>
        </select>
      </label>
      <button type="submit">Submit</button>
    </form>
  );
}
