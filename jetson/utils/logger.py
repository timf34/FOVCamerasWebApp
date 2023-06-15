import os
import datetime

from typing import List


class Logger:
    """
    A class for logging messages to a file on disk and/or to the console. This version
    of the logger uses a buffer to collect log messages before writing them to disk,
    which can help reduce the number of writes and improve performance. Messages can
    also be printed to the console using a separate buffer to minimize the impact on
    performance.

    Args:
        log_file_path (str): The path to the log file.
        buffer_size (int, optional): The maximum number of log messages to buffer before
            writing them to disk. Defaults to 100.
        print_to_console (bool, optional): Whether to print log messages to the console.
            Defaults to False.
        console_buffer_size (int, optional): The maximum number of log messages to buffer
            before printing them to the console. Only used if `print_to_console` is True.
            Defaults to 10.
    """
    def __init__(
            self,
            log_file_path: str,
            buffer_size: int = 100,
            print_to_console: bool = True,
            console_buffer_size: int = 10
    ):
        self.log_file_path: str = log_file_path
        print(f"Log file path: {self.log_file_path}")
        self.log_file = None
        self.buffer: List[str] = []
        self.buffer_size: int = buffer_size
        self.print_to_console: bool = print_to_console
        self.console_buffer: List[str] = []
        self.console_buffer_size: int = console_buffer_size

        self.create_log_file()

    def create_log_file(self) -> None:
        os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)
        with open(self.log_file_path, "a") as log_file:
            log_file.write(f"Created log file at {self.log_file_path}\n")

    def log(self, message: str) -> None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_message = f"{timestamp}: {message}\n"

        self.buffer.append(log_message)

        if len(self.buffer) >= self.buffer_size:
            self.flush_buffer()

        if self.print_to_console:
            self.console_buffer.append(log_message)
            if len(self.console_buffer) >= self.console_buffer_size:
                self.flush_console_buffer()

    def flush_buffer(self) -> None:
        with open(self.log_file_path, "a") as log_file:
            log_file.writelines(self.buffer)
            log_file.flush()
        self.buffer.clear()

    def flush_console_buffer(self):
        console_message = "".join(self.console_buffer)
        print(console_message, end="")
        self.console_buffer.clear()

    def __del__(self):
        # If the file is open, flush the buffer and close it when the object is deleted
        if self.log_file:
            self.flush_buffer()
            self.log_file.close()

        # If there are any remaining log messages in the console buffer, print them
        if self.console_buffer:
            self.flush_console_buffer()


def main():
    import time

    logger = Logger("../../../../PycharmProjects/jetson_camera_code/test.log", buffer_size=10)

    for i in range(100):
        logger.log(f"Test message {i}")
        time.sleep(0.1)

    logger.flush_buffer()
    print("Done")


if __name__ == "__main__":
    main()
