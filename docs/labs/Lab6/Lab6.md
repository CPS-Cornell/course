# Lab 6 - Computer Vision

## Code Explanation

This lab involves two Python scripts: `stream_data.py` which runs on the Raspberry Pi Zero 2 W, and `process_video.py` which runs on your laptop. Together, they stream video from the Pi's camera to the laptop, detect QR codes in the video stream, analyze their shape, and display the annotated video feed.

### [`stream_data.py`](code/zero/stream_data.py) (Raspberry Pi)

This script is responsible for capturing images from the Pi camera, processing them to find QR codes, and streaming the video feed over the network to the laptop.

1. **Imports:**
    - `socket`: Used to get the Raspberry Pi's hostname, which helps identify the video stream source on the laptop.
    - `time`: Used for pausing execution (e.g., `time.sleep()`) to allow the camera to warm up and to throttle the frame rate.
    - `picamera2`: The library for controlling the Raspberry Pi Camera Module 3.
    - `imagezmq`: A library specifically designed for sending OpenCV images over ZeroMQ, a high-performance asynchronous messaging library. This handles the network streaming efficiently.
    - `cv2` (OpenCV): The computer vision library used for image processing, specifically QR code detection and drawing annotations.
    - `numpy`: A fundamental package for numerical computation in Python, used here for handling image data (arrays) and geometric calculations.

2. **`squareness(bbox)` Function:**
    - This function takes the bounding box (`bbox`) of a detected QR code as input. The `bbox` is an array of four corner points.
    - It calculates the lengths of the four sides of the bounding box using `np.linalg.norm` (Euclidean distance).
    - It then finds the ratio of the shortest side length to the longest side length.
    - A perfect square would have a ratio of 1.0. This function helps determine how distorted the QR code appears in the image (e.g., due to perspective). It returns 0 if the `bbox` is invalid or has zero-length sides.

3. **`main()` Function:**
    - **Initialization:**
        - `cv2.QRCodeDetector()`: Creates an object capable of detecting and decoding QR codes in images.
        - `imagezmq.ImageSender()`: Sets up the client side of the image streaming. It needs the `connect_to` address, which should be the IP address and port of the laptop running `process_video.py` (e.g., `tcp://LAPTOP_IP:5555`).
        - `socket.gethostname()`: Gets the Pi's hostname (e.g., "raspberrypi") to send along with the images.
        - `Picamera2()`: Initializes the camera object.
        - `picam2.create_preview_configuration()`: Configures the camera stream resolution (640x480).
        - `picam2.configure()` and `picam2.start()`: Applies the configuration and starts the camera.
        - `time.sleep(2)`: Pauses briefly to let the camera sensor stabilize.
    - **Main Loop (`while True`):**
        - `picam2.capture_array()`: Captures a single frame from the camera as a NumPy array (OpenCV format).
        - `detector.detectAndDecode(frame)`: Attempts to find and decode a QR code within the captured `frame`. It returns the decoded data (string), the bounding box coordinates (`bbox`), and a rectified QR code image (which we ignore with `_`).
        - **If a QR code is detected (`if data:`):**
            - The decoded `data` is printed to the Pi's console.
            - If `bbox` is not `None`:
                - The corner points are extracted (`points = bbox[0].astype(int)`).
                - A small red circle (`cv2.circle`) is drawn at the top-left corner (`points[0]`) of the QR code.
                - The `squareness` function is called with the `bbox`.
                - If the squareness ratio is high (> 0.8), the bounding box is drawn in green (`cv2.polylines`). Otherwise (indicating more distortion), it's drawn in red.
        - `sender.send_image(rpi_name, frame)`: Sends the Pi's hostname and the (potentially annotated) `frame` to the laptop via ImageZMQ. This call blocks until the laptop acknowledges receipt (via `image_hub.send_reply(b"OK")` in `process_video.py`).
        - `time.sleep(0.1)`: A small delay is added to limit the frame rate, reducing network and processing load.
        - **If no QR code is detected (`else:`):**
            - The raw, unannotated frame is still sent to the laptop using `sender.send_image()`.
            - The same `time.sleep(0.1)` delay is applied.
    - **Shutdown (`except KeyboardInterrupt`, `finally`):**
        - Allows you to stop the script gracefully using Ctrl+C.
        - `picam2.stop()`: Stops the camera.
        - `sender.close()`: Closes the ImageZMQ connection.

### [`process_video.py`](code/local/process_video.py) (Laptop)

This script runs on the laptop and acts as the server, receiving and displaying the video stream sent by the Raspberry Pi.

1. **Imports:**
    - `cv2` (OpenCV): Used here primarily for displaying the received images (`cv2.imshow`) and handling user input (`cv2.waitKey`).
    - `imagezmq`: Used to create the `ImageHub`, which listens for and receives images from ImageZMQ senders.

2. **`main()` Function:**
    - **Initialization:**
        - `imagezmq.ImageHub(open_port="tcp://*:5555")`: Creates the server hub. `tcp://*:5555` means it listens on port 5555 on all available network interfaces of the laptop.
    - **Main Loop (`while True`):**
        - `image_hub.recv_image()`: Waits to receive an image. When an image arrives, it returns the sender's name (`rpi_name`, sent by `stream_data.py`) and the image `frame`. This call blocks until an image is received.
        - `cv2.imshow(rpi_name, frame)`: Displays the received `frame` in an OpenCV window. The window title is set to the `rpi_name`, making it easy to identify which Pi the stream is coming from if multiple Pis were connected.
        - `image_hub.send_reply(b"OK")`: Sends a simple "OK" reply back to the sender (the Pi). This is crucial because the `sender.send_image()` on the Pi blocks until it receives this reply. This mechanism prevents the Pi from overwhelming the laptop or network by sending frames faster than they can be processed.
        - `cv2.waitKey(1) & 0xFF == ord("q")`: Checks if the 'q' key has been pressed in the OpenCV display window. `cv2.waitKey(1)` waits for 1ms for a key press. If 'q' is pressed, the loop breaks.
    - **Shutdown (`except KeyboardInterrupt`, `finally`):**
        - Allows stopping the script with Ctrl+C in the terminal.
        - `cv2.destroyAllWindows()`: Closes the OpenCV display window.

In summary, `stream_data.py` captures video, looks for QR codes, annotates the video frame with bounding boxes (colored based on squareness) and a corner marker, and sends the frames over the network using `imagezmq`. `process_video.py` receives these frames using `imagezmq`, displays them in a window, and sends back acknowledgments to regulate the stream.

### [`test_degirum.py`](code/test_degirum.py)

This script demonstrates how to use the DeGirum SDK to perform object detection using a pre-trained model (YOLOv5 in this case) both locally and on the DeGirum cloud platform.

1. **Imports:**
    - `degirum as dg`: The DeGirum SDK for AI inference.
    - `cv2` (OpenCV): Used for displaying the resulting image with detections.
    - `time`: Used to measure the inference time.
2. **Token:**
    - A placeholder `token = "<your_token_here>"` is defined. You need to replace this with your actual DeGirum API token to authenticate with the cloud service.
3. **Connect to Zoo:**
    - `dg.connect()` establishes a connection to the DeGirum cloud model zoo, specifying the cloud URL and providing the token.
4. **Load Models:**
    - `dg.load_model()` is called twice to load the same object detection model (`yolov5m_relu6_coco...`):
        - `model_cloud`: Configured to run inference on the DeGirum cloud (`inference_host_address="@cloud"`).
        - `model_local`: Configured to run inference on the local machine (`inference_host_address="@local"`), assuming the necessary DeGirum runtime and model files are installed locally.
5. **Perform Inference:**
    - The script loads a sample image (`cow.jpg`).
    - It calls `model_local("cow.jpg")` to run inference locally and measures the time taken.
    - It then calls `model_cloud("cow.jpg")` to run inference on the cloud and measures the time taken.
    - The inference times are printed to the console.
6. **Display Result:**
    - `result.image_overlay` contains the original image with bounding boxes drawn around detected objects.
    - `cv2.imshow()` displays this image in a window titled "Detection Result".
    - `cv2.waitKey(0)` keeps the window open until a key is pressed.
    - `cv2.destroyAllWindows()` closes the display window.

This script serves as a basic example to verify your DeGirum setup, test connectivity, compare local vs. cloud inference performance, and understand how to load models and process results using the SDK.

## Task 1: Ensure Viability of Object

The goal of this task is to determine if a object image, placed to the right of the QR code, is fully visible within the camera's field of view. Since we know the approximate size and relative position of the object (similar size to the QR code, immediately to its right), we can use the detected QR code's geometry to estimate the object's position.

**Approach:**

1. **Get QR Code Geometry:** When a QR code is detected, the `detector.detectAndDecode` function returns its bounding box (`bbox`), which contains the coordinates of its four corners.
2. **Estimate QR Code Width:** Calculate the width of the QR code. A simple approximation is the distance between the top-left and top-right corners, or the bottom-left and bottom-right corners. Averaging these might give a more robust estimate, especially if the QR code is viewed at an angle.
3. **Find Rightmost Edge of QR Code:** Determine the maximum x-coordinate among the QR code's corner points. This represents the right edge of the QR code in the image.
4. **Estimate objects's Right Edge:** Since the object is to the right of the QR code and roughly the same width, estimate the position of the object's right edge by adding the estimated QR code width to the QR code's rightmost x-coordinate.
5. **Check Frame Bounds:** Compare the estimated x-coordinate of the object's right edge against the width of the camera frame (640 pixels in our configuration). If the estimated coordinate is less than the frame width, we can assume the object is likely within the frame horizontally. (We assume vertical alignment is sufficient if the QR code itself is fully visible).

**Implementation:**

You need to implement the `object_is_visible(qr_bbox, frame_width)` function in `stream_data.py`.

```pseudocode
FUNCTION object_is_visible(qr_bounding_box, frame_width):

    IF qr_bounding_box is NOT valid THEN
        RETURN FALSE // Cannot estimate without QR code
    ENDIF

    Get the corner points from qr_bounding_box

    // Basic check: If any QR code corner is outside the frame, assume object is also out.
    IF any corner point's x-coordinate >= frame_width OR any corner point's coordinate < 0 THEN
        RETURN FALSE
    ENDIF

    // Estimate the width of the QR code
    Calculate distance between top-left and top-right corners (top_width)
    Calculate distance between bottom-left and bottom-right corners (bottom_width)

    IF top_width <= 0 OR bottom_width <= 0 THEN
        RETURN FALSE // Invalid width calculation
    ENDIF

    qr_estimated_width = AVERAGE(top_width, bottom_width)

    // Find the rightmost edge of the QR code
    qr_rightmost_x = some code that gets the rightmost edge

    // Estimate the position of the object's right edge
    // Assumes object is right next to QR code and is the width of the qr code times
    // some factor
    estimated_object_right_x = qr_rightmost_x + (qr_estimated_width*some factor)

    // Check if the estimated object edge is within the frame
    IF estimated_object_right_x < frame_width THEN
        RETURN TRUE
    ELSE
        RETURN FALSE
    ENDIF

END FUNCTION
```

**Integration:**

1. **Pass Frame Width:** Modify the `main` function to get the frame width. Since we configure it as 640x480, this should be `frame_width = 640`, however if you want to change the frame size in the future you should get it dynamically from the `frame` shape (`frame.shape[1]`).
2. **Call the Function:** Inside the `if data:` block in `main`, after successfully detecting a QR code and getting a valid `bbox`, call `object_is_visible(bbox, frame_width)`.
3. **Use the Result:** You can use the boolean result to modify the visualization. For example, you could change the color of the bounding box or print a status message indicating whether the object is considered visible.

Example call within `main` (inside `if data:` and `if bbox is not None:`):

```python
                # ... (inside if data: and if bbox is not None:)
                frame_width = frame.shape[1] # Get frame width
                object_in_view = object_is_visible(bbox, frame_width)

                # Draw the bounding box - color based on visibility AND squareness
                points = bbox[0].astype(int)
                is_square = squareness(bbox) > 0.8

                if object_in_view and is_square:
                    box_color = (0, 255, 0) # Green: Square and object Visible
                    print("QR Code detected: {} - Object Visible: Yes".format(data))
                elif Object_in_view and not is_square:
                     box_color = (0, 255, 255) # Yellow: Distorted but object Visible
                     print("QR Code detected: {} - Object Visible: Yes (Distorted)".format(data))
                elif not object_in_view and is_square:
                    box_color = (0, 165, 255) # Orange: Square but object NOT Visible
                    print("QR Code detected: {} - Object Visible: No".format(data))
                else: # not object_in_view and not is_square
                    box_color = (0, 0, 255) # Red: Distorted and object NOT Visible
                    print("QR Code detected: {} - Object Visible: No (Distorted)".format(data))

                cv2.polylines(frame, [points], isClosed=True, color=box_color, thickness=2)

                # Draw red dot at top-left corner regardless
                upper_left = tuple(points[0])
                cv2.circle(frame, upper_left, radius=6, color=(0, 0, 255), thickness=-1)

            else: # bbox is None
                 print("QR Code detected: {} - BBox is None".format(data))

        # ... rest of the loop ...
```

Remember to adjust the print statements and color logic as needed for your specific requirements.

## Task 2: Image Resolution

The goal of this task is to increase the resolution of the video stream captured by the Raspberry Pi camera from 640x480 to 1920x1080 (Full HD). This will provide a much clearer image but will also increase the processing and network load.

**Steps:**

1. **Locate the relevant code:** Open the `stream_data.py` script, which runs on the Raspberry Pi. Find the `main()` function.
2. **Identify the configuration line:** Inside `main()`, look for the line where the camera configuration is created:

    ```python
    config = picam2.create_preview_configuration(main={"size": (640, 480)})
    ```

3. **Modify the resolution:** Change the `size` tuple from `(640, 480)` to `(1920, 1080)`. The modified line should look like this:

    ```python
    config = picam2.create_preview_configuration(main={"size": (1920, 1080)})
    ```

4. **Save the changes:** Save the modified `stream_data.py` file.
5. **Run the scripts:** Execute `stream_data.py` on the Raspberry Pi and `process_video.py` on your laptop as before.

**Observations:**

- The video displayed on the laptop should now be significantly larger and more detailed.
- Notice the potential impact on performance:
  - The frame rate might be lower due to the increased amount of data being captured, processed (especially QR code detection on a larger image), and sent over the network.
  - The Raspberry Pi's CPU usage might increase.
  - Network latency could become more noticeable.
- The `process_video.py` script on the laptop does not require any changes, as `imagezmq` and `cv2.imshow` handle variable frame sizes automatically. However, displaying the larger video window will consume more resources on the laptop as well.

Experiment with this higher resolution and observe how it affects the system's performance and the QR code detection process.

## Task 3: DeGirum Performance Testing

The goal of this task is to measure and compare the inference performance of the DeGirum AI platform under different conditions. You will use the provided `test_degirum.py` script as a basis to test object detection inference time locally versus on the cloud, on both your laptop and the Raspberry Pi, using images of different resolutions.

**Steps:**

1. **Find a Test Image:** Download a reasonably high-resolution image (e.g., > 1920x1080 pixels) from the internet. A JPG or PNG image containing various objects would be suitable. Save it in the same directory as your test script.
2. **Modify `test_degirum.py` (or create a new script):**
    - **Load Image:** Replace `cow.jpg` with the filename of your chosen image. Use `cv2.imread()` to load it into a NumPy array.

        ```python
        image_path = "your_image_name.jpg" # Replace with your image file
        original_image = cv2.imread(image_path)
        if original_image is None:
            print(f"Error: Could not load image at {image_path}")
            exit()
        print(f"Loaded image: {image_path}, Original Size: {original_image.shape[1]}x{original_image.shape[0]}")
        ```

    - **Define Resolutions:** Specify two target resolutions for testing.

        ```python
        low_res_size = (640, 480) # Width, Height
        # Use a higher resolution, e.g., 1920x1080 or the original size if appropriate
        high_res_size = (1920, 1080) # Width, Height
        # Or dynamically get a size, e.g., high_res_size = (original_image.shape[1], original_image.shape[0])
        ```

    - **Resize Images:** Create resized versions of the original image using `cv2.resize`. Remember `cv2.resize` takes `(width, height)`.

        ```python
        low_res_image = cv2.resize(original_image, low_res_size)
        high_res_image = cv2.resize(original_image, high_res_size)
        images_to_test = {
            "LowRes": low_res_image,
            "HighRes": high_res_image
        }
        ```

    - **Load DeGirum Models:** Keep the code that loads the cloud and local models (`dg.connect`, `dg.load_model`). Ensure you replace `<your_token_here>` with your actual DeGirum token.

3. **Install DeGirum Runtime (if needed):** Ensure the DeGirum runtime is installed on both your laptop and your Raspberry Pi if you want to run local inference on both. You can typically install it using pip:

    ```bash
    pip install degirum
    ```

    Follow DeGirum's documentation for detailed installation instructions and any prerequisites. If local inference is not possible on the Pi (e.g., due to hardware limitations or installation issues), you can skip those specific tests but note why.

4. **Set up a DeGirum Account:**
    - Go to [www.degirum.ai](www.degirum.ai) and click `Sign In` in the upper right hand corner.
    - Create an account or sign in with a google account.
    - To to the `Tokens` tab on the left hand side of the page.
    - Generate a new token and use this new token in the `test_degirum.py` script.

5. **Run on Laptop:** Execute the modified script on your laptop. Record the four timing results (Local/LowRes, Local/HighRes, Cloud/LowRes, Cloud/HighRes).
6. **Run on Raspberry Pi:** Copy the modified script and the test image to your Raspberry Pi. Execute the script on the Pi. Record the four timing results (Local/LowRes, Local/HighRes, Cloud/LowRes, Cloud/HighRes). Note if local inference fails or is not attempted.
7. **Analyze Results:** Compare the 8 measurements. Consider:
    - How does local performance compare between the laptop and the Pi?
    - How does cloud performance compare when initiated from the laptop versus the Pi? (This primarily reflects network latency differences).
    - How does increasing image resolution affect local inference time on each device?
    - How does increasing image resolution affect cloud inference time?
    - How does local performance compare to cloud performance for each device/resolution combination?

## Task 4: Putting it all together

The final task is to integrate the components developed in the previous tasks to create a system that can reliably determine when a object is likely clearly visible next to a QR code and then *simulate* triggering an external process, such as calling the Google Cloud Vision API for object classification.

**Goal:** Modify `stream_data.py` to trigger an API call only when specific conditions indicate a high confidence that the object is in view and clearly captured. Crucially, implement a hysteresis mechanism to avoid excessive triggers, conserving resources like API quotas.

**Context: API Limits**: Real-world APIs, like the Google Cloud Vision or DeGirum API, often have usage limits. The free tier might allow only a certain number of calls per month (e.g., 1000). Therefore, it's essential to trigger the API call *only* when necessary and not continuously, even if the conditions are met frame after frame.

**Trigger Conditions:**

An API call should only be triggered if **all** of the following conditions are met simultaneously:

1. A QR code is successfully detected (`data` is not empty).
2. The QR code's bounding box is valid (`bbox` is not `None`).
3. The `object_is_visible()` function (from Task 2) returns `True`.
4. The `squareness()` of the QR code is above a threshold indicating a clear, head-on view (e.g., `squareness(bbox) > 0.8`).
5. A minimum time interval (cooldown period) has passed since the last API call was triggered (e.g., 30 seconds).

**Hysteresis Implementation:**

To implement the cooldown period (hysteresis):

1. **Track Last Call Time:** You'll need a variable to store the timestamp of the last time the API call was successfully triggered. Initialize this variable before the main loop (e.g., `last_api_call_time = 0.0`).
2. **Define Cooldown Period:** Define a constant for the required delay between triggers (e.g., `API_COOLDOWN_SECONDS = 30`).
3. **Check Time Elapsed:** Inside the main loop, when evaluating the trigger conditions, add a check using `time.time()`: `(time.time() - last_api_call_time) > API_COOLDOWN_SECONDS`.
4. **Update Timestamp:** If all conditions (including the time check) are met and you trigger the simulated API call, immediately update the `last_api_call_time` to the current time: `last_api_call_time = time.time()`.

**Implementation Steps:**

1. **Modify `stream_data.py`:**
    - Add the `last_api_call_time` variable and `API_COOLDOWN_SECONDS` constant before the `try` block in `main()`.
    - Locate the section within the main loop where the QR code is detected (`if data:` and `if bbox is not None:`).
    - Inside this block, add a new conditional statement (`if`) that checks *all* the trigger conditions listed above (object visible, squareness, and time elapsed).
    - Inside this new `if` block:
        - Print a clear message to the console indicating that the API call is being triggered (e.g., `print(">>> Triggering Object Classification API Call! <<<")`).
        - Update `last_api_call_time = time.time()`.
    - **Note:** The object detection model may return a number of objects depending on what is visible to the camera. Verify the class of the object that is on the piece of paper by analyzing the geometry of the bounding box. The object should be a specific distance (in pixels) from the QR which can be estimated from the size of the QR code bounding box.
    - Ensure your existing visualization logic (drawing colored bounding boxes) still functions correctly alongside this new trigger logic.

2. **Testing:**
    - Run `stream_data.py` on the Pi and `process_video.py` on the laptop.
    - Position the QR code and a placeholder object classification in front of the camera.
    - Move the setup around to test different scenarios:
        - QR code not visible.
        - QR code visible but distorted (low squareness).
        - QR code visible and square, but object estimated to be out of frame.
        - QR code visible, square, and object estimated to be in frame.
    - Observe the console output on the Pi. Verify that the "Triggering..." message appears *only* when all conditions are met.
    - Verify that after the message appears, it does not appear again for at least 30 seconds, even if the conditions remain true during that time.
    - Check that the bounding box colors on the video feed still correctly reflect the squareness and object visibility status.

**Example Code Snippet (Conceptual - place within `main` loop):**

```python
# --- Add these before the try block ---
last_api_call_time = 0.0
API_COOLDOWN_SECONDS = 30
# ---

# ... inside the main loop ...
            if data:
                # ... (existing code to handle data and bbox) ...
                if bbox is not None:
                    # ... (existing code for points, squareness, object_is_visible) ...
                    frame_width = frame.shape[1]
                    object_in_view = object_is_visible(bbox, frame_width)
                    is_square = squareness(bbox) > 0.8 # Or your chosen threshold

                    # --- Add API Trigger Logic ---
                    current_time = time.time()
                    if object_in_view and is_square and (current_time - last_api_call_time > API_COOLDOWN_SECONDS):
                        print(f"QR: {data} - Object Visible: Yes, Square: Yes - Time OK")
                        print(">>> Triggering Object Classification API Call! <<<")
                        last_api_call_time = current_time
                        # In a real application, the API call would happen here.
                    # --- End API Trigger Logic ---

                    # ... (existing code to determine box_color based on object_in_view and is_square) ...
                    # ... (existing code for cv2.polylines and cv2.circle) ...

                else: # bbox is None
                    # ... (existing code) ...
            else:
                 # ... (existing code for sending frame when no QR code) ...

            # ... (rest of the loop: sender.send_image, time.sleep) ...
```

## Questions

1. **QR Code Detection (`stream_data.py`):**
    - How does the `squareness()` threshold (e.g., 0.8) affect the reliability of the `object_is_visible()` estimation? What are the trade-offs of using a higher or lower threshold?
    - The `object_is_visible()` function makes several assumptions (object size relative to QR code, object position). How could you make this estimation more robust or accurate?

2. **Video Streaming (`stream_data.py` & `process_video.py`):**
    - Explain the purpose of the `image_hub.send_reply(b"OK")` call in `process_video.py` and the blocking nature of `sender.send_image()` in `stream_data.py`. What might happen if this reply mechanism were removed?
    - What was the observed impact of increasing the camera resolution (Task 2) on frame rate, CPU usage (if monitored), and network traffic? Discuss the trade-offs between resolution and performance in this streaming scenario.

3. **DeGirum Performance (Task 3):**
    - Based on your measurements, when is local inference preferable to cloud inference, and vice-versa? Consider factors like latency, processing power, network availability, and image resolution.
    - Why might cloud inference time be relatively consistent regardless of whether it's initiated from the laptop or the Pi, while local inference times differ significantly?
    - How did image resolution impact local inference time compared to cloud inference time? Explain the likely reasons for any differences observed.

4. **System Integration & API Triggering (Task 4):**
    - Explain the concept of hysteresis and why it was implemented using `last_api_call_time` and `API_COOLDOWN_SECONDS`. What problems does this solve when interacting with potentially rate-limited or costly APIs?
    - The trigger logic combines multiple conditions (QR detected, object visible, squareness, cooldown). Why is it important to check *all* these conditions before triggering the simulated API call? What could go wrong if one condition was omitted?
    - The current system *simulates* an API call. If you were to implement a real call to an object classification API (like Google Cloud Vision or DeGirum), what additional steps or considerations would be necessary (e.g., handling API keys, processing the API response, error handling)?
    - The note in Task 4 mentions verifying the object class based on geometry relative to the QR code. How would you implement this geometric check using the bounding boxes from an object detection model and the QR code's `bbox`?
