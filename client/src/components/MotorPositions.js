import React, { Component } from 'react';

class MotorPositions extends Component {
    constructor(props) {
        super(props);
        this.state = {
            response: {}
        };
    }

    componentDidMount() {
        this.fetchMotorPositions();
    }

    fetchMotorPositions = () => {
        fetch('http://localhost:5000/api/get-motor-positions')
            .then(response => response.json())
            .then(data => {
                this.setState({ response: data });
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };

    render() {
        const { response } = this.state;

        return (
            <div>
                <h5>Motor Positions</h5>
                <pre>{JSON.stringify(response, null, 2)}</pre>
                <button onClick={this.fetchMotorPositions}>Refresh</button>
            </div>
        );
    }
}

export default MotorPositions;
