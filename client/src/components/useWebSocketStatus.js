import { useState, useEffect } from 'react';
import io from 'socket.io-client';

export default function useWebSocketStatus() {
  const [status, setStatus] = useState([]);

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

  return status;
}
