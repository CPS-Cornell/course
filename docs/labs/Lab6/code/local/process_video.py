# laptop_receiver.py
# Install dependencies on the laptop:
#   pip install imagezmq opencv-python

import cv2
import imagezmq
import signal
import sys

def signal_handler(sig, frame):
    print('Ctrl+C pressed, shutting down...')
    # Clean up resources
    cv2.destroyAllWindows()
    if 'image_hub' in globals():
        image_hub.close()
    sys.exit(0)

def main():
    # Register signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Listen on all interfaces port 5555
    global image_hub
    image_hub = imagezmq.ImageHub(open_port="tcp://*:5555")

    try:
        while True:
            rpi_name, frame = image_hub.recv_image()
            # Display in a window named after the Pi hostname
            cv2.imshow(rpi_name, frame)

            # Send reply so the Pi can send next frame
            image_hub.send_reply(b"OK")

            # Exit on 'q' key
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Ensure proper cleanup
        cv2.destroyAllWindows()
        image_hub.close()

if __name__ == "__main__":
    main()
