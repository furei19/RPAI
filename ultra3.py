import RPi.GPIO as GPIO
import time

# GPIO setup
GPIO.setmode(GPIO.BCM)

# Define pins
GPIO_TRIGGER = 27  # Trigger Pin (Pin 13)
GPIO_ECHO = 17     # Echo Pin (Pin 11)
GPIO_BUZZER = 22   # Buzzer control (simulating VCC)

# Setup GPIO pins
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_BUZZER, GPIO.OUT)

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

try:
    while True:
        distance = measure_distance()
        print(f"Distance: {distance:.2f} cm")

        # Turn buzzer ON if object is near (e.g. < 10 cm)
        if distance < 10:
            GPIO.output(GPIO_BUZZER, GPIO.HIGH)
        else:
            GPIO.output(GPIO_BUZZER, GPIO.LOW)

        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopped by User")
    GPIO.cleanup()
