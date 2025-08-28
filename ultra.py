import RPi.GPIO as GPIO
import time

# Define GPIO mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)

# Set GPIO Pins
GPIO_TRIGGER = 27  # GPIO13 (Pin 13)
GPIO_ECHO = 17     # GPIO11 (Pin 11)

# Set direction of GPIO pins
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def measure_distance():
    # Set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # Set Trigger after 10µs to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()

    # Save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    # Save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # Time difference between start and arrival
    time_elapsed = stop_time - start_time

    # Multiply with the sonic speed (34300 cm/s) and divide by 2 (to and fro)
    distance = (time_elapsed * 34300) / 2

    return distance

try:
    while True:
        dist = measure_distance()
        print(f"Measured Distance = {dist:.2f} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nMeasurement stopped by User")
    GPIO.cleanup()
