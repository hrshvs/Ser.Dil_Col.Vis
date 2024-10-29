import cv2
import numpy as np

# Known BGR values for multiple reference colors
ideal_colors = {
    "white": np.array([255, 255, 255]),
    "gray": np.array([127, 127, 127]),
    "red": np.array([0, 0, 255]),
    "green": np.array([0, 255, 0]),
    "blue": np.array([255, 0, 0]),
    # Add more colors if you have them available on your color card
}

# Placeholder for measured colors
measured_colors = {}

def capture_reference_colors(image, color_positions):
    # Capture each color's BGR value from the specified regions in `color_positions`
    for color, (x_start, y_start, x_end, y_end) in color_positions.items():
        roi = image[y_start:y_end, x_start:x_end]
        measured_colors[color] = roi.mean(axis=(0, 1))
    return measured_colors

def calculate_correction_factors(ideal_colors, measured_colors):
    # Calculate a correction factor per color and channel
    correction_factors = {}
    for color in ideal_colors:
        correction_factors[color] = ideal_colors[color] / measured_colors[color]
    return correction_factors

def apply_color_correction(pixel, correction_factors):
    # Calculate the closest correction factor based on the color of the pixel
    closest_color = min(correction_factors.keys(), key=lambda color: np.linalg.norm(pixel - measured_colors[color]))
    return (pixel * correction_factors[closest_color]).clip(0, 255)

# Set up video capture
cap = cv2.VideoCapture(0)

# Calibration step - capture an image of the reference card with color patches
ret, ref_image = cap.read()
if ret:
    # Define ROI coordinates for each color in the reference card (modify based on actual layout)
    color_positions = {
        "white": (50, 50, 100, 100),
        "gray": (150, 50, 200, 100),
        "red": (50, 150, 100, 200),
        "green": (150, 150, 200, 200),
        "blue": (50, 250, 100, 300),
    }
    
    # Capture measured colors
    measured_colors = capture_reference_colors(ref_image, color_positions)
    print(f"Measured Colors BGR: {measured_colors}")

    # Calculate correction factors for each color
    correction_factors = calculate_correction_factors(ideal_colors, measured_colors)
    print(f"Correction Factors: {correction_factors}")
else:
    print("Failed to capture reference image")

# Real-time tracking with color adjustment
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Apply per-pixel color correction using nearest correction factor
    corrected_frame = np.apply_along_axis(apply_color_correction, 2, frame, correction_factors).astype(np.uint8)

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
