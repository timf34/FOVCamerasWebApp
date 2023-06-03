import React, { useState } from 'react';
import { auth } from './firebase'; 

export default function StartCameraControlButton() {
    const [deviceId, setDeviceId] = useState('jetson1'); 
    const [startCamera, setStartCamera] = useState('start_camera_control');

    const startCameraControl = async () => {
        if (!auth.currentUser) {
            console.error('User not logged in');
            return;
        }
        else {
            console.log('User logged in:', auth.currentUser.email);
        }
        const token = await auth.currentUser.getIdToken();

        const response = await fetch('http://localhost:5000/api/start-camera', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ deviceId, startCamera })
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
            <button onClick={startCameraControl}>
                Start Camera Control
            </button>
        </div>
    );
}
