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



from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

while True:
    # Grab the webcamera's image.
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window
    cv2.imshow("Webcam Image", image)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

   

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    class_name = class_name.strip()
    if class_name.lower() == "0 left hand" :
        move_forward()
    else:
        stop()
        
    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()


GPIO.cleanup()
