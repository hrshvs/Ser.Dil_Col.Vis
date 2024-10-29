import cv2
import numpy as np

# Set up video capture from the default camera
cap = cv2.VideoCapture(0)

while True:
    # Read frame from the camera
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to capture image")
        break

    # Get the dimensions of the frame
    height, width, _ = frame.shape

    # Define the area representing 33% of the frame (bottom right area here)
    # You can adjust the coordinates depending on which part of the frame you want to track
    x_start = width // 2
    y_start = height // 2
    x_end = width
    y_end = int(height * (1.5 / 3))  # This will give 1/3rd of height

    # Extract the region of interest (ROI)
    roi = frame[y_start:y_end, x_start:x_end]

    # Calculate the average BGR values
    avg_bgr = roi.mean(axis=(0, 1))

    # Display the original frame with the ROI highlighted
    cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
    cv2.putText(frame, f"Avg BGR: {avg_bgr}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Camera Feed", frame)

    # Display the average BGR values in the console
    print(f"Average BGR in ROI: {avg_bgr}")

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
