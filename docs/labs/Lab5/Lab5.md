# Kalman Filter

## File Overview

### Files Designed to Run on the Raspberry Pi Pico

1. **[controller.py](code/pico/controller.py)**

   - **What it contains**: An abstract `Controller` class meant to be extended for different control strategies (e.g., PID). It defines the interface (`update`, `is_done`, `clear_history`) that all controllers must implement.
   - **How it works**: You can create your own specialized controller (like a PID) by subclassing `Controller`. That specialized controller then implements how the input (for instance, an error signal) translates into an output (motor effort).
   - **Usage**: In this project, the `PID` class (defined in `pid.py`) inherits from this to handle tasks such as speed control, heading maintenance, or distance-based movement.

2. **[pid.py](code/pico/pid.py)**

   - **What it contains**: A `PID` class that extends `Controller`. This code tracks integral and derivative terms and handles capping output, integral wind-up, and checking whether the controller has reached its target (via `is_done`).
   - **How it works**: The `update` method calculates a control output based on proportional, integral, and derivative terms. You can configure gains (kp, ki, kd), output limits, and tolerance for stopping.
   - **Usage**: Used anywhere you want closed-loop control for speeds, positions, or angles (for example, maintaining a certain heading or traveling at a certain velocity).

3. **[motor.py](code/pico/motor.py)**

   - **What it contains**: Two classes (`SinglePWMMotor` and `DualPWMMotor`) that manage basic motor operations such as setting direction, PWM duty cycle, and braking or coasting.
   - **How it works**: Depending on the hardware version, the class sets a PWM signal to the motor driver pins, flipping direction if the effort is negative. There are also methods to brake or let the motor coast.
   - **Usage**: These classes are lower-level drivers. Higher-level code (like `EncodedMotor` or `DifferentialDrive`) calls methods here to move the motors.

4. **[encoder.py](code/pico/encoder.py)**

   - **What it contains**: An `Encoder` class that uses the Raspberry Pi Pico’s Programmable I/O (PIO) to track shaft rotations. It reads two digital input signals (A and B channels) and keeps an internal count.
   - **How it works**: The code uses a small assembly program (written in rp2 ASM) to decode the quadrature signals from the motor shaft. It returns both raw counts and derived revolutions.
   - **Usage**: Provides feedback on how far (and in what direction) the motor or wheel has turned. Essential for measuring distance traveled and heading in a differential drive system.

5. **[encoded_motor.py](code/pico/encoded_motor.py)**

   - **What it contains**: An `EncodedMotor` class that combines a motor driver (from `motor.py`) and an encoder (from `encoder.py`). It has methods for speed control, effort control, and position resets.
   - **How it works**:
     - When you call `set_speed`, it uses a PID controller (from `pid.py`) to match the measured speed (derived from the encoder) to the requested target.
     - When you call `set_effort`, it directly sets PWM duty cycles.
   - **Usage**: Serves as a mid-level abstraction so you do not have to deal directly with PWM signals or raw encoder counts. Great for tasks like “maintain 10 cm/s” or “apply half effort.”

6. **[differential_drive.py](code/pico/differential_drive.py)**

   - **What it contains**: A `DifferentialDrive` class that encapsulates two `EncodedMotor` objects (left and right) plus an optional IMU for heading measurements. It also has high-level movement methods (straight, turn, arcade drive).
   - **How it works**:
     - Functions like `arcade` or `set_speed` combine efforts for left and right motors to move the robot forward, backward, or turn in place.
     - The “straight” and “turn” methods are asynchronous, using PID logic on distance or angle errors.
     - Optionally uses IMU data (if present) to refine turning accuracy.
   - **Usage**: Instead of controlling each motor individually, you can just say: “Go 20 cm forward” or “Turn 90 degrees,” and it handles the details via motor and encoder data.

7. **[imu.py](code/pico/imu.py)**

   - **What it contains**: An `IMU` class to read accelerometer and gyroscope data from an onboard LSM6DSO sensor. It includes methods to calibrate the sensor, get X/Y/Z rates, and keep an internal running pitch/roll/yaw.
   - **How it works**:
     - Uses I2C to communicate with the sensor.
     - On a timer interrupt, it continuously updates angles (pitch, roll, yaw) based on the gyro’s rotation rates.
     - Allows calibrations for offsets so you can zero out drift on each axis.
   - **Usage**: Provides orientation information that can be fused with encoder data. In the lab, this is the “sensor measurement” side of the Kalman filter.

8. **[imu_defs.py](code/pico/imu_defs.py)**

   - **What it contains**: Constants and register definitions used by `imu.py`. For instance, the sensor’s I2C address and bitfield definitions for scale ranges (2g, 4g, etc.), output data rates, and so on.
   - **How it works**: `imu.py` uses these definitions to set up the IMU registers (e.g., to pick a measurement rate of 208 Hz and a gyro range of ±2000 dps).
   - **Usage**: You likely will not need to modify this file unless you want to change register-level behavior.

9. **[udp_server.py](code/pico/udp_server.py)**

   - **What it contains**: A simple `UDPServer` class and a helper function `connect_to_wifi`. The class handles sending strings or bytes to a specified IP/port.
   - **How it works**:
     - Uses a standard Python socket on the Pico to transmit data via UDP.
     - `connect_to_wifi(ssid, password)` brings up the network interface and attempts to join the WiFi network.
   - **Usage**: In `kalman_filter.py`, you create a `UDPServer` instance and call `send` to pass data back to a client on your laptop (for plotting or logging).

10. **[kalman_filter.py](code/pico/kalman_filter.py)**

    - **What it contains**:
      - A main loop (using `asyncio`) that continuously reads encoder yaw (from the differential drive) and gyro yaw (from the IMU) and fuses them using a simple 1D Kalman filter.
      - Parameters for the filter (Q, R, P) and an example of how to store readings in arrays.
      - A routine to send the data arrays to a laptop via UDP once the array is filled.
    - **How it works**:
      - Defines `Q` (process noise), `R` (measurement noise), and `P` (initial covariance).
      - Each iteration does a predict-and-update step to estimate heading.
      - Collects data in arrays (`time_data`, `encoder_yaw_data`, `imu_yaw_data`, `kalman_data`, etc.) and sends them via `udp_server.send()`.
    - **Usage**: This is the main script you run on the Pico. You can alter Q, R, or the array sizes and observe the results in real time.

11. **[timeout.py](code/pico/timeout.py)**

    - **What it contains**: A `Timeout` class that helps track elapsed time and can indicate when a specified duration has passed.
    - **How it works**: When initialized with a timeout value in seconds, it records the current time (in milliseconds) and later checks whether the difference exceeds that timeout. If it does, `is_done()` returns True.
    - **Usage**: Primarily used to enforce a maximum duration for certain tasks (for instance, in `differential_drive.py` to stop trying to move forward or turn if it takes too long). This ensures the robot doesn’t stall indefinitely.

---

### Files Designed to Run on the Laptop Client

The following files are **not** intended for the Pico. They are used on your **laptop** to receive data from the Pico, parse it, log it, and generate plots.

12. **[data_logger.py](code/local/data_logger.py)**

    - **What it contains**: A `DataLogger` class that processes incoming sensor data, organizes it by sensor and time, and can save it to a file (either as a pickle or CSV).
    - **How it works**:
      - `process_string` parses raw text data with fields like `"TIME:<time>, SENSOR:<value>"`.
      - `process_dict` can handle dictionary-based data (e.g., arrays of time and sensor values).
      - The data is stored internally, and you can then save it to disk.
    - **Usage**: Instantiate this class in your laptop-based script or application. As new data arrives over UDP, call the logger’s methods to store and eventually save the data.

13. **[live_plotter.py](code/local/live_plotter.py)**

    - **What it contains**: A `LivePlotter` class that creates a Matplotlib window and updates it in real time with roll/pitch/yaw (or other) data.
    - **How it works**:
      - Maintains a fixed buffer size for recent data.
      - You can call `process_incoming_data(message)` to parse new data points.
      - An async loop `run_plot_loop` continuously updates the plot so it appears to stream in real time.
    - **Usage**: Use on the laptop side to visualize data as it arrives from the Pico. It can be combined with a UDP client that feeds each incoming message into `process_incoming_data`.

14. **[udp_client.py](code/local/udp_client.py)**

    - **What it contains**: A `UDPClient` class designed to receive UDP messages on your laptop.
    - **How it works**:
      - Binds to a local IP/port (e.g., `0.0.0.0:5005`).
      - Runs a background thread that calls a callback function whenever data is received.
    - **Usage**: Create a `UDPClient`, provide a callback to handle incoming packets (e.g., parse and log them). This is the companion to the `udp_server` code running on the Pico.

15. **[udp_client_example.py](code/local/udp_client_example.py)**

    - **What it contains**: A basic example script that uses `UDPClient` and `DataLogger`.
    - **How it works**:
      - Defines a callback function (`print_message`) that unpacks the data from the Pico. It checks the data length, interprets them as floats, and feeds them into a `DataLogger`.
      - Runs a loop so it can continuously listen and store data.
    - **Usage**: Launch this on your laptop to receive sensor arrays from `kalman_filter.py` running on the Pico. Adjust the array sizes and sensor lists as needed.

## Task 2: Tuning the Kalman Filter Parameters (Q and R)

1. **Locating Q and R**

   - In [`kalman_filter.py`](code/pico/kalman_filter.py), near the top, you will see lines like:
     ```python
     Q = 0.01  # Process noise covariance
     R = 0.1   # Measurement noise covariance
     ```
   - `Q` represents how uncertain you believe your *process* model is (i.e., how accurate you think your encoder-based estimate is).
   - `R` represents how uncertain you believe your *sensor* (IMU) measurement is.

2. **Experiment**

   - Vary Q and R to explore how the Kalman filter estimate changes.
   - Generate three distinct test runs, collecting data each time so you can plot the results:
     - **Case A**: Make Q larger than R.
     - **Case B**: Make R larger than Q.
     - **Case C**: Make them about the same.

3. **Plot**

   - For each of the three cases, plot:
     - IMU yaw vs. time
     - Encoder yaw vs. time
     - Kalman-filtered yaw vs. time
   - Be sure to include uncertainty bands (variance or the signal) as part of the graph.
   - These three lines on one plot show you how the filter merges the two signals differently depending on noise ratios.

4. **Observations**

   - When Q is very large, your encoder (process) updates are deemed untrustworthy, and the filter may rely more on the IMU reading.
   - When R is very large, the IMU measurement is seen as untrustworthy, so the filter leans more heavily on the encoder reading.
   - When Q and R are similar, the filter attempts to balance both signals.

---

## Task 3: Adjusting the Array Size and Measuring Loop Speed

1. **Locate the Array Size**

   - In [`kalman_filter.py`](code/pico/kalman_filter.py), there is a variable named `ARRAY_SIZE = 50`. This controls how many samples you store and send at once.

2. **Synchronize Changes**

   - If you change `ARRAY_SIZE` on the server (Pico side), you must also change the client-side code that *receives* the data. The data format uses `struct.pack` in chunks of `ARRAY_SIZE` floats, so the client needs to expect the same number.

3. **Experiment**

   - Increase the array size in increments (e.g., 100, 200, 500, …). After each change, run the system:
     - Watch if it successfully transmits or if you get errors or dropped packets.
     - Watch your loop time.
   - Keep going until something breaks, such as out-of-memory errors, UDP errors, or noticeable lag.

4. **Measure Loop Timing**

   - Add some code to measure how fast each loop iteration runs. For instance:
     ```python
     start_time = time.ticks_us()
     # (rest of the loop)
     end_time = time.ticks_us()
     elapsed = time.ticks_diff(end_time, start_time)
     ```
   - Print or store `elapsed` to see how the average loop time changes with bigger array sizes. Does it get slower?

---

## Task 4: Discussion Questions

After conducting the above experiments, answer the following:

1. **How do process noise (Q) and sensor noise (R) individually affect the Kalman filter?**

   - Reflect on how your plots changed in Task 2.

2. **How does a Kalman filter compare to a complementary filter?**

   - Both can fuse multiple sensor inputs.
   - The complementary filter is typically simpler, using fixed-weight filtering in the frequency domain, while the Kalman filter adapts weighting based on dynamic estimates of uncertainty.

3. **How does the array (buffer) size impact performance?**

   - Consider your data from Task 3. Did it affect real-time responsiveness? Did you notice memory limits or dropped data?

4. **Does the buffer size impact only the server, or also the client?**

   - Because the client must receive the same number of floats, both ends must match. The client side can also get overwhelmed by larger or more frequent packets.

5. **Any additional observations or ideas for improvement?**

   - This is open-ended. You might consider potential expansions like including the accelerometer reading into the filter or using more sophisticated filtering for the gyroscope drift.

---

# Complementary Filter

## 1. Introduction

In this lab, your will explore the design and implementation of a **complementary filter**—a simple yet effective method of sensor fusion used to estimate orientation by combining the strengths of accelerometer and gyroscope measurements. The accelerometer offers an absolute measurement of orientation based on gravity, while the gyroscope provides angular rate information that must be integrated over time to obtain an angle. Each sensor has its own weaknesses: the accelerometer is subject to noise and disturbances (e.g., from vibrations), whereas the gyroscope is prone to drift over time. The complementary filter blends both measurements using a weighted approach to produce a reliable estimate of roll and pitch.

---

## 2. Complementary Filter Theory

A complementary filter functions by applying a **high-pass filter** on the gyroscope data and a **low-pass filter** on the accelerometer data, effectively covering each sensor’s weaknesses with the strengths of the other. The process is governed by a parameter—commonly referred to as **alpha (α)**—that defines the weight given to the gyroscope versus the accelerometer. A typical filter update equation for an angle (e.g., roll) is:

```
roll_filtered = α × (previous_roll + gyro_rate × Δt) + (1 – α) × roll_acc
```

Where:

- `(previous_roll + gyro_rate × Δt)` is the estimate from the gyroscope.
- `roll_acc` is the angle computed from the accelerometer.
- `α` is the filter coefficient (typically 0.95–0.99).

---

## 3. Gyroscope Data for Attitude Estimation

Gyroscopes measure the rate of rotation around an axis. When integrated over time, these angular rates yield an estimate of the angle (roll, pitch, and yaw). In the lab, students **do not need to integrate the gyroscope data manually** because the provided IMU class (from [`imu.py`](code/pico/imu.py)) handles this.

To access these values:

```python
imu.get_roll()
imu.get_pitch()
imu.get_yaw()
```

These return the orientation values (in degrees) computed from gyroscope integration.

---

## 4. Calculating Roll and Pitch from the Accelerometer

The accelerometer measures acceleration along the sensor’s axes. When gravity is the only force acting, we can calculate orientation using trigonometry:

```
roll_acc = arctan2(acc_y, acc_z) × (180 / π)
pitch_acc = arctan2(-acc_x, sqrt(acc_y² + acc_z²)) × (180 / π)
```

- `acc_x`, `acc_y`, `acc_z` are accelerometer readings in mg.
- These formulas yield roll and pitch angles in degrees.

For a more detailed overview of how these equations are derived, see [this](https://mwrona.com/posts/accel-roll-pitch/) blogpost.

---

## 5. Implementing the Complementary Filter

To fuse the gyro and accelerometer readings:

### Filter Algorithm:

1. Get the gyroscope-based angle (`imu.get_roll()`).
2. Get accelerometer readings (`imu.get_acc_x()`, etc.).
3. Compute roll and pitch from accelerometer using `arctan2`.
4. Fuse the values:

```
filtered_roll = α × (previous_roll + gyro_roll_rate × dt) + (1 – α) × roll_acc
```


---

## 6. Data Transmission Using `UDPServer`

The `UDPServer` class (from [`udp_server.py`](code/pico/udp_server.py)) is used to transmit data from the Pico to your computer. Efficient data transmission is critical to ensure smooth operation and minimal delays.

### Best Practices:

1. **Use Fixed-Length Array Buffers:**
  - Instead of Python lists, use [**MicroPython arrays**](https://docs.micropython.org/en/latest/library/array.html) for buffering data. Arrays are more memory-efficient and faster because they store elements of a fixed type (e.g., `float` or `int`), whereas lists can store mixed types and have higher memory overhead.
  - Arrays are particularly useful on resource-constrained devices like the Pico, where memory and processing power are limited.
  - Think of these arrays as C++ style arrays, which are static but more efficient than python lists.

2. **Buffering Strategy:**
  - Avoid sending data on every loop iteration, as this can overwhelm the UDP connection and lead to dropped packets or delays.
  - Use a **fixed-length array buffer** to accumulate data. Only send the data over UDP when the buffer is full. This reduces the frequency of transmissions and ensures that each packet contains meaningful data.

3. **Multiple Buffers for Different Data Types:**
  - If you need to store and transmit multiple types of data (e.g., timestamps, accelerometer roll and pitch, gyroscope roll and pitch, complementary filter roll and pitch), you should use separate buffers for each type. This ensures that the data remains organized and easy to process on the receiving end.
  - For example, if you want to store the following:
    - **Timestamps**
    - **Accelerometer roll and pitch**
    - **Gyroscope roll and pitch**
    - **Complementary filter roll and pitch**
    You would need **7 separate buffers** of the same size, one for each data type.

4. **Processing Data on the Client:**
   - When the data is received on your laptop, make sure to parce the strings correctly.
   - You can save this data to a CSV file and create visualizations.

---

1. ## Pseudocode:

```python
# Initialize filter parameters
alpha = 0.98
dt = 0.01  # time between updates
previous_roll = imu.get_roll()

# Create fixed-length array buffers
buffer_size = SOME_SIZE
buffer = create_fixed_length_array(buffer_size)
buffer_index = 0

# Main loop
while True:
    gyro_roll = imu.get_roll()
    
    ax = imu.get_acc_x()
    ay = imu.get_acc_y()
    az = imu.get_acc_z()

    roll_acc = some math

    filtered_roll = some more math
    previous_roll = filtered_roll

    buffer[buffer_index] = [filtered_roll, ...]
    buffer_index += 1

    if buffer_index == buffer_size:
        udp_server.send_message(buffer) # Assuming udp_server is an instance of UDPServer from udp_server.py
        buffer_index = 0

    sleep(dt)
```

## 8. Complentary Filter Questions

Answer the following questions after completing your implementation:

1. **Sensor Fusion Advantage:**  
   What are the advantages and disadvantages of using only the gyroscope or accelerometer?

2. **Filter Mechanism:**  
   How does the complementary filter work? Why do we high-pass the gyro and low-pass the accelerometer?

3. **Alpha Parameter:**  
   What is the role of α in the filter? How does changing α affect performance?

4. **Buffering Strategy:**  
   Why is buffering necessary before sending over UDP? What benefits do arrays have over lists in MicroPython?

5. **Graphs:**
   Inlcude a graph or the accelleromter, gryoscope, and complementary filter data for roll and pitch (use separate graphs for roll and pitch).

6. **Yaw Computation:**
   Why is the the yaw not computed using a complementary filter?

