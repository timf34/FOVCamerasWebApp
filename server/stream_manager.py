import threading


class StreamManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.latest_image = None

    def update_image(self, image):
        with self.lock:
            self.latest_image = image

    def get_image(self):
        with self.lock:
            return self.latest_image