import React, { useState } from 'react';
import {useForm} from "./useForm";
import { auth } from './firebase';

export default function CameraControlForm() {
  const [values, handleChange] = useForm({
    deviceId: 'jetson1',
    action: 'start',
  });
  const { deviceId, action } = values;

  const handleFormSubmit = async (event) => {
    event.preventDefault();

    if (!auth.currentUser) {
      console.error('User not logged in');
      return;
    } else {
      console.log('User logged in:', auth.currentUser.email);
    }

    const token = await auth.currentUser.getIdToken();
    const apiUrl = action === 'start' ? `${process.env.REACT_APP_URL}/api/start-camera` : `${process.env.REACT_APP_URL}/api/stop-camera`;

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
        <select name="action" value={action} onChange={handleChange}>
          <option value="start">Start Camera Control</option>
          <option value="stop">Stop Camera Control</option>
        </select>
      </label>
      <label>
        Select Device:
        <select name="deviceId" value={deviceId} onChange={handleChange}>
          <option value="jetson1">Jetson 1</option>
          <option value="jetson2">Jetson 2</option>
        </select>
      </label>
      <button type="submit">Submit</button>
    </form>
  );
}
