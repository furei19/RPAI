import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

# Coin size range in pixels
MIN_AREA = 1000
MAX_AREA = 10000

# Detection status
red_detected = False
last_detection_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red HSV range
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Create mask and reduce noise
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = mask1 | mask2
    red_mask = cv2.GaussianBlur(red_mask, (5, 5), 0)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    # Find contours
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    found_red = False

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if MIN_AREA <= area <= MAX_AREA:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Red Coin-Sized Object", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            found_red = True
            break  # Only need one

    # Triggered detection logic
    if found_red and not red_detected:
        print("🔴 Coin-sized red object detected!")
        red_detected = True
        last_detection_time = time.time()

    # If no red detected for 1 second, reset state
    if red_detected and not found_red and (time.time() - last_detection_time) > 1:
        red_detected = False

    cv2.imshow("Webcam", frame)
    cv2.imshow("Red Mask", red_mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

