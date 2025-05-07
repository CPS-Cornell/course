import cv2
import numpy as np
import os

# --- Configuration ---
TEMPLATE_IMAGE_PATH = 'example.jpg'
# NUM_GOOD_MATCHES = 15 # Initial value, will be controlled by slider
# LOWE_RATIO_TEST = 0.75 # Initial value, will be controlled by slider
WINDOW_NAME = 'Feature Matching Controls' # Window for display and controls

# --- Helper Function for Trackbars ---
def nothing(x):
    """Dummy callback function for createTrackbar"""
    pass

# --- Initialization ---

# Check if template image exists
if not os.path.exists(TEMPLATE_IMAGE_PATH):
    print(f"Error: Template image not found at {TEMPLATE_IMAGE_PATH}")
    exit()

# Load the template image in grayscale
template_img = cv2.imread(TEMPLATE_IMAGE_PATH, cv2.IMREAD_GRAYSCALE)
if template_img is None:
    print(f"Error: Could not load template image from {TEMPLATE_IMAGE_PATH}")
    exit()

# Initialize ORB detector
orb = cv2.ORB_create()

# Find keypoints and descriptors in the template image
kp_template, des_template = orb.detectAndCompute(template_img, None)
if des_template is None:
    print("Error: No descriptors found in the template image. Try a different image.")
    exit()

# Initialize Brute-Force Matcher
# Use cv2.NORM_HAMMING for ORB, SIFT, SURF use cv2.NORM_L2
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False) # crossCheck=False for ratio test

# Initialize video capture (0 is usually the default webcam)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# --- Create Window and Trackbars ---
cv2.namedWindow(WINDOW_NAME)
# Trackbar for Number of Good Matches to display
cv2.createTrackbar('Num Matches', WINDOW_NAME, 15, 50, nothing) # Initial 15, Max 50
# Trackbar for Lowe Ratio Test (scaled by 100)
cv2.createTrackbar('Ratio Test x100', WINDOW_NAME, 75, 100, nothing) # Initial 0.75 * 100 = 75, Max 100

print("Starting webcam feed. Press 'q' to quit.")
print("Adjust sliders in the 'Feature Matching Controls' window.")

# --- Main Loop ---
while True:
    # --- Read Trackbar Values ---
    num_good_matches_threshold = cv2.getTrackbarPos('Num Matches', WINDOW_NAME)
    # Ensure at least 1 match is requested for display if slider is > 0
    if num_good_matches_threshold == 0:
        num_good_matches_threshold = 1
    lowe_ratio = cv2.getTrackbarPos('Ratio Test x100', WINDOW_NAME) / 100.0
    # Ensure ratio is slightly above 0 if slider is 0, to avoid issues
    if lowe_ratio == 0:
        lowe_ratio = 0.01

    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Convert frame to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find keypoints and descriptors in the current frame
    kp_frame, des_frame = orb.detectAndCompute(frame_gray, None)

    output_display = None # Initialize variable to hold the image to display

    if des_frame is None or len(des_frame) < 2:
        # Need at least 2 descriptors for knnMatch
        # Create a side-by-side view of template and color frame even if no frame descriptors
        # Ensure template is BGR for stacking with color frame
        template_bgr = cv2.cvtColor(template_img, cv2.COLOR_GRAY2BGR)
        # Resize template to match frame height for hstack
        h1, w1 = template_bgr.shape[:2]
        h2, w2 = frame.shape[:2]
        if h1 != h2:
             # Calculate new width maintaining aspect ratio
            new_w1 = int(w1 * h2 / h1)
            template_bgr = cv2.resize(template_bgr, (new_w1, h2), interpolation=cv2.INTER_AREA)
        # Stack images horizontally
        # Make sure output_display is always assigned before imshow
        if 'template_bgr' in locals() and 'frame' in locals(): # Check if variables exist
             output_display = np.hstack((template_bgr, frame))
        else: # Fallback if template/frame not ready
             output_display = frame # Just show the frame

    else:
        # Match descriptors using KNN (k=2 for ratio test)
        matches = bf.knnMatch(des_template, des_frame, k=2)

        # Apply Lowe's ratio test to find good matches using the slider value
        good_matches = []
        # Handle potential empty matches list or matches with only one neighbor
        try:
            if matches and len(matches[0]) == 2:
                 for m, n in matches:
                     if m.distance < lowe_ratio * n.distance: # Use slider value
                         good_matches.append(m)
        except IndexError:
             # Handle cases where some matches might not have k=2 neighbors
             print("Warning: Issue processing matches (IndexError). Skipping frame.")
             good_matches = [] # Reset good matches

        # Sort matches by distance (best first)
        good_matches = sorted(good_matches, key=lambda x: x.distance)

        # Ensure we don't try to draw more matches than we found or requested
        num_matches_to_draw = min(len(good_matches), num_good_matches_threshold) # Use slider value

        # Draw matches if enough good matches are found (still need > 4 for potential homography)
        if len(good_matches) > 4:
            # Draw matches on the grayscale frame used for detection
            output_display = cv2.drawMatches(template_img, kp_template, frame_gray, kp_frame,
                                          good_matches[:num_matches_to_draw], None, # Use calculated num_matches_to_draw
                                          flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        else:
            # If not enough matches, show template and color frame side-by-side without matches
            # print(f"Not enough good matches found ({len(good_matches)}/ > 4)") # Optional print
            # Use cv2.drawMatches with empty matches list to get side-by-side view
            output_display = cv2.drawMatches(template_img, kp_template, frame, kp_frame,
                                             [], None, # Empty list for matches
                                             flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # Display the resulting frame (either with matches or just side-by-side)
    if output_display is not None:
        cv2.imshow(WINDOW_NAME, output_display) # Show in the named window
    else:
        # Fallback: show the raw frame if output_display wasn't created
        cv2.imshow(WINDOW_NAME, frame) # Show in the named window


    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break

# --- Cleanup ---
cap.release()
cv2.destroyAllWindows()
print("Webcam released and windows closed.")
