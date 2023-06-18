import Jetson.GPIO as GPIO
import time

# Pin Definitions
# Define the GPIO pins for the stepper motors
# Update these pin numbers based on your wiring
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

# Motor Speeds (in steps per second)
F_SPEED = 800
I_SPEED = 90
Z_SPEED = 800
# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(F_STEP_PIN, GPIO.OUT)
GPIO.setup(F_DIR_PIN, GPIO.OUT)
GPIO.setup(F_SLEEP_PIN, GPIO.OUT)
GPIO.setup(I_STEP_PIN, GPIO.OUT)
GPIO.setup(I_DIR_PIN, GPIO.OUT)
GPIO.setup(I_SLEEP_PIN, GPIO.OUT)
GPIO.setup(Z_STEP_PIN, GPIO.OUT)
GPIO.setup(Z_DIR_PIN, GPIO.OUT)
GPIO.setup(Z_SLEEP_PIN, GPIO.OUT)
GPIO.setup(SHDN, GPIO.OUT)

# Pull sleep pins LOW at the start
GPIO.output(F_SLEEP_PIN, GPIO.LOW)
GPIO.output(I_SLEEP_PIN, GPIO.LOW)
GPIO.output(Z_SLEEP_PIN, GPIO.LOW)
GPIO.output(SHDN, GPIO. LOW)

# Motor Positions
F_POSITION = 0
I_POSITION = 0
Z_POSITION = 0


# Function to rotate a motor
def rotate_motor(step_pin, dir_pin, sleep_pin, steps, direction, speed):
    # Set the motor direction
    if direction == "clockwise":
        GPIO.output(dir_pin, GPIO.HIGH)
    elif direction == "counter-clockwise":
        GPIO.output(dir_pin, GPIO.LOW)

    # Activate sleep pin
    GPIO.output(SHDN, GPIO.HIGH)
    GPIO.output(sleep_pin, GPIO.HIGH)
    time.sleep(0.1)  # Delay before motor movement

    # Rotate the motor
    for _ in range(steps):
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(1 / speed)
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(1 / speed)

    # Deactivate sleep pin
    GPIO.output(sleep_pin, GPIO.LOW)
    GPIO.output(SHDN, GPIO.LOW)


# Function to move F motor
def move_F_motor(target_position):
    global F_POSITION
    steps = target_position - F_POSITION
    direction = "clockwise" if steps >= 0 else "counter-clockwise"
    rotate_motor(F_STEP_PIN, F_DIR_PIN, F_SLEEP_PIN, abs(steps), direction, F_SPEED)
    F_POSITION = target_position


# Function to move I motor
def move_I_motor(target_position):
    global I_POSITION
    steps = target_position - I_POSITION
    direction = "clockwise" if steps >= 0 else "counter-clockwise"
    rotate_motor(I_STEP_PIN, I_DIR_PIN, I_SLEEP_PIN, abs(steps), direction, I_SPEED)
    I_POSITION = target_position


# Function to move Z motor
def move_Z_motor(target_position):
    global Z_POSITION
    steps = target_position - Z_POSITION
    direction = "clockwise" if steps >= 0 else "counter-clockwise"
    rotate_motor(Z_STEP_PIN, Z_DIR_PIN, Z_SLEEP_PIN, abs(steps), direction, Z_SPEED)
    Z_POSITION = target_position


# Main program
if __name__ == "__main__":
    while True:
        # Pull sleep pins LOW at the start of each iteration
        GPIO.output(F_SLEEP_PIN, GPIO.LOW)
        GPIO.output(I_SLEEP_PIN, GPIO.LOW)
        GPIO.output(Z_SLEEP_PIN, GPIO.LOW)

        # Terminal input for motor coordinate and axis
        motor_input = input("Enter the motor axis (F, I, Z) and target coordinate or 'q' to quit: ")

        if motor_input == "q":
            break

        # Parse the motor axis and target coordinate
        axis, target_coord = motor_input.split(',')
        target_position = int(target_coord)

        # Move the specified motor
        if axis == "f":
            move_F_motor(target_position)
        elif axis == "i":
            move_I_motor(target_position)
        elif axis == "z":
            move_Z_motor(target_position)
        else:
            print("Invalid motor axis. Please try again.")

        # Print motor positions
        print("F Motor Position:", F_POSITION)
        print("I Motor Position:", I_POSITION)
        print("Z Motor Position:", Z_POSITION)

    # Cleanup GPIO
    GPIO.cleanup()
