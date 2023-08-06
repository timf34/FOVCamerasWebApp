import subprocess

try:
    result = subprocess.run(['aws', 's3', 'sync', '/home/fov/Desktop/videos', 's3://australia-fov'], check=True)
except subprocess.CalledProcessError as e:
    # TODO: this should be logged to a log file that is synced to AWS
    print(f"Sync failed with error: {e}")
