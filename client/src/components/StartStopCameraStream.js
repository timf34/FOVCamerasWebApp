import React, { useContext } from 'react';
import { useForm } from "./useForm";
import { auth } from './firebase';
import StreamContext from './StreamContext';
import DeviceContext from './DeviceContext';

export default function CameraStreamForm() {
  const { isStreaming, setStreaming } = useContext(StreamContext);
  const { deviceId, setDeviceId } = useContext(DeviceContext);

  const [values, handleChange] = useForm({
    action: 'start-stream',
  });

  const handleFormSubmit = async (event) => {
    event.preventDefault();

    const { action } = values;

    console.log('deviceId:', deviceId);


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
          <select name="action" value={values.action} onChange={handleChange}>
            <option value="start-stream">Start Camera Stream</option>
            <option value="stop-stream">Stop Camera Stream</option>
          </select>
        </label>
        <button type="submit">Submit</button>
      </form>
  );
}
