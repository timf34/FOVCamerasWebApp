import time


class FPS:
    def __init__(self):
        self._start = None
        self._end = None

        self.num_frames = 0

    def start(self) -> None:
        self._start = time.perf_counter()

    def stop(self) -> None:
        self._end = time.perf_counter()

    def fps(self) -> float:
        return 1 / (self._end - self._start)

    def update(self):
        self.num_frames += 1

    def average_fps(self):
        return self.num_frames / (self._end - self._start)


def test_fps():
    fps = FPS()

    # First lets test the normal FPS timing functionality
    fps.start()
    time.sleep(3)
    fps.stop()
    print("Normal FPS (it should be approx 1/3):", fps.fps())

    # Now lets test the average FPS functionality
    fps.start()
    for _ in range(5):
        time.sleep(0.5)
        fps.update()
    fps.stop()
    print("Average FPS (it should be approx 2 (ie 5 frames/ 5*0.5 seconds):", fps.average_fps())


if __name__ == '__main__':
    test_fps()

