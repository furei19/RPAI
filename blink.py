import RPi.GPIO as GPIO
import time


# Use BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)
# Set GPIO 17 as output
GPIO.setup(17, GPIO.OUT)

try:
    while True:
        GPIO.output(17, GPIO.HIGH)  # LED on
        time.sleep(1)               # wait 1 second
        GPIO.output(17, GPIO.LOW)   # LED off
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting program...")

finally:
    GPIO.cleanup()
