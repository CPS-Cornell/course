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
window_name = 'Original | Edge Detection' # Changed window name
cv2.namedWindow(window_name)

# Create trackbars for Canny thresholds
# Max value 255 is common, adjust if needed
# Initial values 100 and 200 are typical starting points
cv2.createTrackbar('Threshold 1', window_name, 100, 255, nothing)
cv2.createTrackbar('Threshold 2', window_name, 200, 255, nothing)


print("Press 'q' to quit.")

# Loop to continuously get frames from the webcam
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # If frame reading was not successful, break the loop
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        break

    # Get current trackbar positions for thresholds
    thresh1 = cv2.getTrackbarPos('Threshold 1', window_name)
    thresh2 = cv2.getTrackbarPos('Threshold 2', window_name)

    # Convert frame to grayscale for Canny
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply Canny edge detection using trackbar values
    edges = cv2.Canny(gray_frame, thresh1, thresh2)
    # Convert single-channel edges back to 3-channel BGR for display
    edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Ensure both frames have the same height before stacking
    # (Should be the case here, but good practice if resizing)
    # combined_height = max(frame.shape[0], edges_bgr.shape[0])
    # frame_resized = cv2.resize(frame, (int(frame.shape[1] * combined_height / frame.shape[0]), combined_height))
    # edges_bgr_resized = cv2.resize(edges_bgr, (int(edges_bgr.shape[1] * combined_height / edges_bgr.shape[0]), combined_height))

    # Stack the original frame and the edge-detected frame side-by-side
    combined_frame = np.hstack((frame, edges_bgr))


    # Display the combined frame
    cv2.imshow(window_name, combined_frame)

    # Check for 'q' key press to exit
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture object and destroy all windows
cap.release()
cv2.destroyAllWindows()
