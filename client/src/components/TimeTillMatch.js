import React, {useContext, useEffect, useState} from 'react';
import { useForm } from './useForm';
import deviceContext from "./DeviceContext";
import '../stylesheets/MotorPositions.css'
import DeviceContext from "./DeviceContext";

function TimeTillMatch() {
    const { deviceId, setDeviceId } = useContext(DeviceContext);
    const [response, setResponse] = useState({});

    const fetchTimeTillMatch = () => {
        fetch(`${process.env.REACT_APP_URL}/api/get-time-till-match/${deviceId}`)
            .then(response => response.json())
            .then(data => setResponse(data))
            .catch((error) => console.error('Error:', error));
    };

    useEffect(() => {
        fetchTimeTillMatch();
    }, [deviceId]);

    return (
    <div className="container">
        <h5>Time Till Match</h5>
        <div className="pre">
    {JSON.stringify(response)}
</div>
        <button className="button" onClick={fetchTimeTillMatch}>Refresh</button>
    </div>
);

}

export default TimeTillMatch;
