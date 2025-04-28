# pi_zero_camera.py
# Install dependencies on the Pi:
#   sudo apt update
#   sudo apt install python3-picamera2 python3-pip
#   pip3 install imagezmq numpy opencv-python>=4.0.0 # Ensure OpenCV version is 4.0.0 or higher

import socket
import time
from picamera2 import Picamera2
import imagezmq
import cv2    
import numpy as np

def squareness(bbox):
    if bbox is not None:
        points = bbox[0].astype(int)
    
        # Calculate side lengths
        side1 = np.linalg.norm(points[0] - points[1])
        side2 = np.linalg.norm(points[1] - points[2])
        side3 = np.linalg.norm(points[2] - points[3])
        side4 = np.linalg.norm(points[3] - points[0])
    
        # Avoid division by zero if a side length is somehow 0
        if min(side1, side2, side3, side4) > 0:
            max_side = max(side1, side2, side3, side4)
            min_side = min(side1, side2, side3, side4)
            side_ratio = min_side / max_side
        else:
            side_ratio = 0 # Not a valid quadrilateral for our purpose
    else:
        side_ratio = 0

    return side_ratio

def landmark_is_visible(qr_bbox):
    #TODO: Implement this function to check if the landmark is visible in the frame
    # This is a placeholder function. You need to implement the logic to check if the landmark is visible.
    pass

              
def main():
              
    detector = cv2.QRCodeDetector() # Corrected class name

    # Replace with your laptop's IP (or hostname) and port:
    connect_to = "tcp://10.49.66.76:5555"
    sender = imagezmq.ImageSender(connect_to=connect_to)
    rpi_name = socket.gethostname()

    picam2 = Picamera2()
    # Configure preview stream at 640×480
    preview_config = picam2.create_preview_configuration(main={"size": (640, 480)})
    picam2.configure(preview_config)
    picam2.start()
    time.sleep(2)  # let camera warm up

    try:
        while True:
            frame = picam2.capture_array()

            # Use the correct variable 'frame' here
            data, bbox, _ = detector.detectAndDecode(frame) 
            if data:
                print("QR Code detected:", data)
                # Optionally, draw the bounding box on the frame
                # Ensure bbox is not None before trying to access its elements
                if bbox is not None:
                    # bbox is a numpy array of shape (1, 4, 2) for a single QR code
                    # Extract the points correctly
                    points = bbox[0].astype(int)
                    # Draw a red dot at the upper left corner of the QR code
                    upper_left = tuple(points[0])
                    cv2.circle(frame, upper_left, radius=6, color=(0, 0, 255), thickness=-1)
                    # Draw the bounding box
                    if squareness(bbox) > 0.8:
                        cv2.polylines(frame, [points], isClosed=True, color=(0, 255, 0), thickness=2)
                    else:
                        cv2.polylines(frame, [points], isClosed=True, color=(0, 0, 255), thickness=2)

                # send_image blocks until the message is sent
                sender.send_image(rpi_name, frame)
                # Optional: throttle frame rate
                time.sleep(0.1)
            else:
                 # Send frame even if no QR code is detected
                 sender.send_image(rpi_name, frame)
                 time.sleep(0.1) # Keep throttling consistent

    except KeyboardInterrupt:
        pass
    finally:
        picam2.stop()
        sender.close() # Close the sender socket

if __name__ == "__main__":
    main()
