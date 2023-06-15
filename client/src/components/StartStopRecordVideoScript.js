import React, { useState } from 'react';
import { auth } from './firebase';

export default function RecordVideoForm() {
  const [deviceId, setDeviceId] = useState('jetson1');
  const [action, setAction] = useState('start-record');

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
    const apiUrl = action === 'start-record' ? `${process.env.REACT_APP_URL}/api/start-record` : `${process.env.REACT_APP_URL}/api/stop-record`;

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
          <option value="start-record">Start Record Video Script</option>
          <option value="stop-record">Stop Record Video Script</option>
        </select>
      </label>
      <button type="submit">Submit</button>
    </form>
  );
}
