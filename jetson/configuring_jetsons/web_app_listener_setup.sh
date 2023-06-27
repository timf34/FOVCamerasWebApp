#!/bin/bash

# Note: System wide environment variables are defined in /etc/environment

# Define the service file path
SERVICE_FILE_PATH="/etc/systemd/system/jetson_simulator.service"

# Define the user
USER_NAME="timf34"

# Define the python script path
PYTHON_SCRIPT_PATH="/home/$USER_NAME/Desktop/FOVCamerasWebApp/jetson/jetson_simulator.py"

# Create the service file with the appropriate content
echo "[Unit]
Description=Python Script jetson_simulator
Wants=network-online.target
After=network-online.target

[Service]
User=$USER_NAME
ExecStart=/usr/bin/python3 $PYTHON_SCRIPT_PATH $DEVICE_NAME
Restart=always
Environment=\"PATH=/usr/bin:/bin:/usr/sbin:/sbin\"
EnvironmentFile=/home/$USER_NAME/Desktop/FOVCamerasWebApp/jetson/.env

[Install]
WantedBy=multi-user.target" | sudo tee $SERVICE_FILE_PATH

# Set the appropriate permissions for the service file
sudo chmod 644 $SERVICE_FILE_PATH

# Reload the systemd manager configuration
sudo systemctl daemon-reload

# Enable the service so that it starts on boot
sudo systemctl enable jetson_simulator.service

# Start the service immediately
sudo systemctl start jetson_simulator.service

# Check the status of the service
sudo systemctl status jetson_simulator.service
