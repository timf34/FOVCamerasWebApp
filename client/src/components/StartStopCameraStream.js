import React, { useState } from 'react';
import { auth } from './firebase';

export default function CameraStreamForm() {
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
    const apiUrl = action === 'start' ? 'http://localhost:5000/api/start-camera-stream' : 'http://localhost:5000/api/stop-camera-stream';

    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ deviceId, action }),
    });

    if (!response.ok) {
      console.error('Failed to send command:', response.statusText);
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
          <option value="start-stream">Start Camera Stream Control</option>
          <option value="stop-stream">Stop Camera Stream Control</option>
        </select>
      </label>
      <button type="submit">Submit</button>
    </form>
  );
}
