import React, {useContext, useEffect, useState} from 'react';
import { useForm } from './useForm';
import deviceContext from "./DeviceContext";
import '../stylesheets/MotorPositions.css'
import DeviceContext from "./DeviceContext";

function MotorPositions() {
    const { deviceId, setDeviceId } = useContext(DeviceContext);
    const [response, setResponse] = useState({});

    const fetchMotorPositions = () => {
        fetch(`${process.env.REACT_APP_URL}/api/get-motor-positions/${deviceId}`)
            .then(response => response.json())
            .then(data => setResponse(data))
            .catch((error) => console.error('Error:', error));
    };

    useEffect(() => {
        fetchMotorPositions();
    }, [deviceId]);

    return (
        <div className="container">
            <h5>Motor Positions</h5>
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
