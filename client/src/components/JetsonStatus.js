import React from 'react';

class JetsonStatus extends React.Component {
    constructor(props) {
        super(props);
        this.state = { status: null };
    }

    componentDidMount() {
        // Replace with the actual API endpoint
        fetch('http://localhost:3000/api/status')
            .then(response => response.json())
            .then(data => this.setState({ status: data }));
    }

    render() {
        const { status } = this.state;

        if (!status) {
            return <div>Loading...</div>;
        }

        return (
            <div>
                <h1>Status of {status.deviceId}</h1>
                <p>WiFi Status: {status.wifiStatus ? 'Connected' : 'Disconnected'}</p>
                <p>Battery Level: {status.batteryLevel}%</p>
                <p>Temperature: {status.temperature}°C</p>
                {/* Display any other status information you need */}
            </div>
        );
    }
}

export default JetsonStatus;
