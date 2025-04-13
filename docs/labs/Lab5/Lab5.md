
# Complementary Filter Lab

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

Gyroscopes measure the rate of rotation around an axis. When integrated over time, these angular rates yield an estimate of the angle (roll, pitch, and yaw). In the lab, students **do not need to integrate the gyroscope data manually** because the provided IMU class handles this.

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

The `UDPServer` class is used to transmit data from the Pico to your computer. Efficient data transmission is critical to ensure smooth operation and minimal delays.

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
        udp_server.send_message(buffer)
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

