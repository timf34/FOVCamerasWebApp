import os

def load_env():
    with open(".env", "r") as f:
        for line in f:
            if line.strip():
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

