# FoV Cameras Web App

This project provides a dashboard for monitoring multiple Nvidia Jetson Nano devices installed around a football pitch.

## Project Structure

The project is divided into two parts:

1. `client`: This directory contains the React application.
2. `server`: This directory contains the Express.js server that serves the API used by the client.

## Prerequisites

1. [Node.js](https://nodejs.org/en/download/) and [npm](https://www.npmjs.com/get-npm) (comes with Node.js) should be installed.
2. [Python](https://www.python.org/downloads/) (if you're using the Python server)

## Development

### Starting the Server

<!-- For Node.js server:

1. Navigate into the `server` directory from the terminal:
    ```bash
    cd server
    ```
2. Install the necessary packages:
    ```bash
    npm install
    ```
3. Start the server:
    ```bash
    node server.js
    ```

The server will run on [http://localhost:3000](http://localhost:3000). -->

For Python server:

**Note that you need to run this through the venv! Otherwise the server doesn't work and gets stuck in the backgroun tasks func**

1. Navigate into the `server` directory from the terminal:
    ```bash
    cd server
    ```
2. Create activate a virtual environment (venv):
   - Windows:
     - Create a venv:
         ```bash
        python -m venv env
        ```
      - Activate the venv:
        ```bash
         env\Scripts\activate
        ```
    - Linux/macOS:
      - Create a venv:
        ```bash
        python3 -m venv venv
        ```
      - Activate the venv:
        ```bash
        source venv/bin/activate
        ```
3. Install the necessary packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Start the server:
    ```bash
    python server.py
    ```
5. Start the Jetson simulator:
   ```bash
    python jetson_simulator.py [device-id]
    ```

The server will run on [http://localhost:5000](http://localhost:5000).

### Starting the Client

1. Navigate into the `client` directory from the terminal:
    ```bash
    cd client
    ```
2. Install the necessary packages:
    ```bash
    npm install
    ```
3. Start the application:
    ```bash
    npm start
    ```

The application will run on [http://localhost:3000](http://localhost:3000) if you're using the Node.js server, or [http://localhost:5000](http://localhost:5000) if you're using the Python server.

## Testing

You can test the server by navigating to the `/api/status` endpoint (e.g., [http://localhost:3000/api/status](http://localhost:3000/api/status)) in your web browser. You should see a JSON object with the status of the Jetson device.

## Running 

1. Start the server.
```bash
cd server
env\Scripts\activate
python server.py
```

2. Start the Jetson simulator.
```bash
python jetson_simulator.py [device-id]
```

3. Start the client.
```bash
cd client
npm start
```

Also note to be sure to run `server.py` before running `jetson_simulator.py [device_id]` to 
ensure that there is a server there for the device to connect to (and so its ID is properly 
added to the list of connections).