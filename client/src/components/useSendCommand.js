import React, { useState, useContext } from 'react';
import { auth } from './firebase';
import DeviceContext from "./DeviceContext";

export default function CommandButton() {
    const [command, setCommand] = useState('print hello world');
    const { deviceId, setDeviceId } = useContext(DeviceContext);

    const sendCommand = async () => {
        if (!auth.currentUser) {
            console.error('User not logged in');
            return;
        }
        else {
            console.log('User logged in:', auth.currentUser.email);
        }
        const token = await auth.currentUser.getIdToken();

        console.log('Token:', token);
        console.log('deviceId:', deviceId)

        const response = await fetch(`${process.env.REACT_APP_URL}/api/command`, {
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
        <div>
            <button onClick={sendCommand}>
                Send Command
            </button>
        </div>
    );
}
