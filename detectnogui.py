import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

# Area range for iPhone-sized red object in pixels (adjust if needed)
MIN_AREA = 20000
MAX_AREA = 80000

# Detection tracking
red_detected = False
last_detection_time = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Red HSV ranges
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        # Combine red masks
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = mask1 | mask2

        # Clean noise
        red_mask = cv2.GaussianBlur(red_mask, (5, 5), 0)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

        # Find contours
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        found_red = False

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if MIN_AREA <= area <= MAX_AREA:
                found_red = True
                break

        # Event-driven printing
        if found_red and not red_detected:
            print("🔴 iPhone-sized red object detected!")
            red_detected = True
            last_detection_time = time.time()

        elif not found_red and red_detected:
            if (time.time() - last_detection_time) > 1:
                print("🟢 Image is clear.")
                red_detected = False

        time.sleep(0.05)  # Slight delay to reduce CPU usage

except KeyboardInterrupt:
    print("🛑 Detection stopped by user.")

finally:
    cap.release()

