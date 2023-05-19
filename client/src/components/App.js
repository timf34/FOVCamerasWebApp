import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

function App() {
    const [status, setStatus] = useState(null);

    useEffect(() => {
        const socket = io('http://localhost:5000');

        socket.on('connect', () => {
            console.log('connected to websocket');
        });

        socket.on('status', (data) => {
            setStatus(data);
        });

        // Clean up on unmount
        return () => socket.disconnect();
    }, []);

    return (
        <div className="App">
            {status ? (
                <div>
                    <p>Device ID: {status.deviceId}</p>
                    <p>WiFi Status: {status.wifiStatus ? 'Connected' : 'Disconnected'}</p>
                    <p>Battery Level: {status.batteryLevel}</p>
                    <p>Temperature: {status.temperature}</p>
                </div>
            ) : (
                <p>Loading status...</p>
            )}
        </div>
    );
}

export default App;
