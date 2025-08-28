import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM)

# Define pins
GPIO_TRIGGER = 27
GPIO_ECHO = 17
MOTOR_FORWARD = 23
MOTOR_BACKWARD = 24

# Setup GPIO directions
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(MOTOR_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_BACKWARD, GPIO.OUT)

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
    GPIO.output(MOTOR_FORWARD, True)
    GPIO.output(MOTOR_BACKWARD, False)
    print("Moving Forward")

def move_backward():
    GPIO.output(MOTOR_FORWARD, False)
    GPIO.output(MOTOR_BACKWARD, True)
    print("Moving Backward")

def stop():
    GPIO.output(MOTOR_FORWARD, False)
    GPIO.output(MOTOR_BACKWARD, False)
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
