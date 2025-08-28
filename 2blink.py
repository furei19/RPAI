import RPi.GPIO as GPIO
import time

# light play - rhythm 

# Use BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

# Set GPIO 17 as output
GPIO.setup(17, GPIO.OUT)

def light(n):
    GPIO.output(17, GPIO.HIGH)
    time.sleep(n)
    GPIO.output(17, GPIO.LOW)
    time.sleep(n)

def lightOff(n):
    GPIO.output(17, GPIO.LOW)
    time.sleep(n)
    
#def lightDone():
    #GPIO.clean()
    

light(.5)
time.sleep(0.5)
for i in range(4):
    light(.3)
time.sleep(1)
light(.5)
light(.5)


