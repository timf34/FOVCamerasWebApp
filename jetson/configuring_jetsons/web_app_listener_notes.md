## Setup

Run the following command to set up the web_app_listener service. 

Note that you need sudo privileges to run this command.

```bash
chmod +x web_app_listener_setup.sh 
sudo ./web_app_listener_setup.sh
```


## Old notes 

You can use systemd services to manage the execution of your Python script in the background when your Nvidia Jetson Nano connects to the internet.

Here are the steps you need to follow:

1. **Create a systemd service file:**

Create a file:

`sudo nano /etc/systemd/system/web_app_listener.service`

The service file can be something like:

```
[Unit]
Description=Python Script jetson_simulator
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/tim/Desktop/FOVCamerasWebApp/jetson/jetson_simulator.py jetson
WorkingDirectory=/home/tim/Desktop/FOVCamerasWebApp
Restart=always
User=tim
Environment="PATH=/usr/bin:/bin:/usr/sbin:/sbin"
EnvironmentFile=/home/tim/Desktop/FOVCamerasWebApp/jetson/.env

[Install]
WantedBy=multi-user.target
```
In this configuration:

- `Description` gives a brief explanation of the service.
- `After=network.target` ensures the service will start after the network is up.
- `ExecStart` specifies the command to start the service. Replace `/path/to/` with the actual path to your Python script and `/usr/bin/python3` with the output of `which python3`.
- `WorkingDirectory` is where the script is located. Replace `/path/to/` with the actual path of the script.
- `Restart=always` ensures the script is restarted if it ever fails.
- `User` is the user who will run the script. On the Jetson Nano, it's usually `nvidia`.
- `Environment` can be used to set environment variables for your service. In this case, we're setting the PATH variable to include the location of Python3.
- `EnvironmentFile` is a path to a file from which to read environment variables. Replace `/path/to/.env` with the path to your `.env` file. If the environment variables are already available in the system, this line may be unnecessary.
- `WantedBy=multi-user.target` ensures the service starts at boot.

2. **Enable and start the service:**

After creating the service file, refresh the systemd manager configuration by running:

```
sudo systemctl daemon-reload
```

Then, enable the service to start at boot:

```
sudo systemctl enable web_app_listener.service
```

And start the service:

```
sudo systemctl start web_app_listener.service
```

And check its status with:

```bash
sudo systemctl status web_app_listener.service
```

Now, your Python script should run in the background whenever your Nvidia Jetson Nano connects to the internet and it will restart if it ever fails.

Remember, you should create separate service files for each instance of your script if you plan to run it with different arguments (e.g., `jetson_nano_1`, `jetson_nano_2`, etc.). The service files should have different names and `ExecStart` lines for each instance.

Also, check the status of your service by running `sudo systemctl status web_app_listener.service`. You can view the service logs with `journalctl -u web_app_listener.service`.

**Also note that I need to ensure that the python files we are running/ executing are executable!**

Run `chmod +x jetson_simulator.py` to make the file executable.