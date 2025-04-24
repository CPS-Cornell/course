# Computer Vision Examples

This directory contains several examples demonstrating computer vision techniques using OpenCV and Python.

## Basic Image Processing [`basic.py`](basic.py)
Demonstrates basic thresholding on webcam input. The example:
- Captures frames from the webcam
- Extracts the red channel from the RGB image
- Applies binary thresholding with an adjustable threshold value
- Allows interactive control of the threshold via a trackbar

## Gaussian Blur [`blur.py`](blur.py)
Shows how to apply Gaussian blur to a webcam feed:
- Captures frames from the webcam
- Applies Gaussian blur with an adjustable kernel size
- Provides a trackbar to control the blur intensity
- Maps the trackbar value to ensure kernel sizes are always positive and odd

## Corner Detection [`corner_detection.py`](corner_detection.py)
Demonstrates Shi-Tomasi corner detection:
- Captures frames from the webcam
- Uses `goodFeaturesToTrack()` to detect corners
- Provides trackbars to adjust detection parameters:
  - Maximum number of corners
  - Quality level (minimum quality of corners)
  - Minimum distance between corners
- Visualizes corners as green circles on the frame

## Edge Detection [`edge_detection.py`](edge_detection.py)
Implements Canny edge detection:
- Captures frames from the webcam
- Applies Canny edge detection with adjustable thresholds
- Shows original and edge-detected frames side by side
- Provides trackbars to adjust the two threshold parameters

## Lucas-Kanade Optical Flow [`lucas_kanade.py`](lucas_kanade.py)
Demonstrates sparse optical flow tracking:
- Detects good features to track using Shi-Tomasi method
- Tracks these features across frames using the Lucas-Kanade algorithm
- Visualizes motion by drawing lines between old and new feature positions
- Re-detects features when too many are lost
- Provides trackbars to adjust feature detection parameters

## Feature Matching [`feature_matching_webcam.py`](feature_matching_webcam.py)
Shows feature matching between a template image and webcam frames:
- Loads a template image ('example.jpg')
- Uses ORB (Oriented FAST and Rotated BRIEF) for feature detection
- Applies brute-force matching with Lowe's ratio test
- Visualizes matches between the template and current frame
- Provides trackbars to control:
  - Number of good matches to display
  - Ratio test threshold for match filtering
