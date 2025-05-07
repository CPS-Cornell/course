import cv2
import numpy as np

# Callback function for trackbar (does nothing, we read value in loop)
def nothing(x):
    pass

# Initialize video capture from the default webcam (index 0)
cap = cv2.VideoCapture(0)

# Check if the webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Create a named window
window_name = 'Original | Corner Detection' # Changed window name
cv2.namedWindow(window_name)

# Create trackbars for goodFeaturesToTrack parameters
# Max corners: 1 to 100, initial 25
cv2.createTrackbar('Max Corners', window_name, 25, 100, nothing)
# Quality level: 1 to 100 (representing 0.01 to 1.0), initial 10 (0.1)
cv2.createTrackbar('Quality Level', window_name, 10, 100, nothing)
# Min distance: 1 to 100, initial 10
cv2.createTrackbar('Min Distance', window_name, 10, 100, nothing)


print("Press 'q' to quit.")

# Loop to continuously get frames from the webcam
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # If frame reading was not successful, break the loop
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        break

    # Get current trackbar positions for goodFeaturesToTrack
    max_corners = cv2.getTrackbarPos('Max Corners', window_name)
    # Ensure max_corners is at least 1
    if max_corners < 1:
        max_corners = 1
    quality_level_raw = cv2.getTrackbarPos('Quality Level', window_name)
    # Convert quality level from 1-100 to 0.01-1.0
    quality_level = quality_level_raw / 100.0
    # Ensure quality_level is at least 0.01
    if quality_level < 0.01:
        quality_level = 0.01
    min_distance = cv2.getTrackbarPos('Min Distance', window_name)
    # Ensure min_distance is at least 1
    if min_distance < 1:
        min_distance = 1


    # Convert frame to grayscale for corner detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply goodFeaturesToTrack (Shi-Tomasi corner detection)
    corners = cv2.goodFeaturesToTrack(gray_frame, max_corners, quality_level, min_distance)

    # Draw corners on the original frame if any are found
    if corners is not None:
        corners = np.intp(corners) # Use np.intp for indexing
        for i in corners:
            x, y = i.ravel()
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1) # Draw green circles at corners

    # Display the frame with corners overlaid
    cv2.imshow(window_name, frame)

    # Check for 'q' key press to exit
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture object and destroy all windows
cap.release()
cv2.destroyAllWindows()
