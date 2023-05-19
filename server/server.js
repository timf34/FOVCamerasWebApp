// Note: going to stick with a Python Flask backend as that's what
// I know best and will be fastest to develop. 

const express = require('express');
const app = express();
const cors = require('cors');

app.use(cors()); // This allows cross-origin requests

// Pseudo status data
const status = {
    'deviceId': 'jetson_nano_1',
    'wifiStatus': true,
    'batteryLevel': 90,
    'temperature': 40
};

app.get('/api/status', (req, res) => {
    res.json(status);
});

app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});
