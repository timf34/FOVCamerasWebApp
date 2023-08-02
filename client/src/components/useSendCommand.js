import React, { useState, useContext } from 'react';
import DeviceContext from "./DeviceContext";

export default function CommandButton() {
    const [command, setCommand] = useState('print hello world');
    const { deviceId, setDeviceId } = useContext(DeviceContext);

    const sendCommand = async () => {

        console.log('deviceId:', deviceId)

        const response = await fetch(`${process.env.REACT_APP_URL}/api/command`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
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
            <button onClick={sendCommand}>
                Send Command
            </button>
        </div>
    );
}
