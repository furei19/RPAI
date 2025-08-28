import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM)

# Define pins
GPIO_TRIGGER = 27
GPIO_ECHO = 17

WHITE = 22
RED = 23

MOTOR_FORWARD = 23
MOTOR_BACKWARD = 24

LEFT_IN1 = 6
LEFT_IN2 = 5
RIGHT_IN3 = 16
RIGHT_IN4 = 26

# Setup GPIO directions
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(MOTOR_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_BACKWARD, GPIO.OUT)

GPIO.setup(WHITE, GPIO.OUT)
GPIO.setup(RED, GPIO.OUT)

GPIO.setup(LEFT_IN1, GPIO.OUT)
GPIO.setup(LEFT_IN2, GPIO.OUT)
GPIO.setup(RIGHT_IN3, GPIO.OUT)
GPIO.setup(RIGHT_IN4, GPIO.OUT)


def measure_distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2
    return distance

def move_forward():
    GPIO.output(LEFT_IN1, GPIO.HIGH)
    GPIO.output(LEFT_IN2, GPIO.LOW)
    GPIO.output(RIGHT_IN3, GPIO.HIGH)
    GPIO.output(RIGHT_IN4, GPIO.LOW)
    GPIO.output(WHITE, GPIO.HIGH)
    GPIO.output(RED, GPIO.LOW)
    
    #GPIO.output(MOTOR_FORWARD, True)
    #GPIO.output(MOTOR_BACKWARD, False)
    print("Moving Forward")
    time.sleep(2)
    stop()

def move_backward():
    GPIO.output(LEFT_IN1, GPIO.LOW)
    GPIO.output(LEFT_IN2, GPIO.HIGH)
    GPIO.output(RIGHT_IN3, GPIO.LOW)
    GPIO.output(RIGHT_IN4, GPIO.HIGH)

    #GPIO.output(MOTOR_FORWARD, False)
    #GPIO.output(MOTOR_BACKWARD, True)
    print("Moving Backward")
    time.sleep(2)
    stop()

def stop():
    #GPIO.output(MOTOR_FORWARD, False)
    #GPIO.output(MOTOR_BACKWARD, False)
    GPIO.output(LEFT_IN1, GPIO.LOW)
    GPIO.output(LEFT_IN2, GPIO.LOW)
    GPIO.output(RIGHT_IN3, GPIO.LOW)
    GPIO.output(RIGHT_IN4, GPIO.LOW)
    GPIO.output(WHITE, GPIO.LOW)
    GPIO.output(RED, GPIO.HIGH)
    print("Stopped")

try:
    while True:
        dist = measure_distance()
        print(f"Distance: {dist:.2f} cm")

        if dist > 20:
            move_forward()
        elif dist < 10:
            move_backward()
        else:
            stop()

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Program stopped")
    GPIO.cleanup()
