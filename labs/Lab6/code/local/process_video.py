# laptop_receiver.py
# Install dependencies on the laptop:
#   pip install imagezmq opencv-python

import cv2
import imagezmq
import time
import simplejpeg

def main():
    # Listen on all interfaces port 5555
    image_hub = imagezmq.ImageHub(open_port="tcp://*:5555")

    try:
        start_time = time.time()
        n_frames = 0
        while True:
            # Use this line of code to receive uncompressed images
            #rpi_name, frame = image_hub.recv_image()

            # Use these lines of code to receive compressed images
            rpi_name, frame = image_hub.recv_jpg()
            frame = simplejpeg.decode_jpeg(frame, colorspace="BGR")

            # Display in a window named after the Pi hostname
            cv2.imshow(rpi_name, frame)

            # Send reply so the Pi can send next frame
            image_hub.send_reply(b"OK")

            # Exit on 'q' key
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            # This code measures the frame rate (FPS)
            if n_frames % 10 == 0:
                end_time = time.time()
                elapsed_time = end_time - start_time
                fps = n_frames / elapsed_time
                print(f"FPS: {fps:.2f}")
                start_time = end_time
                n_frames = 0
            n_frames = n_frames + 1
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
