import cv2
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp
import sys

# Define start and end percentages
Start_y = 30
End_y = 60
Start_x = 20
End_x = 80
assert Start_y in range(101) and End_y in range(101) and Start_y < End_y
assert Start_x in range(101) and End_x in range(101) and Start_x < End_x


def capture(array, terminate, *, xrange=(0, 100), yrange=(0, 100)):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        sys.exit(1)

    while cap.isOpened() and terminate.value == 0:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale and flip the frame
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flipped_frame = cv2.flip(gray_frame, 1)

        # Update sections
        sections(array, flipped_frame, xrange, yrange)

        # Display the frame with drawn lines
        cv2.imshow("Camera", flipped_frame)

        # Exit when 'ESC' is pressed
        if cv2.waitKey(5) & 0xFF == 27:
            terminate.value = 1
            break

    cap.release()
    cv2.destroyAllWindows()


def sections(array, frame, xrange, yrange):
    start_x, end_x = xrange
    start_y, end_y = yrange
    h, w = frame.shape[:2]

    # Convert percentage ranges to pixel coordinates
    start_ypixel = int(np.floor(start_y * h / 100))
    end_ypixel = int(np.floor(end_y * h / 100))
    start_xpixel = int(np.floor(start_x * w / 100))
    end_xpixel = int(np.floor(end_x * w / 100))

    # Draw bounding box for the region
    cv2.line(frame, (start_xpixel, start_ypixel), (end_xpixel, start_ypixel), (0, 255, 0), 1)
    cv2.line(frame, (start_xpixel, end_ypixel), (end_xpixel, end_ypixel), (0, 255, 0), 1)
    cv2.line(frame, (start_xpixel, start_ypixel), (start_xpixel, end_ypixel), (0, 255, 0), 1)
    cv2.line(frame, (end_xpixel, start_ypixel), (end_xpixel, end_ypixel), (0, 255, 0), 1)

    # Compute intensity array for the specified region
    intensity_array = [0] * w
    for i in range(start_xpixel, end_xpixel):
        column_values = frame[start_ypixel:end_ypixel, i]
        intensity_array[i] = np.mean(column_values)

    # Update shared memory array
    for i in range(len(intensity_array)):
        array[i] = intensity_array[i]


def plot(array, terminate):
    # Initialize plot
    plt.figure(figsize=(6, 4))
    plt.ion()
    ax = plt.subplot(111)
    line, = ax.plot([], [], 'k-', label="Pixel vs Intensity")
    ax.set_xlim(0, 640)  # Pixel range
    ax.set_ylim(0, 255)  # Intensity range
    ax.set_title("Dynamic Plot")
    ax.set_xlabel("Pixel Number")
    ax.set_ylabel("Intensity")
    ax.legend()

    # Dynamic update loop
    while terminate.value == 0:
        x = np.arange(len(array))
        line.set_data(x, list(array))
        plt.draw()
        plt.pause(0.1)

    plt.ioff()
    plt.close('all')


if __name__ == '__main__':
    # Shared values and array
    array = mp.Array('d', 640)
    terminate = mp.Value('i', 0)

    # Create processes for capturing and plotting
    p1 = mp.Process(target=capture, args=(array, terminate), kwargs={"xrange": (Start_x, End_x), "yrange": (Start_y, End_y)})
    p2 = mp.Process(target=plot, args=(array, terminate))

    # Start and join processes
    p1.start()
    p2.start()

    p1.join()
    p2.join()
