import React, { useState } from 'react';
import { auth } from './firebase'; 

export default function SendInputButton() {
    const [deviceId, setDeviceId] = useState('jetson1'); 
    const [inputData, setInputData] = useState('');

    const sendInput = async () => {
        if (!auth.currentUser) {
            console.error('User not logged in');
            return;
        }
        else {
            console.log('User logged in:', auth.currentUser.email);
        }
        const token = await auth.currentUser.getIdToken();

        console.log('Token:', token);

        const response = await fetch('http://localhost:5000/api/send-input', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ deviceId, input: inputData })
        });

        if (!response.ok) {
            console.error('Failed to send input:', response.statusText);
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
            <input 
                type="text" 
                value={inputData} 
                onChange={e => setInputData(e.target.value)}
                placeholder="Enter input" 
            />
            <button onClick={sendInput}>
                Send Input
            </button>
        </div>
    );
}
