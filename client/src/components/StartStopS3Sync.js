import React, { useState, useContext } from 'react';
import {useForm} from "./useForm";
import DeviceContext from "./DeviceContext";

export default function SyncS3Form() {
  const [values, handleChange] = useForm({
    action: 'start',
  });
  const { deviceId, setDeviceId } = useContext(DeviceContext);
  const { action } = values;

  const handleFormSubmit = async (event) => {
    event.preventDefault();

    const apiUrl = action === 'start' ? `${process.env.REACT_APP_URL}/api/start-s3-sync` : `${process.env.REACT_APP_URL}/api/stop-s3-sync`;

    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
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
          <option value="start">Start S3 Sync</option>
          <option value="stop">Stop S3 Sync</option>
        </select>
      </label>
      <button type="submit">Submit</button>
    </form>
  );
}