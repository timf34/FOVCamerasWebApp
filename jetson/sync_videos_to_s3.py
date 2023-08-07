import os
import subprocess

my_env = os.environ.copy()
my_env["PATH"] = "/home/fov/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"


try:
    if os.name == 'nt':
        # Windows
        result = subprocess.run(['aws', 's3', 'sync', './videos', 's3://australia-fov'], check=True, env=my_env)
    else:
        result = subprocess.run(['aws', 's3', 'sync', '/home/fov/Desktop/videos', 's3://australia-fov'], check=True)
except subprocess.CalledProcessError as e:
    # TODO: this should be logged to a log file that is synced to AWS
    print(f"Sync failed with error: {e}")
