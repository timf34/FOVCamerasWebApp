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
            <option value="marvel-fov-1">marvel-fov-1</option>
            <option value="marvel-fov-2">marvel-fov-2</option>
            <option value="marvel-fov-3">marvel-fov-3</option>
            <option value="marvel-fov-4">marvel-fov-4</option>
            <option value="marvel-fov-5">marvel-fov-5</option>
            <option value="marvel-fov-6">marvel-fov-6</option>
            <option value="marvel-fov-7">marvel-fov-7</option>
            <option value="marvel-fov-8">marvel-fov-8</option>
        </select>
    );
}

export default DeviceSelection;
