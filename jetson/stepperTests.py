# TODO: this file needs refactoring. At least add some typing. S

import os
import requests
import sys
import time

# Simulation flag
SIMULATION_MODE = True

try:
    import Jetson.GPIO as GPIO
except ImportError:
    if not SIMULATION_MODE:
        raise

# Function to simulate GPIO operations
def simulated_gpio_method(*args, **kwargs):
    # print(f"Simulated GPIO method called with args: {args} kwargs: {kwargs}")
    pass # Do nothing

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


# Pin Definitions
# Define the GPIO pins for the stepper motors
# Update these pin numbers based on your wiring
F_STEP_PIN = 15
F_DIR_PIN = 12
F_SLEEP_PIN = 7

I_STEP_PIN = 35
I_DIR_PIN = 33
I_SLEEP_PIN = 37

Z_STEP_PIN = 21
Z_DIR_PIN = 19
Z_SLEEP_PIN = 23

IRH = 13
IRL = 15
h = 1

# Motor Speeds  DO NOT EXCEED! 
F_SPEED = 3200
I_SPEED = 80
Z_SPEED = 3200

# File name to store the motor positions
POSITIONS_FILE = "motor_positions.txt"

# Create the positions file if it doesn't exist
if not os.path.exists(POSITIONS_FILE):
    with open(POSITIONS_FILE, "w") as file:
        file.write("0,0,0")

# TODO: add error handling here!
with open('ip_address.txt', 'r') as file:
    ip_address = file.read().strip()

# Setup GPIO
def setup_gpio():
    GPIO.setmode(GPIO.BOARD)
    pins = [F_STEP_PIN, F_DIR_PIN, F_SLEEP_PIN,
            I_STEP_PIN, I_DIR_PIN, I_SLEEP_PIN,
            Z_STEP_PIN, Z_DIR_PIN, Z_SLEEP_PIN]
    GPIO.setup(pins + [IRH, IRL], GPIO.OUT)

    # Pull sleep pins LOW at the start
    GPIO.output(pins[2::3], GPIO.LOW)

# Cleanup GPIO
def cleanup_gpio():
    GPIO.cleanup()

# Function to rotate a motor
def rotate_motor(step_pin, dir_pin, sleep_pin, steps, direction, speed):
    # Set the motor direction
    GPIO.output(dir_pin, GPIO.HIGH if direction == "clockwise" else GPIO.LOW)

    # Activate sleep pin
    GPIO.output(sleep_pin, GPIO.HIGH)
    time.sleep(0.1)  # Delay before motor movement

    # Rotate the motor
    if not SIMULATION_MODE:
        for i in range(steps):
            GPIO.output(step_pin, GPIO.HIGH)
            time.sleep(1 / speed)
            GPIO.output(step_pin, GPIO.LOW)
            time.sleep(1 / speed)

    print("End rotation") # Debug print

    # Deactivate sleep pin
    GPIO.output(sleep_pin, GPIO.LOW)


# Function to move a motor
def move_motor(step_pin, dir_pin, sleep_pin, position, conversion_factor, limit, speed):
    steps = int(conversion_factor * limit / 100) - position
    direction = "counter-clockwise" if steps > 0 else "clockwise"
    rotate_motor(step_pin, dir_pin, sleep_pin, abs(steps), direction, speed)

    return position + steps

# Function to load the motor positions from a file
def load_motor_positions():
    try:
        with open(POSITIONS_FILE, "r") as file:
            positions = file.readline().strip().split(",")
            if len(positions) == 3:
                return list(map(int, positions))
    except FileNotFoundError:
        pass

    # If the file doesn't exist or the positions couldn't be loaded, return default positions
    return [0, 0, 0]

# Function to save the motor positions to a file
def save_motor_positions(f_position, i_position, z_position):
    try:
        with open(POSITIONS_FILE, "w") as file:
            file.write(f"{f_position},{i_position},{z_position}")

        # Prepare data to be sent
        data = {
            "deviceId": "jetson1",
            "f_position": f_position,
            "i_position": i_position,
            "z_position": z_position
        }

        # Send a POST request to the server
        # response = requests.post(f"http://{ip_address}:5000/api/motor-positions", json=data)  
        response = requests.post(f"http://fovcameraswebappv2.eu-west-1.elasticbeanstalk.com/api/motor-positions", json=data)
        # Print the server's response (for debugging purposes)
        print(response.text)

        # Check the server's response
        if response.status_code != 200:
            raise ValueError(f"Error from server: {response.text}")

    except Exception as e:
        print(f"Error in save_motor_positions: {e}")


# Main program
if __name__ == "__main__":
    setup_gpio()

    # Load motor positions from the file
    f_position, i_position, z_position = load_motor_positions()

    while True:
        print("F Motor Position:", f_position)
        print("I Motor Position:", i_position)
        print("Z Motor Position:", z_position)
        print("F Motor %:", (f_position / (9354 * 4)) * 100)
        print("I Motor %:", (i_position / (75 * 4)) * 100)
        print("Z Motor %:", (z_position / (4073 * 4)) * 100)

        GPIO.output([F_SLEEP_PIN, I_SLEEP_PIN, Z_SLEEP_PIN], GPIO.LOW)

        # Terminal input for motor coordinate and axis
        motor_input = sys.stdin.readline().strip()

        if motor_input == "q":
            # Save motor positions before quitting
            save_motor_positions(f_position, i_position, z_position)
            break

        axis, target_coord = motor_input.split(',')
        target_position = int(target_coord)

        if axis == "f":
            f_position = move_motor(F_STEP_PIN, F_DIR_PIN, F_SLEEP_PIN, f_position, target_position, 9354 * 4, F_SPEED)
            save_motor_positions(f_position, i_position, z_position)
        elif axis == "i":
            i_position = move_motor(I_STEP_PIN, I_DIR_PIN, I_SLEEP_PIN, i_position, target_position, 75 * 4, I_SPEED)
            save_motor_positions(f_position, i_position, z_position)
        elif axis == "z":
            z_position = move_motor(Z_STEP_PIN, Z_DIR_PIN, Z_SLEEP_PIN, z_position, target_position, 4073 * 4, Z_SPEED)
            save_motor_positions(f_position, i_position, z_position)
        else:
            print("Invalid motor axis. Please try again.")

    cleanup_gpio()
