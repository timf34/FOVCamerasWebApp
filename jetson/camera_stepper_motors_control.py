import os
import requests
import sys
import time
from requests.exceptions import Timeout

from utils.utility_funcs import load_env

# Load environment variables
load_env()
URL = os.environ.get('REACT_APP_URL')

# Device ID as a command line argument
if len(sys.argv) != 2:
    print('Usage: python script.py <device_id>')
    sys.exit(1)

DEVICE_ID = sys.argv[1]
# DEVICE_ID = os.environ.get('DEVICE_NAME', "jetson1")


# Simulation flag
if os.name == 'nt':
    SIMULATION_MODE = True
else:
    SIMULATION_MODE = False

try:
    import Jetson.GPIO as GPIO
except ImportError:
    if not SIMULATION_MODE:
        raise


# Pin Definitions
F_STEP_PIN = 15
F_DIR_PIN = 12
F_SLEEP_PIN = 7

I_STEP_PIN = 37
I_DIR_PIN = 13
I_SLEEP_PIN = 35

Z_STEP_PIN = 21
Z_DIR_PIN = 23
Z_SLEEP_PIN = 19

SHDN = 16

# Motor Speeds  DO NOT EXCEED!
F_SPEED = 800
I_SPEED = 30
Z_SPEED = 800

# Function to simulate GPIO operations
def simulated_gpio_method(*args, **kwargs):
    # print(f"Simulated GPIO method called with args: {args} kwargs: {kwargs}")
    pass  # Do nothing


# If we're in simulation mode, replace the GPIO methods with our simulated method
if SIMULATION_MODE:
    GPIO = type('GPIO', (object,), {
        'setmode': simulated_gpio_method,
        'setup': simulated_gpio_method,
        'output': simulated_gpio_method,
        'cleanup': simulated_gpio_method,
        'BOARD': 'BOARD',
        'OUT': 'OUT',
        'HIGH': 'HIGH',
        'LOW': 'LOW'
    })


class Motor:
    def __init__(self, step_pin: int, dir_pin: int, sleep_pin: int, speed: int, shdn: int):
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.sleep_pin = sleep_pin
        self.speed = speed
        self.osition = 0
        self.shdn = shdn

    def rotate(self, steps, direction):
        # Set the motor direction
        GPIO.output(self.dir_pin, GPIO.HIGH if direction == "clockwise" else GPIO.LOW)

        # Activate sleep pin
        self._activate_sleep()

        # Rotate the motor
        if not SIMULATION_MODE:
            for i in range(1, steps + 1):
                effective_speed = self._calculate_speed(i)
                
                # Move motor
                self._move_motor(effective_speed)

        # Deactivate sleep pin
        self._deactivate_sleep()

    def _activate_sleep(self):
        GPIO.output(self.sleep_pin, GPIO.HIGH)
        GPIO.output(self.shdn, GPIO.HIGH)
        time.sleep(0.1)  # Delay before motor movement

    def _deactivate_sleep(self):
        GPIO.output(self.sleep_pin, GPIO.LOW)
        GPIO.output(self.shdn, GPIO.LOW)

    def _calculate_speed(self, step_number):
        if self.step_pin == I_STEP_PIN:
            return self.speed
        else:
            # Calculate acceleration
            acceleration_factor = min(step_number, 10)  # We only increment speed for the first 10 steps
            return self.speed * (acceleration_factor / 10)

    def _move_motor(self, effective_speed):
        GPIO.output(self.step_pin, GPIO.HIGH)
        time.sleep(1 / effective_speed)
        GPIO.output(self.step_pin, GPIO.LOW)
        time.sleep(1 / effective_speed)


    def move(self, target_position):
        steps = int(target_position - self.position)
        direction = "counter-clockwise" if steps > 0 else "clockwise"
        self.rotate(abs(steps), direction)
        self.position += steps


class MotorController:
    def __init__(self, f_motor, i_motor, z_motor, shdn):
        self.f_motor = f_motor
        self.i_motor = i_motor
        self.z_motor = z_motor
        self.shdn = shdn

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        pins = [self.f_motor.step_pin, self.f_motor.dir_pin, self.f_motor.sleep_pin,
                self.i_motor.step_pin, self.i_motor.dir_pin, self.i_motor.sleep_pin,
                self.z_motor.step_pin, self.z_motor.dir_pin, self.z_motor.sleep_pin]
        GPIO.setup(pins, GPIO.OUT)
        GPIO.setup(self.shdn, GPIO.OUT)

        # Pull sleep pins LOW at the start
        GPIO.output(pins[2::3], GPIO.LOW)
        GPIO.output(self.shdn, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()


class ServerRequest:
    @staticmethod
    def post(data):
        try:
            response = requests.post(f"{URL}/api/motor-positions", json=data, timeout=2)
            # Check the server's response
            if response.status_code != 200:
                raise ValueError(f"Error from server: {response.text}")
        except Timeout:
            print("Request timed out ")
        except Exception as e:
            print(f"Error in save_motor_positions: {e}")


class MotorPositionFile:
    def __init__(self, filename="motor_positions.txt"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                file.write("0,0,0")

    def load(self):
        try:
            with open(self.filename, "r") as file:
                positions = file.readline().strip().split(",")
                if len(positions) == 3:
                    return list(map(int, positions))
        except FileNotFoundError:
            pass
        return [0, 0, 0]

    def save(self, f_position, i_position, z_position):
        try:
            with open(self.filename, "w") as file:
                file.write(f"{f_position},{i_position},{z_position}")
            data = {
                "deviceId": DEVICE_ID,
                "f_position": f_position,
                "i_position": i_position,
                "z_position": z_position
            }
            print(f"Saving motor positions: {data}")
            ServerRequest.post(data)
        except Exception as e:
            print(f"Error in save_motor_positions: {e}")



# Main program
if __name__ == "__main__":
    try:
        # Setup GPIO
        motor_controller = MotorController(
            f_motor=Motor(F_STEP_PIN, F_DIR_PIN, F_SLEEP_PIN, F_SPEED, SHDN),
            i_motor=Motor(I_STEP_PIN, I_DIR_PIN, I_SLEEP_PIN, I_SPEED, SHDN),
            z_motor=Motor(Z_STEP_PIN, Z_DIR_PIN, Z_SLEEP_PIN, Z_SPEED, SHDN),
            shdn=SHDN
        )
        motor_controller.setup()

        # Load motor positions from the file
        positions_file = MotorPositionFile()
        f_position, i_position, z_position = positions_file.load()
        motor_controller.f_motor.position = f_position
        motor_controller.i_motor.position = i_position
        motor_controller.z_motor.position = z_position

        # Save motor positions on setup
        positions_file.save(f_position, i_position, z_position)

        # Main loop
        while True:
            print("F Motor Position:", motor_controller.f_motor.position)
            print("I Motor Position:", motor_controller.i_motor.position)
            print("Z Motor Position:", motor_controller.z_motor.position)
            print("F Motor %:", (motor_controller.z_motor.position / 69))  # Find out what the proper percentage ratio is here!
            print("I Motor %:", (i_position))
            print("Z Motor %:", (z_position))

            GPIO.output([motor_controller.f_motor.sleep_pin, motor_controller.i_motor.sleep_pin, motor_controller.z_motor.sleep_pin], GPIO.LOW)

            # Terminal input for motor coordinate and axis
            # Note: enter it in steps!
            print("Enter axis (f, i, z) and motor steps separated by a comma (i.e. f, 50); press q to quit:")
            motor_input = sys.stdin.readline().strip()

            if motor_input == "q":
                # Save motor positions before quitting
                positions_file.save(motor_controller.f_motor.position, motor_controller.i_motor.position, motor_controller.z_motor.position)
                break

            axis, target_coord = motor_input.split(',')
            target_position = int(target_coord)

            if axis == "f":
                motor_controller.f_motor.move(target_position)
            elif axis == "i":
                motor_controller.i_motor.move(target_position)
            elif axis == "z":
                motor_controller.z_motor.move(target_position)
            else:
                print("Invalid motor axis. Please try again.")

            positions_file.save(motor_controller.f_motor.position, motor_controller.i_motor.position, motor_controller.z_motor.position)
    finally:
        motor_controller.cleanup()
