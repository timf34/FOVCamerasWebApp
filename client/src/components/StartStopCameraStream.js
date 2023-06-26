import React, { useState, useContext } from 'react';
import { auth } from './firebase';
import StreamContext from './StreamContext';

export default function CameraStreamForm() {
  const [deviceId, setDeviceId] = useState('jetson1');
  const [action, setAction] = useState('start-stream');
  const { isStreaming, setStreaming } = useContext(StreamContext);

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

    if (action === 'start-stream') {
      setStreaming(true);
    } else {
      setStreaming(false);
    }

    const token = await auth.currentUser.getIdToken();
    const apiUrl = action === 'start-stream' ? `${process.env.REACT_APP_URL}/api/start-camera-stream` : `${process.env.REACT_APP_URL}/api/stop-camera-stream`;

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
          <option value="start-stream">Start Camera Stream</option>
          <option value="stop-stream">Stop Camera Stream</option>
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
