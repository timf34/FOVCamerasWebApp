import React, { useState } from 'react';
import { auth } from './firebase'; 

export default function MotorControlForm() {
    const [deviceId, setDeviceId] = useState('jetson1'); 
    const [axis, setAxis] = useState('');
    const [percentage, setPercentage] = useState('');

    const moveMotor = async () => {
        if (!auth.currentUser) {
            console.error('User not logged in');
            return;
        }
        else {
            console.log('User logged in:', auth.currentUser.email);
        }
        
        const token = await auth.currentUser.getIdToken();

        console.log('Token:', token);

        const response = await fetch(`${process.env.REACT_APP_URL}/api/send-input`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ deviceId, input: axis + percentage })
        });

        if (!response.ok) {
            console.error('Failed to move motor:', response.statusText);
            return;
        }

        const responseBody = await response.json();
        console.log(responseBody.message);
    };

    return (
        <div>
            <label>
                Axis:
                <select value={axis} onChange={(e) => setAxis(e.target.value)}>
                    <option value="">--Select an axis--</option>
                    <option value="f,">F</option>
                    <option value="i,">I</option>
                    <option value="z,">Z</option>
                </select>
            </label>
            <label>
                Percentage:
                <input type="number" value={percentage} onChange={(e) => setPercentage(e.target.value)} />
            </label>
            <label>
                Select Device:
                <select onChange={e => setDeviceId(e.target.value)} value={deviceId}>
                  <option value="jetson1">Jetson 1</option>
                  <option value="jetson2">Jetson 2</option>
                </select>
            </label>
            <button onClick={moveMotor}>
                Move Motor
            </button>
        </div>
    );
}
