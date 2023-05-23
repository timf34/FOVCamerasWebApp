import React from 'react';

export default function StatusList({ status }) {
  if (!status.length) {
    return <p>Loading status...</p>;
  }

  return (
    <div>
      {status.map(deviceStatus => (
        <div key={deviceStatus.deviceId}>
          <p>Device ID: {deviceStatus.deviceId}</p>
          <p>WiFi Status: {deviceStatus.wifiStatus ? 'Connected' : 'Disconnected'}</p>
          <p>Battery Level: {deviceStatus.batteryLevel}</p>
          <p>Temperature: {deviceStatus.temperature}</p>
        </div>
      ))}
    </div>
  );
}
