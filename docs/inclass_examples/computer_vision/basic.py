import cv2
import numpy as np

def nothing(x):
    pass

# Initialize video capture from the default webcam (index 0)
cap = cv2.VideoCapture(0)

# Check if the webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Create a named window
window_name = 'Webcam Feed'
cv2.namedWindow(window_name)

cv2.createTrackbar('Value', window_name, 100, 255, nothing)

print("Press 'q' to quit.")

# Loop to continuously get frames from the webcam
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # If frame reading was not successful, break the loop
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        break

    thresh1 = cv2.getTrackbarPos('Value', window_name)

    #frame_copy = np.clip(frame.astype(np.float32) * .3, 0, 255).astype(np.uint8)

    # Convert frame to grayscale 
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold to the grayscale image
    #_, thresh_frame = cv2.threshold(gray_frame, thresh1, 255, cv2.THRESH_BINARY)

    b,g,r = cv2.split(frame)
    _, thresh_frame = cv2.threshold(r, thresh1, 255, cv2.THRESH_BINARY)

    # Display the frame
    cv2.imshow(window_name, thresh_frame)

    # Check for 'q' key press to exit
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture object and destroy all windows
cap.release()
cv2.destroyAllWindows()
