import React, { useState } from 'react';
import { auth } from './firebase'; 

export default function MotorControlForm() {
    const [deviceId, setDeviceId] = useState('jetson1'); 
    const [axis, setAxis] = useState('');
    const [steps, setSteps] = useState('');
    const [usePercentage, setUsePercentage] = useState(false);

    const maxSteps = { "f,": 9353, "i,": 75, "z,": 4073 };

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

        // Calculate the steps or percentage depending on the selection
        let calculatedSteps = steps;
        if (usePercentage) {
            calculatedSteps = Math.round((steps / 100) * maxSteps[axis]);
        }

        console.log("Calculated steps:", calculatedSteps);

        const response = await fetch(`${process.env.REACT_APP_URL}/api/send-input`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ deviceId, input: axis + calculatedSteps })
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
                Mode:
                <select value={usePercentage} onChange={(e) => setUsePercentage(e.target.value === 'true')}>
                    <option value={false}>--Select mode--</option>
                    <option value={false}>Steps</option>
                    <option value={true}>Percentage</option>
                </select>
            </label>
            <label>
                Input Value:
                <input type="number" value={steps} onChange={(e) => setSteps(e.target.value)} />
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
