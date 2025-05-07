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
window_name = 'Blurred Webcam Feed'
cv2.namedWindow(window_name)

# Create a trackbar for kernel size
# Max value 50 (will correspond to kernel size 101)
# Initial value 7 (will correspond to kernel size 15)
cv2.createTrackbar('Kernel Size', window_name, 7, 50, nothing)


print("Press 'q' to quit.")

# Loop to continuously get frames from the webcam
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # If frame reading was not successful, break the loop
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        break

    # Get current trackbar position
    kernel_val = cv2.getTrackbarPos('Kernel Size', window_name)

    # Ensure kernel size is odd and positive
    kernel_size_val = kernel_val * 2 + 1 # Map 0->1, 1->3, 2->5, ... 50->101

    # Apply Gaussian blur to the frame using the dynamic kernel size
    # sigmaX=0 means it's calculated from kernel size
    # Handle case where kernel_size_val might be 0 or negative if trackbar is at 0
    if kernel_size_val > 0:
        blurred_frame = cv2.GaussianBlur(frame, (kernel_size_val, kernel_size_val), 0)
    else: # Should not happen with kernel_val * 2 + 1, but good practice
        blurred_frame = frame # No blur if kernel is invalid


    # Display the blurred frame
    cv2.imshow(window_name, blurred_frame)

    # Check for 'q' key press to exit
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture object and destroy all windows
cap.release()
cv2.destroyAllWindows()
