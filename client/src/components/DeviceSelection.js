import React, { useContext } from 'react';
import DeviceContext from './DeviceContext';

function DeviceSelection() {
    const { deviceId, setDeviceId } = useContext(DeviceContext);

    return (
        <select onChange={e => setDeviceId(e.target.value)} value={deviceId}>
            <option value="jetson1">Jetson 1</option>
            <option value="jetson2">Jetson 2</option>
            <option value="jetson3">Jetson 3</option>
            <option value="jetson4">Jetson 4</option>
        </select>
    );
}

export default DeviceSelection;
