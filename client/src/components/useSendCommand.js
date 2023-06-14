import React, { useState } from 'react';
import { auth } from './firebase'; 

export default function CommandButton() {
    const [deviceId, setDeviceId] = useState('jetson1'); 
    const [command, setCommand] = useState('print hello world');

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

        const response = await fetch(`${process.env.REACT_APP_API_URL}/api/command`, {
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
            <select onChange={e => setDeviceId(e.target.value)} value={deviceId}>
                <option value="jetson1">jetson1</option>
                <option value="jetson2">jetson2</option>
                <option value="jetson3">jetson3</option>
                <option value="jetson4">jetson4</option>
            </select>
            <button onClick={sendCommand}>
                Send Command
            </button>
        </div>
    );
}
