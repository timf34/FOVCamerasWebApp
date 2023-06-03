import React from 'react';
import '../stylesheets/StatusList.css';  

export default function StatusList({ status }) {
  if (!status.length) {
    return <p>Loading status...</p>;
  }

  return (
    <div>
      {status.map(deviceStatus => (
        <div key={deviceStatus.deviceId}  className={`status-box ${deviceStatus.wifiStatus ? 'connected' : 'disconnected'}`}>
          <p>Device ID: {deviceStatus.deviceId}</p>
          <p>WiFi Status: {deviceStatus.wifiStatus ? 'Connected' : 'Disconnected'}</p>
          <p>Battery Level: {deviceStatus.batteryLevel}</p>
          <p>Temperature: {deviceStatus.temperature}</p>
        </div>
      ))}
    </div>
  );
}
