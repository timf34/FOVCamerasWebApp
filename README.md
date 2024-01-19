# FoV Cameras Web App

This project provides a dashboard for monitoring multiple Nvidia Jetson Nano devices installed around a football pitch.

## Project Structure

The project is divided into three parts:

1. `client`: This directory contains the frontend React application.
2. `server`: This directory contains the server code that serves the client and handles the API requests.
3. `jetson`: This directory contains the Python script that runs on the Jetson devices

## Development

### Server

#### Local: Running Flask server through Gunicorn (simulating production)

1. Use **WSL** to navigate into the `server` directory from the terminal:
    ```bash
    cd server
    ```
2. Create activate a virtual environment (venv):
3. Activate the venv (if not already activated):
    ```bash
    source wsl_venv/bin/activate
    ```
4. Run gunicorn server:
    ```bash
   gunicorn -k eventlet -w 1 application:application
   ```

#### Local: Running Flask directly

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
        venv\Scripts\activate
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
    python application.py
    ```
5. Start the Jetson simulator:
   ```bash
    python jetson_simulator.py [device-id]
    ```

The server will run on [http://localhost:5000](http://localhost:5000).


### Client

#### Serving the Client from the Server

1. Build ReactJS client
    - `cd client`
    - `npm run build`
1. Move build folder to server folder
    - `mv build/ server/`
    - Or just copy, paste, etc.
1. Start the server as shown above. 


#### Starting the Client Directly (without the server)

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

## Older notes 

### The Client code is served from the server 

Note that in our current setup, we serve the client code from the server (i.e. from `/build`). To update this, do the following:

1. Build the client code 
   1. `cd client`
   2. `npm run build`
   3. Copy and paste the resulting `/build` directory in `/client` into the root directory of `/server`
   4. We can now serve the client code from the server:)  

## Testing

You can test the server by navigating to the `/api/status` endpoint (e.g., [http://localhost:5000/api/status](http://localhost:3000/api/status)) in your web browser. You should see a JSON object with the status of the Jetson device.

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


**Note:**

I have created a symbolic link between the root .env file and the .env files in the different sub folders 
so I only have to change one file. (used this command: `mklink .env ..\.env`)

To test the .env file locally, use:
```
REACT_APP_URL=http://localhost:5000
```

or 
```
REACT_APP_URL=http://192.168.234.1:5000
```

To deploy it on AWS, use: 
```
REACT_APP_URL=http://fovcameraswebappv2.eu-west-1.elasticbeanstalk.com
```

### Deploying to AWS EB

1. Build ReactJS client
    - `cd client`
    - `npm run build`
1. Move build folder to server folder
    - `mv build/ server/`
    - Or just copy, paste, etc.
1. Create a zip file of the server folder
    - `zip -r server.zip server/`
    - Or just right click and compress
        - Ensure to not select the `Dockerfile`, `/venv`, `/aws_zips` or `.dockerignore` when compressing
    - _Note: Don't include the following directories or files: `Dockerfile`, `venv`, `pycache`, `.dockerignore` when zipping._