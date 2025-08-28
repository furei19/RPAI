import RPi.GPIO as GPIO
import time

# Use BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
GPIO_TRIGGER = 27  # Trigger Pin (Pin 13)
GPIO_ECHO = 17     # Echo Pin (Pin 11)
GPIO_BUZZER = 22   # Buzzer Pin (Pin 15)

# Setup GPIO pins
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_BUZZER, GPIO.OUT)

def measure_distance():
    # Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()

    # Wait for echo to go high (start)
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    # Wait for echo to go low (end)
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # Calculate distance
    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2

    return distance

try:
    while True:
        distance = measure_distance()
        print(f"Measured Distance = {distance:.2f} cm")

        # If object is closer than 10 cm, trigger the buzzer
        if distance < 10:
            GPIO.output(GPIO_BUZZER, True)
        else:
            GPIO.output(GPIO_BUZZER, False)

        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram stopped by User")
    GPIO.cleanup()
