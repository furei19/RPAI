import RPi.GPIO as GPIO
import time

# Use BCM pin numbering
GPIO.setmode(GPIO.BCM)

# Motor pins
LEFT_IN1 = 6
LEFT_IN2 = 5
RIGHT_IN3 =16
RIGHT_IN4 = 26

# Set pins as output
GPIO.setup(LEFT_IN1, GPIO.OUT)
GPIO.setup(LEFT_IN2, GPIO.OUT)
GPIO.setup(RIGHT_IN3, GPIO.OUT)
GPIO.setup(RIGHT_IN4, GPIO.OUT)

# Function to move forward
def forward(duration):
    GPIO.output(LEFT_IN1, GPIO.HIGH)
    GPIO.output(LEFT_IN2, GPIO.LOW)
    GPIO.output(RIGHT_IN3, GPIO.HIGH)
    GPIO.output(RIGHT_IN4, GPIO.LOW)
    time.sleep(duration)
    stop()

# Function to move backward
def backward(duration):
    GPIO.output(LEFT_IN1, GPIO.LOW)
    GPIO.output(LEFT_IN2, GPIO.HIGH)
    GPIO.output(RIGHT_IN3, GPIO.LOW)
    GPIO.output(RIGHT_IN4, GPIO.HIGH)
    time.sleep(duration)
    stop()



# Function to turn left
def turn_left(duration):
    GPIO.output(LEFT_IN1, GPIO.LOW)
    GPIO.output(LEFT_IN2, GPIO.HIGH)
    GPIO.output(RIGHT_IN3, GPIO.HIGH)
    GPIO.output(RIGHT_IN4, GPIO.LOW)
    time.sleep(duration)
    stop()

# Function to turn right
def turn_right(duration):
    GPIO.output(LEFT_IN1, GPIO.HIGH)
    GPIO.output(LEFT_IN2, GPIO.LOW)
    GPIO.output(RIGHT_IN3, GPIO.LOW)
    GPIO.output(RIGHT_IN4, GPIO.HIGH)
    time.sleep(duration)
    stop()

# Function to stop motors
def stop():
    GPIO.output(LEFT_IN1, GPIO.LOW)
    GPIO.output(LEFT_IN2, GPIO.LOW)
    GPIO.output(RIGHT_IN3, GPIO.LOW)
    GPIO.output(RIGHT_IN4, GPIO.LOW)

# Main program
try:
    stop()
    while True:
        command = input("Enter command (f=forward, b=backward, l=left, r=right, s=stop, q=quit): ").lower()
        if command == 'f':
            forward(1)
        elif command == 'b':
            backward(1)
        elif command == 'l':
            turn_left(1)
        elif command == 'r':
            turn_right(1)
        elif command == 's':
            stop()
        elif command == 'q':
            break
        else:
            print("Invalid command!")

finally:
    GPIO.cleanup()
