import { useState, useEffect } from 'react';
import { getDatabase, ref, onValue, off } from 'firebase/database';
import io from 'socket.io-client';

export default function useStatus(useFirebase) {
  const [status, setStatus] = useState([]);

  useEffect(() => {
    if (useFirebase) {
      const db = getDatabase();
      const statusesRef = ref(db, 'statuses/');

      const listener = onValue(statusesRef, (snapshot) => {
        const val = snapshot.val();

        console.log("val:", val);

        if (val) {
          // Drill down into each device entry and extract the status
          const statusValues = Object.keys(val).map(deviceKey => val[deviceKey].status);
          // const statusValues = Object.values(val).map(device => device.status); This would also work 
          setStatus(Object.values(statusValues));
        } else {
          setStatus([]);
        }
      });

      return () => {
        off(statusesRef, 'value', listener);
      };
    } else {
      const socket = io(`${process.env.REACT_APP_API_URL}`);

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
    }
  }, [useFirebase]);

  return status;
}
