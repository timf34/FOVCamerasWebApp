import React, { Component } from 'react';

class MotorPositions extends Component {
    constructor(props) {
        super(props);
        this.state = {
            response: {},
            selectedDevice: 'jetson1',  // default to jetson1
        };
    }

    componentDidMount() {
        this.fetchMotorPositions();
    }

    fetchMotorPositions = () => {
        const { selectedDevice } = this.state;
        fetch(`http://localhost:5000/api/get-motor-positions/${selectedDevice}`)
            .then(response => response.json())
            .then(data => {
                this.setState({ response: data });
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };

    handleDeviceChange = (event) => {
        this.setState({ selectedDevice: event.target.value });
    };

    render() {
        const { response, selectedDevice } = this.state;

        return (
            <div>
                <h5>Motor Positions</h5>
                <div>
                    <label>Select device: </label>
                    <select value={selectedDevice} onChange={this.handleDeviceChange}>
                        <option value="jetson1">jetson1</option>
                        <option value="jetson2">jetson2</option>
                        <option value="jetson3">jetson3</option>
                        <option value="jetson4">jetson4</option>
                    </select>
                </div>
                <pre>{JSON.stringify(response, null, 2)}</pre>
                <button onClick={this.fetchMotorPositions}>Refresh</button>
            </div>
        );
    }
}

export default MotorPositions;
