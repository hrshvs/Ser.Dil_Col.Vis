import cv2
import numpy as np

# Known BGR values for reference colors (example: white, gray, etc.)
ideal_colors = {
    "white": np.array([255, 255, 255]),
}

# Placeholder for calculated correction offsets
correction_offsets = np.array([0.0, 0.0, 0.0])

def capture_reference_color(image):
    # Set ROI to capture reference color (adjust for your reference object)
    x_start, y_start, x_end, y_end = 100, 100, 200, 200
    roi = image[y_start:y_end, x_start:x_end]
    
    # Calculate average BGR in the reference area
    avg_bgr = roi.mean(axis=(0, 1))
    return avg_bgr

def calculate_correction_offsets(avg_bgr, ideal_bgr):
    # Calculate the offset for each BGR channel
    offsets = ideal_bgr - avg_bgr
    return offsets

# Set up video capture
cap = cv2.VideoCapture(0)

# Calibration step - capture an image of the reference card
ret, ref_image = cap.read()
if ret:
    # Capture reference color
    measured_bgr = capture_reference_color(ref_image)
    print(f"Measured BGR for reference: {measured_bgr}")

    # Calculate correction offsets
    correction_offsets = calculate_correction_offsets(measured_bgr, ideal_colors["white"])
    print(f"Correction offsets: {correction_offsets}")
else:
    print("Failed to capture reference image")

# Real-time tracking with color adjustment
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Apply correction to each pixel by adding offset
    corrected_frame = frame + correction_offsets
    corrected_frame = np.clip(corrected_frame, 0, 255).astype(np.uint8)

    # Define the 33% ROI (bottom right area)
    height, width, _ = frame.shape
    x_start = width // 2
    y_start = height // 2
    x_end = width
    y_end = int(height * (1.5 / 3))

    # Extract ROI and calculate corrected average BGR
    roi = corrected_frame[y_start:y_end, x_start:x_end]
    avg_bgr = roi.mean(axis=(0, 1))

    # Display corrected frame with ROI and average BGR
    cv2.rectangle(corrected_frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
    cv2.putText(corrected_frame, f"Avg BGR: {avg_bgr}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.imshow("Corrected Camera Feed", corrected_frame)

    # Display average BGR values in the console
    print(f"Adjusted Average BGR in ROI: {avg_bgr}")

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release and cleanup
cap.release()
cv2.destroyAllWindows()
