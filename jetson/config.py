"""
A config file to help speed up match day work.
For storing the time of the match + IP addresses too potentially.
"""
import os
import socket


class AFLConfig:
    def __init__(self):

        if os.name == 'nt':
            self.jetson_name: str = "jetson1"  # If we're on windows, just assume we're on jetson1
        else:
            self.jetson_name: str = os.environ.get('DEVICE_NAME', socket.gethostname().lower())

        self.jetson_number: str = self.jetson_name[-1]
        self.hour: int = 16
        self.minute: int = 30
        self.second: int = 2
        self.microsecond: int = 1

        assert 0 <= self.hour <= 23, "Hour must be between 0 and 23"
        assert isinstance(self.hour, int), "Hour must be an int"
        assert 0 <= self.minute <= 59 and isinstance(self.minute, int), "Minute must be between 0 and 59"
        assert isinstance(self.minute, int), "Minute must be an int"
        assert 0 <= self.second <= 59, "Second must be between 0 and 59"
        assert isinstance(self.second, int), "Second must be an int"
        assert isinstance(self.microsecond, int), "Microsecond must be an int"

    def __str__(self):
        return f"hour: {self.hour}, minute: {self.minute}, second: {self.second}, microsecond: {self.microsecond}"


def _test():
    x = BohsConfig()
    print(x)
    print(x.hour)


if __name__ == "__main__":
    _test()