import React, { useEffect, useState } from 'react';
import { useForm } from './useForm';
import '../stylesheets/MotorPositions.css'

function MotorPositions() {
    const initialState = { selectedDevice: 'jetson1' };
    const [values, handleChange] = useForm(initialState);
    const [response, setResponse] = useState({});

    const fetchMotorPositions = () => {
        const { selectedDevice } = values;
        fetch(`${process.env.REACT_APP_URL}/api/get-motor-positions/${selectedDevice}`)
            .then(response => response.json())
            .then(data => setResponse(data))
            .catch((error) => console.error('Error:', error));
    };

    useEffect(() => {
        fetchMotorPositions();
    }, [values.selectedDevice]);

    return (
        <div className="container">
            <h5>Motor Positions</h5>
            <div className="select">
                <label>Select device: </label>
                <select name="selectedDevice" value={values.selectedDevice} onChange={handleChange}>
                    <option value="jetson1">jetson1</option>
                    <option value="jetson2">jetson2</option>
                    <option value="jetson3">jetson3</option>
                    <option value="jetson4">jetson4</option>
                </select>
            </div>
            <div className="pre">
                {Object.entries(response).map(([key, value], i) => (
                    <p key={i}><b>{key}:</b> {value}</p>
                ))}
            </div>
            <button className="button" onClick={fetchMotorPositions}>Refresh</button>
        </div>
    );
}

export default MotorPositions;
