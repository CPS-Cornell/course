# **Lab2: TCP for Data Streaming and Command Messages

## Python on your Laptop

This lab will require you to run python code locally on your laptop, including using pip to install some dependencies. It is best practice to use a virtual environment to ensure that package dependencies don't interfere with each other from project to project. Windows users are also recommended to try using WSL, which can be downloaded from the microsoft store (Ubuntu 24.04 is the recommended version), by following [these](https://dev.to/brayandiazc/install-wsl-from-the-microsoft-store-111h) instructions. 

Instructions on how to install and use virtual environment package managers, such as [pyenv](../../tutorials/pyenv_tutorial.md) and [anaconda](../../tutorials/anaconda_tutorial.md), can be found on the tutorials page.

Once you have your virtual environment set up, use conda or pip to install the appropriate dependencies for running `test_tcp_client.py` on your laptop. 
---

### Overview

In this lab, you will modify a Raspberry Pi Pico MicroPython project that streams Inertial Measurement Unit (IMU) data to a laptop and receives commands from the laptop to control the Pico’s on-board LED. You will be working primarily in **`test_tcp_server.py`**, where you will:

1. Read real-time roll, pitch, and yaw data from the IMU and send those values to a client (running on a PC) via a TCP connection.
2. Respond to messages from the client (`ON` or `OFF`) by turning the LED on or off accordingly.

A matching client program (`test_tcp_client.py`) runs on your laptop, connects to the Pico over Wi-Fi, and plots the received data in real time.

The second portion of this lab will not require any programming, but instead will require you to think about what future functionality you might want to implement on your robot and design a messaging format that supports those functions

---

### Background: Callback functions


## Code Structure and Explanation

Below is an overview of each file and its role in this project.

### 1 [`imu_defs.py`](code/pico/imu_defs.py)
- Defines constants and register addresses for the LSM6DSO IMU (an accelerometer + gyroscope).
- Houses low-level bitfield and register definitions (e.g., `LSM_REG_CTRL1_XL`, `LSM_ODR`, etc.) that help configure and communicate with the sensor.
- You will not need to edit this file directly, but it is useful to understand how the IMU is being set up and read.

### 2 [`imu.py`](code/pico/imu.py)
- Contains the `IMU` class, which handles higher-level communication with the LSM6DSO sensor.
- Manages initialization, calibration, and reading of accelerometer and gyroscope data (in mg and mdps).  
- Maintains internally computed roll, pitch, and yaw angles by integrating gyro data over time.
- Key methods you might call:
  - `get_roll()`, `get_pitch()`, `get_yaw()`: Return the current orientation angles in degrees.
  - `calibrate()`: Collects baseline readings to zero out the IMU.

### 3 [`tcp_server.py`](code/pico/tcp_server.py)
- Implements a simple TCP server class, `TCPServer`, using `uasyncio` on the Pico.
- Handles client connections, listens for incoming messages, and sends data back to the client.
- Provides:
  - `start()`: Sets up Wi-Fi, listens on a port for a client connection.
  - `handle_client(reader, writer)`: Callback that’s invoked once a client connects. Receives messages from the client.
  - `send(message)`: Sends data to the connected client.
  - `callback`: A user-defined function (passed in) that processes incoming messages.

### 4 [`test_tcp_server.py`](code/pico/test_tcp_server.py) (Your Main Focus)
- **Where you will do most of your work.**
- Imports and instantiates `TCPServer`.
- Declares (or should declare) the LED pin and the IMU object.
- Contains:
  - `read_sensor()`: A function that **you will modify** to read roll, pitch, and yaw from the IMU.
  - `process_message()`: A function that **you will modify** to parse incoming text commands from the client and turn the LED on/off.
  - An asynchronous `main()` function that:
    1. Starts the TCP server.
    2. Waits for a connection.
    3. In a loop, calls `read_sensor()` and sends the data to the client over TCP.

### 5 [`tcp_client.py`](code/local_computer/tcp_client.py)
- A Python (desktop) client class, `TCPClient`, using `asyncio` to connect to the Pico.
- When connected, it listens for incoming messages and can send commands back (like `ON` or `OFF`).

### 6 [`test_tcp_client.py`](code/local_computer/test_tcp_client.py)
- Demonstrates usage of `TCPClient`.
- Prompts you for the Pico’s IP address.
- Opens a live plot (via `live_plotter.py`).
- Lets you send text commands (like `ON` or `OFF`) from the keyboard to the Pico.

### 7 [`live_plotter.py`](code/local_computer/live_plotter.py)
- Handles real-time plotting of roll, pitch, and yaw using `matplotlib` and an asynchronous loop.
- Whenever new sensor data arrives, it updates the rolling plot in near real time.


## **Understanding Callback Functions and Their Role in Asynchronous Communication**

### **What is a Callback Function?**
A **callback function** is a function that is **passed as an argument** to another function and is **executed later**, usually in response to an event or the completion of an operation. Instead of directly executing a function where it is defined, the program **"calls back"** to it when needed.

Callbacks are commonly used in **event-driven programming** and **asynchronous systems**, where operations do not execute sequentially but rather respond to external events like user inputs, sensor updates, or incoming network messages.

### **Why Are We Using Callback Functions in This Lab?**
In this lab, the Raspberry Pi Pico is running a **TCP server** that must:
1. **Listen for incoming messages from the client** (your laptop).
2. **Process these messages asynchronously** (without blocking the main execution loop).
3. **Execute specific actions** based on the received messages, such as toggling the LED.

Since **incoming messages arrive unpredictably**, we need a mechanism to **handle them as they come in**, without blocking other tasks like sensor readings. This is where callback functions are useful.

### **How Do Callback Functions Work in This Lab?**
The **callback function is used to process incoming TCP messages asynchronously.** Let's break it down step by step.

1. **The `TCPServer` class (in `tcp_server.py`) is designed to handle TCP communication.**
   - It includes a `callback` function that gets executed **whenever** a message is received.
   - When we create a `TCPServer` object, we **pass a function** (e.g., `process_message()`) as a callback.

2. **Whenever the Pico receives a message from the client, the callback function is executed.**
   - This allows the program to respond dynamically to different messages (like "ON" and "OFF") without needing to check for messages manually.

3. **This makes our system asynchronous** because:
   - We don’t have to stop everything and wait for a message.
   - The Pico can **keep running other tasks** (e.g., reading IMU data) while waiting for messages.

### **Why Are Callback Functions Important for Asynchronous Communication?**
In **asynchronous programming**, multiple tasks can run **concurrently** without blocking each other. This is crucial for networking because **network operations (like waiting for a message) can take an unpredictable amount of time**.

#### **How do Callbacks Improve Asynchronous Communication?**
- Instead of **pausing execution** to wait for data (which would freeze the Pico), the system **registers a callback function** that is **triggered automatically** when new data arrives.
- The **main program continues running** while waiting for network events.
- This approach **prevents lag** and allows the Pico to handle **multiple tasks at once**.

### **Callback Function Implementation in MicroPython on the Pico**
Here’s how we **implement a callback function** to handle incoming TCP messages.

#### **1. The TCP Server Class (`tcp_server.py`)**
In the `TCPServer` class, there is a `callback` function that **gets executed whenever data is received**:
```python
class TCPServer:
    def __init__(self, port=1234, callback=None):  
        self.port = port
        self.callback = callback  # Store the callback function

    async def handle_client(self, reader, writer):
        """Handles incoming messages from a client"""
        print("Client connected")
        try:
            while True:
                data = await reader.readline()  # Read incoming message
                if not data:
                    print("Client disconnected")
                    break
                message = data.decode().strip()
                print("Received:", message)

                if self.callback:  # If a callback function is defined, call it!
                    self.callback(message)
        except Exception as e:
            print("Error handling client:", e)
```
**Key Idea**: The function `self.callback(message)` is triggered when a message is received.

#### **2. Registering a Callback in `test_tcp_server.py`**
We now **pass our own function (`process_message`) as the callback** when creating the `TCPServer` instance.

```python
# Function to process incoming TCP messages (callback function)
def process_message(message):
    print("Processing incoming message:", message)
    #TODO: Check if message is "ON" or "OFF" and control LED

# Initialize the TCP Server and pass `process_message` as the callback
tcp_server = TCPServer(callback=process_message)
```
Here:
- When `TCPServer` receives a message, it **automatically calls** `process_message()`.
- This lets us **separate network handling from application logic**—the Pico’s network module doesn’t need to know what the message means, just that it should forward it to `process_message()`.

### **Example of Callback in a Simple Asynchronous System**
If the concept of callbacks is still unclear, let’s simplify it.

Imagine you have a **button** on the Pico, and you want to execute a function whenever the button is pressed.

**Define a callback function:**
```python
from machine import Pin

def button_pressed(pin):
    print("Button pressed!")

# Initialize button with an interrupt and attach the callback function
button = Pin(2, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)
```
- Instead of **constantly checking** the button in a loop, we register `button_pressed()` as a callback.
- The function **only runs when needed** (i.e., when the button is pressed).

This is the **same concept** we apply in `TCPServer`:
- Instead of **checking for messages manually**, we let the system **call `process_message()` whenever data is received**.


### **Final Thoughts: Why MicroPython and the Pico Need This**

1. **Limited resources**: The Pico doesn’t have a powerful processor, so it cannot afford to block execution while waiting for network messages.
2. **Event-driven model**: MicroPython’s `uasyncio` is designed to handle multiple tasks efficiently.
3. **Cleaner Code**: Using callbacks **keeps networking logic separate** from application logic (reading sensors, controlling LEDs, etc.).

**Summary**
- Callback functions allow us to **react to events asynchronously** instead of constantly checking for updates.  
- They enable **efficient handling of network messages** on the Pico without blocking sensor readings or other tasks.  
- In this lab, we **pass `process_message()` as a callback** so the Pico **automatically handles** TCP messages like "ON" and "OFF" without manual polling.  
- This makes our program **responsive, modular, and efficient**, ensuring smooth real-time data transmission.

---

## Lab Tasks

### Task 1: IMU Data Streaming
1. **Create and initialize the IMU object**:
   - Near the top of `test_tcp_server.py`, create a new IMU object that you can use to get sensor readings.
   - This gives you access to the `imu` methods: `get_roll()`, `get_pitch()`, and `get_yaw()`.

2. **Update `read_sensor()`**:
   - Currently, `read_sensor()` returns random values for demonstration.  
   - Replace that code with calls to the IMU’s orientation getters:
   - Ensure you return a tuple of `(roll, pitch, yaw)` in degrees.

3. **Send the data to the client**:
   - In the loop at the end of `main()`, `test_tcp_server.py` already does something like:
     ```python
     sensor_data = read_sensor()
     await tcp_server.send("Sensor data: " + str(sensor_data))
     ```
   - You don’t need to change that line, but now it will actually return meaningful IMU angles.  

4. **Confirm data is plotted**:
   - On your PC, run `test_tcp_client.py`, provide the Pico’s IP address, and you should see a live plot of roll, pitch, yaw.

### Task 2: LED Control from the Client
1. **Declare the LED pin**:
   - For most Raspberry Pi Pico boards, the onboard LED is connected to `Pin(25)` (or `Pin("LED")` in some builds).
   - At the top of `test_tcp_server.py`, declare an LED pin that you can use to control the onboard LED. 

2. **Implement `process_message(message)`**:
   - The client will send text lines such as `"ON"` or `"OFF"`.
   - Add code that parses the message and turn the LED on or off depending on `"ON"` or `"OFF"`.

3. **Test it**:
   - On your PC, run `test_tcp_client.py`.  
   - Once connected, type `ON` or `OFF` in the console. The Pico’s onboard LED should turn on or off accordingly.

## 4. Deliverables

- **Modified `test_tcp_server.py`** including:
  1. **Working IMU data read** in `read_sensor()`.
  2. **Functional LED on/off handling** in `process_message(message)`.

- **Short demonstration video** (optional but encouraged) showing:
  - This is mostly easily done by uploading a video clip to youtube and including a URL in your report
  - The Pico’s LED turning on/off.
  - Real-time pitch/roll/yaw changes on the live plot as the Pico is moved.

- **Lab report** detailing:
  1. **Setup**: Your wiring (if any), environment, and steps to connect.
  2. **Code Changes**: Summarize your modifications to `test_tcp_server.py`.
  3. **Results**: Screenshots of the plot. Observations about the IMU readings.
  4. **Analysis**: Why is implementing something like a TCP server/client for our future robot important?
  5. **Conclusion**: Challenges, insights, or improvements you might make.
  6. **Note**: Overall, this first portion of the lab is mush shorter than previous labs and won't require as long of a report.

---

## **Thinking Ahead: Expanding Robot Communication**

In this lab, we established a basic communication system between a Raspberry Pi Pico and a laptop, allowing the Pico to **stream IMU data** and **receive simple ON/OFF commands** to control an LED. However, in a real-world robotics application—especially a **differential drive robot**—communication would need to be much more sophisticated.

Now, let’s think ahead:  
- **What types of data should the Pico send to the laptop for logging and analysis?**  
- **What kinds of commands might the laptop send back to the Pico to control its behavior?**  
- **How should these messages be structured for clarity and efficiency?**  

Your task in this section is to **brainstorm and document a communication protocol** that could support more advanced functionality for a differential drive robot.

---

### **Structuring the Communication Protocol**
In this section, you'll brainstormed **what data needs to be sent** and **what commands need to be received**, think about **how to structure messages efficiently.** Some questions to consider:
- Should messages be **human-readable** (e.g., `"TURN:90"`), or should they be **short binary values** to save bandwidth?
- How will messages be **parsed and processed** on both the Pico and the laptop?
- What happens if a message **gets lost** or **corrupt**—should the laptop request data again?

**Documentation Task:**  
- Propose a **structured message format** for both data streaming and command control.  
- Explain how the Pico and the laptop should **interpret** incoming messages.  

For example:
```
<SENSOR_TYPE>:<VALUE_1>,<VALUE_2>,<VALUE_3>
```
where `<SENSOR_TYPE>` could be `IMU`, `ENCODER`, or `BATTERY`, and the `<VALUE>`s represent specific sensor readings.

This exercise will help you **think like a systems designer**, structuring real-world communication for robotics applications. Consider this while implementing the tasks in the next two sections.


### **Data the Pico Should Stream to the Laptop**
In a real differential drive robot, the Pico might need to send various types of sensor data to the laptop for monitoring, logging, and control purposes. Some examples include:

| **Data Type**            | **Description**                                        | **Unit / Format**                                    |
|--------------------------|--------------------------------------------------------|------------------------------------------------------|
| **IMU**                  | Orientation (roll, pitch, yaw) and acceleration        | Degrees (°) for angles, m/s² for acceleration        |
| **Motor Speed**          | Measures how fast each motor is spinning               | RPM (Rotations Per Minute)                           |
| **Ultrasonic/Proximity** | Measures distance to obstacles                         | Centimeters (cm) or meters (m)                       |
| **Temperature**          | Tracks heat levels of components                       | Degrees Celsius (°C)                                 |

**Documentation Task:**  
- These are just some examples of potential data sources that you might want to stream to your laptop. Try to think of any others that might be relevant for a mobile robot.
- For each data type, there might be multiple values. For example, the IMU returns X, Y, Z values for the accelerometer and gyroscope. Identify all the values for each source of data.
- Consider the format for what a message containing a particular data point might look like. In this lab, we just had three values separated by commas. But as the amount of data grows, we should label the data values before we send them so that the client can use a string parser to get the desired values.
- Pick three of your data types and define an example message format for sending them over TCP.  

For example:  
A message that sends IMU data might be formatted as:
```
IMU:ROLL=12.5,PITCH=-4.3,YAW=90.0
```

Or potentially you want to send more IMU data than just roll, pitch, and yaw. 
```
IMU:ROLL=12.5,PITCH=-4.3,YAW=90.0,X_GYRO=0.001,Y_GYRO=0.021,Z_GYRO=9.84
```

This is just to get you thinking about how we will implement data streaming from our robot in future labs.

### **Commands the Laptop Should Send to the Pico**
Just as the Pico sends sensor data to the laptop, the laptop might need to **send control commands back to the robot** to direct its movements and behavior. Consider the following possible commands:

| **Command**        | **Description**                                | **Units / Format**               |
|--------------------|----------------------------------------        |----------------------------------|
| **Move Forward**   | Moves the robot a specified distance           | Centimeters as an int or float   |
| **Turn**           | Rotates the robot by a given number of degrees | Degrees or radians               |
| **Set Motor Speed**| Controls the speed of left and right motors    | cm/second or rotations/minute    |
| **Emergency Stop** | Immediately stops all movement                 | NA                               |
| **Request Data**   | Requests specific data from the Pico           | NA                               |

**Documentation Task:**  
- Identify any commands you think would be useful for the laptop to send to the Pico to control the robot.  
- Explain what each command does.  
- Pick three of these commands and define an example format for sending these commands over TCP.  

For example:  
A message that tells the robot to drive forward might look like:
```
MOVE:FORWARD,30
```
This would tell the robot to move forward 30 cm.

Or perhaps you want to control each wheel speed directly
```
MOTOR:LEFT=30,RIGHT=20
```
---

Your report should be comprised of two sections:

1. Implementing TCP communication between your laptop and the pico.
- This section should follow the standard format of the lab reports, but can be shorter than normal due to limited nature of the tasks.
2. Communication documentation.
- This section should outline the tasks in the thinking ahead portion of the lab. Give an introduction explain why we need a well defined communication interface. Follow that with the documentation tasks, and end with a short conclusion summarizing your implementation of the messaging documentation.

Please email the professor or post on Ed Discussion with any questions.