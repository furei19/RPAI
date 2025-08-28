import RPi.GPIO as GPIO
import time

speed = .1

# Use BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)
# Set GPIO 17 as output
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

try:
    while True:
        GPIO.output(17, GPIO.HIGH)  # LED on
        time.sleep(speed)               # wait 1 second
        GPIO.output(17, GPIO.LOW)   # LED off
        time.sleep(speed)
        
        GPIO.output(27, GPIO.HIGH)  # LED on
        time.sleep(speed)               # wait 1 second
        GPIO.output(27, GPIO.LOW)   # LED off
        time.sleep(speed)
        
        GPIO.output(22, GPIO.HIGH)  # LED on
        time.sleep(speed)               # wait 1 second
        GPIO.output(22, GPIO.LOW)   # LED off
        time.sleep(speed)
except KeyboardInterrupt:
    print("Exiting program...")

finally:
    GPIO.cleanup()

