import cv2
print ("ok cv2")
import numpy as np
print ("ok numpy")
import tensorflow as tf
print ("ok tensorflow")

# Load the trained model
model = tf.keras.models.load_model('keras_model.h5')

# Load labels
with open('labels.txt', 'r') as f:
    labels = [line.strip() for line in f.readlines()]

print ("About to start...")

# Webcam setup
cap = cv2.VideoCapture(0)

# Set image size (depending on your model's input)
img_size = (224, 224)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess image
    img = cv2.resize(frame, img_size)
    img = np.asarray(img, dtype=np.float32).reshape(1, *img_size, 3)
    img = (img / 127.5) - 1  # Normalize to [-1, 1] if required

    # Make prediction
    prediction = model.predict(img)
    class_index = np.argmax(prediction)
    confidence = prediction[0][class_index]
    label = labels[class_index]

    # Display result
    cv2.putText(frame, f"{label}: {confidence:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Hand Detection', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()

