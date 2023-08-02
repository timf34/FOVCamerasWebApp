import React, { useState, useContext } from 'react';
import {useForm} from "./useForm";
import DeviceContext from "./DeviceContext";

export default function MotorControlForm() {
    const [values, handleChange] = useForm({
        axis: '',
        steps: '',
        mode: '',
    });

    const { deviceId, setDeviceId } = useContext(DeviceContext);
    const { axis, steps, mode } = values;
    const [errorMessage, setErrorMessage] = useState('');
    const maxSteps = { "f,": 9353, "i,": 75, "z,": 4073 };

    const moveMotor = async () => {
        console.log('Device ID:', deviceId);

        // Calculate the steps or percentage depending on the selection
        let calculatedSteps = steps;

        // TODO: add a warning and fix to say that the input has to be between 100 and 0 if the percentage is selected
        if (mode === 'percentage') {

            if (steps > 100 || steps < 0) {
                const error = 'Percentage should be between 0 and 100';
                console.error(error);
                setErrorMessage(error);
            }

            calculatedSteps = Math.round((steps / 100) * maxSteps[axis]);
        }

        console.log("Calculated steps:", calculatedSteps);

        const response = await fetch(`${process.env.REACT_APP_URL}/api/send-input`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
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
            {errorMessage && <p style={{ color: 'red' }}>Error: {errorMessage}</p>}
            <label>
                Axis:
                <select name="axis" value={axis} onChange={handleChange}>
                    <option value="">--Select an axis--</option>
                    <option value="f,">F</option>
                    <option value="i,">I</option>
                    <option value="z,">Z</option>
                </select>
            </label>
            <label>
                Mode:
                <select name="mode" value={mode} onChange={handleChange}>
                    <option value=''>--Select mode--</option>
                    <option value='steps'>Steps</option>
                    <option value='percentage'>Percentage</option>
                </select>
            </label>
            <label>
                Input Value:
                <input name="steps" type="number" value={steps} onChange={handleChange} />
            </label>
            <button onClick={moveMotor}>
                Move Motor
            </button>
        </div>
    );
}
