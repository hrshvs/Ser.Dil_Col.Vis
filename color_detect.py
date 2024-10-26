import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# [0-180, 0-255, 0-255]
mincol = np.array([0,100,00], ndmin=3)
maxcol = np.array([180,255,150], ndmin=3)

while cap.isOpened:
    ret, frame = cap.read()
    if not ret:
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, mincol, maxcol)
    # oframe = cv2.bitwise_and(frame, frame, mask = mask)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw rectangles around detected contours
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Filter out small contours
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    fframe=cv2.flip(frame, 1)
    cv2.imshow('color', fframe)
    if cv2.waitKey(5) & 0xFF == 27:  # Exit on 'Esc' key
        break




# if cv2.waitKey(5) & 0xFF == 27:
cap.release()
cv2.destroyAllWindows()
