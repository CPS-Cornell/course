# Lab3: Sensors

In this lab, you will work with multiple sensors on the Raspberry Pi Pico: an IMU, a line-following reflectance sensor, an ultrasonic rangefinder, and a VCNL4040 proximity sensor. Your goal is to get each sensor up and running, print out their data values, and then experiment with transmitting data to a host computer using UDP. You will also learn how to visualize your live data and record logs for later analysis.

---

## File Descriptions

Below is a brief description of the files included in your lab. These files provide sensor drivers, utilities for data transmission, live plotting, and logging.

1. [`imu.py`](code/pico/imu.py)

    - Contains Python code to interface with the Inertial Measurement Unit (IMU) over I2C. It likely includes functions to initialize the IMU, read sensor data (e.g., accelerometer, gyroscope, possibly magnetometer), and return the sensor readings for further processing.

2. [`imu_defs.py`](code/pico/imu_defs.py)

    - Holds various definitions, constants, register addresses, or configuration details used by `imu.py`. This separates hardware-specific constants from the main driver code, making it clearer and easier to maintain.

3. [`rangefinder.py`](code/pico/rangefinder.py)

    - Implements functions to interface with an ultrasonic rangefinder (like the HC-SR04 or similar). This file probably contains code to trigger the sensor, measure the echo time, and compute the distance in centimeters or inches.&#x20;

4. [`reflectance.py`](code/pico/reflectance.py)

    - Provides code for reading data from a line-following reflectance sensor. Your sensor uses QRE113-based reflectance detectors. The code will typically initialize the sensor's GPIO pins (or ADC pins), read the reflectance values, and return either an analog or digital reading indicating the presence or absence of a line.

5. [`vcnl4040.py`](code/pico/vcnl4040.py)

    - Contains code to interface with the VCNL4040 proximity sensor over I2C. This file will give you functions to read the "proximity," "lux," and "light" values from the device registers and return them for printing or further processing.

6. [`udp_server.py`](code/pico/udp_server.py)

    - The UDP server script that runs on the Raspberry Pi Pico. It is primarily responsible for streaming data over to the client (running on the laptop) as fast as possible. It can also receive messages from the client. However, these messages aren't currently being used for anything. 

7. [`udp_client.py`](code/local/udp_client.py)

    - The client script runs on the laptop. It is responsible for handling incoming data messages from the pico. It can choose to format this data for plotting or data logging. It can also send messages back to the server (pico), which should receive an acknowledge message to ensure proper message transmission. 

8. [`test_udp_server.py`](code/pico/test_udp_server.py)

    - This is where most of your code will be written. This script implements the sensor readings and sending messages to the client.

9. [`live_plotter.py`](code/local/live_plotter.py)

    - This class runs a plotting threads that can be updated with data reviewed by the UDP client. 

10. [`data_logger.py`](code/local/data_logger.py)

    - A utility script that runs on the laptop and can be used to log the incoming UDP data from the Pico into a CSV file, which you can analyze later with Excel, Python, MATLAB, or other data analysis tools. The CSV file is automatically generated when the python script is killed. 

11. [`test_udp_client.py`](code/local/test_udp_client.py)

    - A test script that runs on the laptop to interact with the UDP server on the Pico. This file demonstrates how to set up a UDP client, process incoming data, and send messages back to the Pico. It provides a foundation for visualizing sensor data and can be modified to work with the live plotter or data logger.

---

## UDP Basics

**User Datagram Protocol (UDP)** is a simple transmission protocol that offers minimal overhead compared to TCP. Here’s what you need to know:

- **Connectionless**: UDP does not require a formal connection setup (the “handshake”) that TCP uses. One device sends a datagram to a designated IP and port, and if a server is listening, it receives it.
- **Faster, but less reliable**: There’s no guarantee of packet delivery or ordering. This lack of overhead makes UDP ideal for real-time applications (e.g., streaming sensor data), but you must handle potential data loss.
- **Why we use it**: For small sensor updates, speed is often more important than guaranteed reliability. If the occasional packet is lost, the next reading will still come in. This is generally acceptable for real-time sensor visualization.

---

## Lab Tasks

This section goes over how to setup each of the sensors. Note: you do not need to include the terminal outputs or raw sensor readings from this section in your lap report. The lap report should only graphs or information relevant to the methodology, such as debug messages that you needed to find a solution to. The Experiment section below will require you to generate figures. 

### 1. IMU (Review from Previous Lab)

If you completed the last lab, you should already have the IMU working. Your first task is to verify that your IMU still initializes correctly and that you can read accelerometer and gyroscope data. Print these values to the terminal (REPL) to confirm. This should still be working from the last two labs. However, please note that the constructor of the for the IMU class has been updated to take an I2C object instead of pin numbers. This is so that the same I2C object can be shared across different sensors. 

- Verify I2C connections.
- Use the functions in `imu.py` (and any supporting definitions in `imu_defs.py`).
- Print accelerometer and gyro data to the REPL in a human-readable format to verify that it is working.

### 2. Line-Following Reflectance Sensor (QRE113)

Next, move on to the line-following reflectance sensor:

- Refer to `reflectance.py` to see how the sensors are read (they may provide an analog value or a simple digital threshold).
- Print the sensor values to see how they change depending on whether they are over a dark or a reflective surface.
- If available, take note of the two sensors’ readings (left vs. right) so you can see how each sensor compares.

### 3. Ultrasonic Rangefinder

Now, get the ultrasonic sensor working:

- Look in `rangefinder.py` to see how to trigger a measurement (often done via a short pulse on a trigger pin) and measure echo time on an input pin.
- Print the computed distance to the REPL.
- **How it works**: The sensor sends out an ultrasonic pulse and measures how long it takes for the echo to return. The speed of sound is approximately 340 m/s, so distance is computed by:
  $$
  \text{Distance} = \frac{\text{Time} \times \text{Speed of Sound}}{2}
  $$
  (divide by 2 because the wave must travel out and back).

### 4. VCNL4040 Proximity Sensor

Finally, set up the VCNL4040:

- Use `vcnl4040.py` to initialize the sensor and read values.
- Print the following to the REPL:
  - **Proximity**: A dimensionless measure of how close an object is to the sensor (usually a larger number indicates closer proximity).
  - **Lux**: An approximate measure of ambient light intensity in SI units (lux).
  - **Light**: This may be a more raw or differently calibrated light reading, depending on how the code is written.
- **How it works**: This sensor uses infrared emitters to measure reflections and estimate proximity. The ambient light sensor measures the environment’s brightness.

---

## Using the UDP Server & Client

Once all sensors are working and you can reliably read data, set up the UDP server to stream data.

1. On the pico:
    - Set up the wifi SSID and password in `test_udp_server.py`. Its also important check your laptop's IP address so the pico knows "where" to send the data. 
      - Mac and Linux: this can be done py opening a terminal and running `ifconfig`.
      - Windows: Open a powershell and run `ipconfig`.
      - WSL: On WSL2, the subsystem creates its own internal IP address that it uses to interface with windows, a kind of virtual ethernet card. This means that WSL does not operate on the same local area network as the pico, even if your windows machine is connected to RedRover. The easiest way around this is to just use windows or downgrade to WSL1. Conda on windows powershell makes for a suitable alternative. However, there are ways to enable port forwarding. [Here](https://www.youtube.com/watch?v=yCK3easuYm4) is a video describing how to enable port forwarding for WSL2. Note you will likely need to enable UDP in Windows Defender Firewall. [Here](https://learn.microsoft.com/en-us/windows/wsl/networking) is Window's documentation on port forwarding. 

2. On the laptop:
   - Configure the IP address of the pico in the UDPClient declaratin: `client = UDPClient(remote_ip='10.49.10.167', listen_port=12345, callback=process_incoming)`.
   - Implement the desired call back function. This should either print the message to the terminal, plot it using the Live Plotter, and/or save the data using the Data Logger.


**Important**: Make sure your sensor data is formatted consistently. 

For the plotter, use three values separated by commas
```
(accel_x, accel_y, accel_z)
```

for the data logger, every message should have a time field. Each value has a sensor title, followed by a colon and the sensor value. Use `time.ticks_ms()` to generate the time stamps

```
TEMP:23.5, HUMID:45, TIME:1001
```

---

## Experiments

### A. Proximity Sensor (VCNL4040)

1. **Objective**: Investigate how the proximity, lux, and light values relate to each other.
2. **Procedure**:
   - Place an object at distances of 0, 2, 4, 6, …, 20 cm from the sensor (Consider using the range finder to assist with this).
   - Record the sensor readings (proximity, lux, and light).
   - Plot or tabulate the values to see how they change with distance.
3. **Discussion questions**
   - How is the proximity related to the distance of an object 
   - How does ambient light (lux/light) relate to the proximity reading?
   - Why might this proximity sensor need to measure ambient light?
4. **Color Variation**:
    - Repeat the experiment with a white object and then a black, matte object.
    - Notice how the color and reflectivity of the object can affect IR-based proximity readings.

### B. Ultrasonic Rangefinder

1. **Maximum Range**:
    - Take a sturdy object like a notebook or box.
    - Move it further and further away until the sensor can no longer detect it.
    - Record that maximum distance.
3. **Accuracy and Precision**:
    - Take a ruler or tape measure and take three measurements at different distances. Consider averaging a couple of readings together to get a better measurement.
    - Take note of the absolute error (accuracy) of this measurement.
    - Pick one stationary distance to place an object and take a couple hundred sensor readings. What is the standard deviation (precision) of these readings?
4. **Material Differences**:
    - Choose a few different materials (e.g., metal, cardboard, soft clothing).
    - Check whether the ultrasonic sensor can detect them at roughly the same distances. Keep trying materials until you find one that the range finder cannot detect.
    - Observe which materials reflect ultrasonic waves well and which do not.
    - Observe if the precision of the readings change depending on the material.

### C. IMU

1. **Gyroscope**
    - Before conducting these experiements, note that there is an automatic calibration sequence that the code. To see the desired effect, we need to disable that with the following code:

```python
myIMU.gyro_offsets[0] = 0
myIMU.gyro_offsets[1] = 0
myIMU.gyro_offsets[2] = 0
```
+
    - This will reset the internal bias calibration and demonstrate the true bias of the gyroscope
    - Bias: take gyroscope readings once or twice a second for a minute or two from one axis *without* moving your board at all. The readings should remain zero. Is this the case?
    - Integration: Because the gyroscope returns angular velocity, the angular position of the board can be determined by integrating. Below is some pseudocode to implement a digital integrator.
  
```
# Initialize variables
gyro_reading = 0  # Raw gyroscope measurement (degrees per second or radians per second)
angular_position = 0  # Estimated angle (degrees or radians)
previous_time = get_current_time()  # Get initial timestamp

# Loop to continuously read gyroscope and update angular position
while true:
    current_time = get_current_time()  # Get current time
    dt = current_time - previous_time  # Calculate time difference
    previous_time = current_time  # Update last timestamp

    gyro_reading = read_gyroscope()  # Read gyroscope value (angular velocity)

    # Integrate to get angular position (θ = θ + ω * dt)
    angular_position = angular_position + (gyro_reading * dt)

    print("Angular Position:", angular_position)  # Display updated angle
```
+
    - **Note:* this loop doesn't have any `delay` or `sleep` calls. This is because it is imperative to integrate a digital signal as quickly as possible to ensure an accurate approximation for the angular position. Because your code calls `await asyncio.sleep(0.3)`, it is recommended to remove this line of code. If you want updates to be less frequently, implement a time to control the rate of data transfer. 
    - Take a couple hundred readings of the gyroscope (with just one axis). What is the mean and standard deviation? The mean of these readings is what we call the "bias". Use two different methods to estimate the orientation the IMU around one axis using the gyroscope.

      - First, integrate the readings to estimate the angle for a minute or so. Plot this and estimate how much drift has accumulated. (Be sure that the `gryo_offset` fields are set to zero.)
      - Next, record gyroscope readings for a few seconds and take the average like before. Then subtract this average from each reading before you integrate it to estimate the IMU angle. Be sure to do these steps right after each other. 
      - Graph both orientations over the course of a minute. Does subtracting the bias of the gyroscope readings reduce the bias of your angle estimates after integrating? 

1. **Accelerometer**
    - Next measure the noise of the accelerometer. Collect a couple of seconds of accelerometer data and save it in a pickle or CSV file on your laptop. Avoid moving the XRP control board or causing any vibrations by bumping the table. 
    - Compute the standard deviations of all three axis of the control board.

---

## Report

Here is an outline that you can follow to organize your report. 

**Introduction** - Give the reader a general sense of what this lab is about and why this topic is important to CPS. 

**Proximity Sensor** 
    -  Methodology 
    -  Results
    -  Discussion

**Range Finder** 
    -  Methodology 
    -  Results
    -  Discussion

**IMU** 
    -  Methodology 
    -  Results
    -  Discussion

**Analysis** - Give an overview of the significance of your results.

**Conclusion and Application** - Briefly ties these concepts to broader CPS application.

As always, refer to the lab report rubric for a more detailed outline of report expectations.

