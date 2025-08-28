import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

# Area range for iPhone-sized object (adjust based on actual tests)
MIN_AREA = 20000
MAX_AREA = 80000

# Detection state tracking
red_detected = False
last_detection_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define red color range
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Create and clean mask
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = mask1 | mask2
    red_mask = cv2.GaussianBlur(red_mask, (5, 5), 0)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    found_red = False

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if MIN_AREA <= area <= MAX_AREA:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, "Red iPhone-Sized Object", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            found_red = True
            break

    if found_red and not red_detected:
        print("🔴 Red ed object detected!")
        red_detected = True
        last_detection_time = time.time()

    elif not found_red and red_detected:
        # Object just disappeared
        if (time.time() - last_detection_time) > 1:
            print("🟢 Image is clear.")
            red_detected = False

    elif not found_red and not red_detected:
        # Nothing detected, already in "clear" state
        pass

    cv2.imshow("Webcam", frame)
    cv2.imshow("Red Mask", red_mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

