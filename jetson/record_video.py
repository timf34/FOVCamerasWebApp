import cv2
import datetime
import os
import time

from datetime import datetime
from typing import Tuple

from config import BohsConfig
from utils.fps import FPS
from utils.logger import Logger
from utils.utility_funcs import get_ip_address, check_and_create_dir, get_log_file_path

from config import *


class VideoRecorder:
    def __init__(self, debug: bool = False, width: int = 1280, height: int = 720):
        self.debug: bool = debug
        self.conf: BohsConfig = BohsConfig()
        self.width: int = width
        self.height: int = height
        self.frame_size: Tuple[int, int] = (self.width, self.height)
        self.today: datetime = datetime.now()
        self.jetson_name: str = self.conf.jetson_name[-1]  # The final character of the jetson name (i.e. jetson1 -> 1)
        self.log_file_path: str = get_log_file_path(jetson_name=self.conf.jetson_name)
        self.logger: Logger = Logger(
            log_file_path=self.log_file_path,
            buffer_size=100,
            print_to_console=True,
            console_buffer_size=2
        )

    def get_log_file_path(self) -> str:
        """Returns the path to the log file"""
        if os.name == 'nt':
            log_dir = f"{os.getcwd()}/logs/laptop"
        else:
            log_dir = f"{os.getcwd()}/logs/{self.jetson_name}"
        check_and_create_dir(log_dir)
        return f"{log_dir}/{self.today.strftime('%d_%m_%Y')}.log"

    def get_seconds_till_match(self) -> int:
        """Get the number of seconds till the match starts"""

        if self.debug:
            print("Debug mode is on: seconds till match is 1")
            return 1
        current_time = datetime.now()
        time_of_match = current_time.replace(day=current_time.day,
                                             hour=self.conf.hour,
                                             minute=self.conf.minute,
                                             second=self.conf.second,
                                             microsecond=self.conf.microsecond)
        delta_t = time_of_match - current_time
        seconds_till_match = delta_t.seconds + 1
        print(f"get_seconds_till_match()\nCurrent time is {current_time}\nTime of the match is {time_of_match}\nSeconds"
              f" till match: {seconds_till_match}")
        return seconds_till_match

    def get_capture(self) -> cv2.VideoCapture:
        """Check if the OS is using Windows or Linux and return the correct capture object"""
        return (
            cv2.VideoCapture(0)
            if os.name == 'nt'
            else cv2.VideoCapture(
                f'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=60/1 ! '
                f'nvvidconv ! video/x-raw, width={str(self.width)}, height={str(self.height)}, format=BGRx ! '
                f'videoconvert ! video/x-raw, format=BGR ! appsink'
            )
        )

    def create_video_writer(self, video_name: str) -> cv2.VideoWriter:
        """Create a video writer object"""
        return cv2.VideoWriter(video_name,
                               cv2.VideoWriter_fourcc(*'MJPG'),
                               5, self.frame_size)

    @staticmethod
    def create_datetime_video_name() -> str:
        """Create a video name with the current date and time"""
        now = datetime.now()
        return f"{now.strftime('time_%H_%M_%S_date_%d_%m_%Y_')}.avi"

    @staticmethod
    def initialize_fps_timers() -> Tuple[FPS, FPS, FPS, FPS]:
        """Initialize the FPS timers"""
        avg_fps = FPS()
        reading_fps = FPS()
        writing_fps = FPS()
        bohs_fps = FPS()
        return avg_fps, reading_fps, writing_fps, bohs_fps

    def get_timeout(self, timeout_minute_length: float = 22.5) -> int:
        """Return the time in seconds that the video should be recorded for (default is 22.5 minutes)"""
        if self.debug is True:
            return int(time.time() + 10)  # 10-second video if in debug mode
        else:
            return int(time.time() + (timeout_minute_length * 60))

    def get_video_path(self) -> str:
        """Return the path to save the video to (doesn't include name!)"""
        if os.name == 'nt':
            return "./videos/"
        elif self.debug is False:
            ip_address = get_ip_address()
            video_dir_path = f"../tim/bohsVids/{self.today.strftime('%m_%d_%Y@')}_{self.jetson_name}_{ip_address}"
            check_and_create_dir(video_dir_path)
            return video_dir_path
        else:
            return "../tim/bohsVids/test"

    def record_video(self, video_length_mins: float, video_path: str) -> None:
        """
        Record and save a video for as long as set in the timeout

        :param video_length_mins: The length of the video in minutes
        :param video_path: The path to save the video to (i.e. ./videos/) - does not include file name
        """
        cap = self.get_capture()

        video_name = self.create_datetime_video_name()
        video_path = os.path.join(video_path, video_name) # Join the path and the name together

        writer = self.create_video_writer(video_name=video_path)
        avg_fps, reading_fps, writing_fps, bohs_fps = self.initialize_fps_timers()
        frame_counter = 0
        timeout = self.get_timeout(video_length_mins)

        # Camera loop
        try:
            if cap.isOpened():
                while cap.isOpened():
                    # Read the next frame
                    reading_fps.start()
                    ret_val, img = cap.read()
                    reading_fps.stop()

                    # Resize the frame to (720, 1280)
                    img = cv2.resize(img, self.frame_size)

                    if not ret_val:
                        print("Not ret_val. Breaking!")
                        break

                    # Write the frame to the file
                    writing_fps.start()
                    writer.write(img)
                    writing_fps.stop()

                    frame_counter += 1

                    if time.time() > timeout:
                        print("Timeout reached. Breaking!")
                        raise KeyboardInterrupt

                    self.logger.log(
                        f"Reading FPS: {reading_fps.fps()} - Writing FPS: {writing_fps.fps()} - Frame: {frame_counter}"
                    )
            else:
                print("Camera not opened")
        except KeyboardInterrupt:
            print("KeyboardInterrupt")

        cap.release()
        writer.release()
        cv2.destroyAllWindows()
        print("Video saved to", video_name)

    @staticmethod
    def wait_for_match_to_start(seconds_till_match: int) -> bool:
        """Waits for the match to start"""
        time_till_match_starts = time.time() + seconds_till_match
        while time.time() < time_till_match_starts:
            print("waiting for match to start")
            time.sleep(1)
        return True

    def record_full_match_in_batches(self) -> None:
        """Records videos for the match. Four 22.5-minute long videos + one 10-minute long video for the halftime"""
        # Set our file directory
        path = self.get_video_path()
        check_and_create_dir(path)

        seconds_till_match = self.get_seconds_till_match()
        self.wait_for_match_to_start(seconds_till_match)  # Blocks until the match starts

        for i in range(5):
            if (i == 2) or (i > 5):
                self.record_video(video_length_mins=10, video_path=path)
            else:
                self.record_video(video_length_mins=22.5, video_path=path)


def main():
    video_recorder = VideoRecorder(debug=True)
    video_recorder.record_full_match_in_batches()


if __name__ == '__main__':
    main()