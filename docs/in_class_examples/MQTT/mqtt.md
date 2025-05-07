# Using MQTT with Raspberry Pi Pico W, MicroPython, and HiveMQ

This tutorial will guide you through setting up MQTT communication on a Raspberry Pi Pico W using MicroPython and HiveMQ as the broker. We'll walk through creating a HiveMQ account, setting up a new broker, creating user credentials, and connecting your Pico W to it.

## What is MQTT?

MQTT (Message Queuing Telemetry Transport) is a lightweight publish-subscribe network protocol that transports messages between devices. It is often used in IoT (Internet of Things) applications due to its efficiency and low overhead.

## What is HiveMQ?

HiveMQ is a cloud-based MQTT broker platform that allows devices to publish and subscribe to topics easily. They provide a free "HiveMQ Cloud" service that we can use for development and testing.

---

# Step 1: Create a HiveMQ Account and Set Up a Broker

1. **Go to [HiveMQ Cloud](https://www.hivemq.com/mqtt-cloud-broker/)**.
2. **Sign Up for an Account**: Click on "Get Started for Free" and create an account.
3. **Create a New Cluster**:
   - After signing in, click "Create Cluster".
   - Select "Free Tier".
   - Choose a cluster name, region, and click "Create Cluster".
4. **Copy Broker Information**:
   - Once the cluster is created, you will be given:
     - Hostname (e.g., `your-cluster.hivemq.cloud`)
     - Port: Use port `8883` (TLS/SSL secured)

# Step 2: Set Up MQTT User Credentials

1. **Navigate to Access Management**:
   - Go to the "Access Management" tab.
2. **Create New User**:
   - Click "Create User".
   - Set a username and password for connecting clients.
   - Save these credentials; you will need them for the Pico W connection.
   - **Tip**: You may want to create a second user account for logging in and viewing the data separately from the device that is publishing or subscribing.

---

# Step 3: Script Walkthrough

This step provides a detailed walkthrough of the two MicroPython scripts you'll use: the publish script ([`test_mqtt_pub.py`](pico/test_mqtt_pub.py)) and the subscribe script ([`test_mqtt_sub.py`](pico/test_mqtt_sub.py)). Each section describes what the code is doing and the expected outcome when running it on your Pico W. You will also need to the files [`simple.py`](pico/simple.py) and [`robust`](pico/robust.py).

## 3.1 Publish Script ([`test_mqtt_pub.py`](pico/test_mqtt_pub.py))

The publish script performs the following actions:

1. **Wi‑Fi Connection**: Reads your SSID and password from `wifi_credentials.txt` and connects to the network using the `network` module. It reports success or failure and prints the assigned IP address.
2. **MQTT Client Setup**: Imports MQTT parameters (server, port, user, password, SSL settings) from `config.py` and establishes a secure connection to the HiveMQ broker using `MQTTClient` from `simple.py`.
3. **Publishing Loop**: Enters an infinite loop where it:
   - Constructs payloads for temperature, pressure, and humidity topics using a simple counter for demonstration.
   - Publishes each payload to its corresponding topic (`pico/temperature`, `pico/pressure`, `pico/humidity`).
   - Prints the topic and payload to the REPL for debugging.
   - Increments the counter values and waits 10 seconds before repeating.

**Expected Outcome**: After running `test_mqtt_pub.py`, your Pico W should connect to Wi‑Fi, then publish three messages every 10 seconds to the HiveMQ broker. You’ll see logs in the serial console and can verify messages appear in the HiveMQ Web Client under the respective topics.

## 3.2 Subscribe Script ([`test_mqtt_sub.py`](pico/test_mqtt_sub.py))

The subscribe script performs the following actions:

1. **Wi‑Fi Connection**: Similarly reads Wi‑Fi credentials from `wifi_credentials.txt` and connects using the `network` module, printing status messages and IP address.
2. **MQTT Client Setup**: Loads the same MQTT connection parameters from `config.py`, connects securely to HiveMQ, and sets up a callback function (`my_callback`) to handle incoming messages.
3. **Callback Definition**: Defines `my_callback(topic, message)` to:
   - Print the received topic and message.
   - Control the onboard LED (`machine.Pin('LED')`) by turning it ON when the message payload is `b'ON'` and OFF when `b'OFF'`.
4. **Subscription and Loop**:
   - Subscribes to the `pico/led` topic.
   - Enters a loop where every 5 seconds it calls `client.check_msg()` to process incoming messages and logs that the loop is running.

**Expected Outcome**: When running `test_mqtt_sub.py`, your Pico W will subscribe to `pico/led`. Sending messages (`ON` or `OFF`) to this topic from HiveMQ or another client will toggle the Pico W’s onboard LED accordingly, with feedback printed to the console.

---

# Step 4: Testing

1. **Testing `test_mqtt_pub.py` (Publishing Data)**:
    - Run `test_mqtt_pub.py` on your Pico W.
    - Open your HiveMQ Cloud Console in a web browser.
    - Navigate to the "MQTT Web Client".
    - Connect to your broker using the **second set of user credentials** you created (or create one now if you haven't). This allows you to observe the data without interfering with the Pico's connection.
    - In the "Subscriptions" section of the Web Client, add subscriptions for the following topics:
      - `pico/temperature`
      - `pico/pressure`
      - `pico/humidity`
    - You should see messages appearing under these topics, with values incrementing every 10 seconds, as sent by your Pico W.

2. **Testing `test_mqtt_sub.py` (Subscribing to Commands)**:
    - Stop the previous script and run `test_mqtt_sub.py` on your Pico W.
    - In the HiveMQ MQTT Web Client (still connected with your second user credentials):
      - Go to the "Publish" section.
      - Set the "Topic" to `pico/led`.
      - In the "Message" field, type `ON` and click "Publish". Observe the onboard LED on your Pico W; it should turn on.
      - Change the "Message" to `OFF` and click "Publish". The LED should turn off.
    - You will also see log messages in your Pico W's REPL console confirming the received messages and LED state changes.

---

# Troubleshooting

- **Connection Refused**: Make sure Wi-Fi credentials, MQTT username, and password are correct.
- **SSL Errors**: Ensure you are connecting on port `8883` with SSL enabled.
- **Cannot Import `umqtt.simple`**: Upload the `umqtt` library manually to your Pico W.
