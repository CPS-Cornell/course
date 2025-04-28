import degirum as dg
import cv2
import time

token = "dg_SxtLxKUmnHvhaB2567apQKwdy3wbGTuuhyzCx"
#token = "<your_token_here>"  # Replace with your actual token

# Connect to DeGirum's public model zoo
zoo = dg.connect(dg.CLOUD, "https://cs.degirum.com/degirum/public", token=token)

model_cloud = dg.load_model(
    model_name="yolov5m_relu6_coco--640x640_quant_tflite_multidevice_1",
    inference_host_address="@cloud",
    zoo_url='degirum/public',
    token=token,
)

#https://hub.degirum.com/degirum/intel/yolov8n_relu6_coco--640x640_quant_openvino_multidevice_1
model_local = dg.load_model(
    model_name="yolov5m_relu6_coco--640x640_quant_tflite_multidevice_1",
    inference_host_address="@local",
    zoo_url='degirum/public',
    token=token,
)

import pdb; pdb.set_trace()

# Load the image using OpenCV
image_path = "cow.jpg"
image_np = cv2.imread(image_path)

# Check if the image was loaded successfully
if image_np is None:
    print(f"Error: Could not load image from {image_path}")
    exit()

# Perform inference on the NumPy array
start_time = time.time()
result_local = model_local(image_np)
print(f"Local Inference time: {time.time() - start_time:.2f} seconds")

start_time = time.time()
result_cloud = model_cloud(image_np)
print(f"Cloud Inference time: {time.time() - start_time:.2f} seconds")

# Display the result (using the local result for display)
# Note: result_cloud.image_overlay could also be used if needed
cv2.imshow("Detection Result", result_local.image_overlay)
cv2.waitKey(0) # Wait indefinitely until a key is pressed
cv2.destroyAllWindows() # Close the window
