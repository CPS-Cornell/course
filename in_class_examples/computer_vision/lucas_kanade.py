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
window_name = 'Lucas-Kanade Optical Flow' # Changed window name
cv2.namedWindow(window_name)

# Create trackbars for goodFeaturesToTrack parameters
# Max corners: 1 to 100, initial 25
cv2.createTrackbar('Max Corners', window_name, 25, 100, nothing)
# Quality level: 1 to 100 (representing 0.01 to 1.0), initial 10 (0.1)
cv2.createTrackbar('Quality Level', window_name, 10, 100, nothing)
# Min distance: 1 to 100, initial 10
cv2.createTrackbar('Min Distance', window_name, 10, 100, nothing)

# Parameters for Lucas-Kanade optical flow
# winSize: Size of the search window at each pyramid level.
# maxLevel: 0-based maximal pyramid level number; if set to 0, pyramids are not used (single level); if set to 1, two levels are used, and so on.
# criteria: Parameter, specifying the termination criteria of the iterative search algorithm.
lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors for drawing tracks
color = np.random.randint(0, 255, (100, 3))

# Take first frame and find corners in it
ret, old_frame = cap.read()
if not ret:
    print("Error: Could not read initial frame.")
    cap.release()
    exit()

old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = None # Initialize points as None

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)

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

    # Parameters for ShiTomasi corner detection (updated from trackbars)
    feature_params = dict( maxCorners = max_corners,
                           qualityLevel = quality_level,
                           minDistance = min_distance,
                           blockSize = 7 )

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # If p0 is None or has too few points, detect new features
    if p0 is None or len(p0) < max_corners // 2: # Re-detect if less than half points remain
        print(f"Detecting new features... (Current points: {0 if p0 is None else len(p0)})")
        p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
        if p0 is None:
             print("No features found, trying next frame.")
             old_gray = frame_gray.copy() # Update old_gray even if no features found
             mask = np.zeros_like(old_frame) # Reset mask
             continue # Skip the rest of the loop if no features found
        print(f"Detected {len(p0)} features.")
        mask = np.zeros_like(old_frame) # Reset mask when re-detecting

    # Calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # Select good points
    if p1 is not None and st is not None:
        good_new = p1[st==1]
        good_old = p0[st==1]
    else:
        # Handle case where optical flow fails entirely
        print("Optical flow calculation failed.")
        p0 = None # Force re-detection next frame
        old_gray = frame_gray.copy()
        mask = np.zeros_like(old_frame) # Reset mask
        continue

    # Draw the tracks
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel().astype(int) # Use astype(int) for drawing
        c, d = old.ravel().astype(int) # Use astype(int) for drawing
        mask = cv2.line(mask, (a, b), (c, d), color[i % len(color)].tolist(), 2)
        frame = cv2.circle(frame, (a, b), 5, color[i % len(color)].tolist(), -1)

    # Combine the frame with the mask
    img = cv2.add(frame, mask)

    # Display the resulting frame
    cv2.imshow(window_name, img)

    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

    # Check for 'q' key press to exit
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture object and destroy all windows
cap.release()
cv2.destroyAllWindows()
