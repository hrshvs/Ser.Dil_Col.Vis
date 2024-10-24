import cv2
import numpy as np

cap = cv2.VideoCapture(0)

mincol = np.array([200,200,0], ndmin=3)
maxcol = np.array([255,255,0], ndmin=3)

while cap.isOpened:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mask = cv2.inRange(rgb_frame, mincol, maxcol)
    oframe = cv2.bitwise_and(frame, frame, mask = mask)

    cv2.imshow('color', oframe)
    if cv2.waitKey(5) & 0xFF == 27:  # Exit on 'Esc' key
        break




# if cv2.waitKey(5) & 0xFF == 27:
cap.release()
cv2.destroyAllWindows()
