# Using a Raspberry Pi Pico W to Send Data to ThingSpeak

---

## What is ThingSpeak?

**ThingSpeak** is a cloud-based platform designed for the Internet of Things (IoT) applications. It allows you to:

- **Collect** data from sensors or devices.
- **Store** and **analyze** the data.
- **Visualize** the data through graphs and dashboards.
- **Trigger actions** based on data or events.

ThingSpeak is popular for DIY IoT projects because it has a free tier and easy integration with microcontrollers like Arduino, ESP8266, and now the Raspberry Pi Pico W.

---

## How ThingSpeak Works

The basic workflow is:

1. Create a "**channel**" on ThingSpeak.
2. Send HTTP requests (GET or POST) containing your data and a unique **API key** to the ThingSpeak server.
3. ThingSpeak stores and displays your data in graphs.

Every channel can have multiple **fields** (like temperature, humidity, etc.), and you can control the access (public or private).

---

## Setting Up ThingSpeak

### Step 1: Create a MathWorks Account

1. Go to [https://thingspeak.com](https://thingspeak.com).
2. Click on **Sign Up** (top-right corner).
3. You will be redirected to MathWorks to create an account.
   - Provide an email address.
   - Create a password.
   - Fill out any required profile information.

**Note**: If you already have a MathWorks account (for MATLAB, Simulink, etc.), you can use it.

**Important**: If you sign up using a **cornell.edu** email address, MathWorks will require you to sign in using your **NetID** and **two-factor authentication**.

### Step 2: Create a New Channel

1. After signing in to ThingSpeak, click on your profile picture (top-right) and choose **My Channels**.
2. Click **New Channel**.
3. Fill in the channel name (e.g., "Pico W Test") and add Field Names (e.g., Field 1 = "Temperature").
4. Make sure to check the box for **Enable Fields** that you plan to use.
5. Click **Save Channel**.

#### Important:

- After creating the channel, go to the **API Keys** tab.
- Copy the **Write API Key**. You'll use this key to send data from your Pico.

---

## Programming the Raspberry Pi Pico W

### Prerequisites

- Raspberry Pi Pico W.
- Thonny IDE (or any MicroPython IDE).
- MicroPython firmware installed on your Pico W.
- Internet-connected Wi-Fi network.

### Install Required Libraries

No external libraries are required other than standard MicroPython libraries (`network`, `urequests`, and `gc`). If your Pico doesn't have `urequests`, upload it manually.

### Code Explanation

The provided Python script [`thingspeak_test.py`](thingspeak/thingspeak_test.py) is designed to run on a Raspberry Pi Pico W and perform the following actions:

1.  **Import Libraries**:
    *   `network`: For managing network connections (Wi-Fi).
    *   `time`: For adding delays (e.g., waiting for connection, rate-limiting API calls).
    *   `urequests`: A lightweight version of the `requests` library for making HTTP requests.
    *   `gc`: For garbage collection, helping to manage memory on the microcontroller.

2.  **Wi-Fi Connection (`connect_to_wifi` function)**:
    *   This helper function takes an SSID (Wi-Fi network name) and an optional password.
    *   It activates the Pico W's Wi-Fi station interface.
    *   If not already connected, it attempts to connect to the specified Wi-Fi network.
    *   It includes a loop that waits up to 20 seconds for the connection to establish, printing status messages.
    *   Upon successful connection, it prints the IP address.
    *   It returns `True` if connected, `False` otherwise.

3.  **ThingSpeak Configuration**:
    *   `api_key`: **You must replace `'YOUR_THINGSPEAK_WRITE_API_KEY'` with your actual ThingSpeak Channel Write API Key.** This key authorizes your script to send data to your channel.
    *   `base_url`: The base URL for the ThingSpeak API endpoint used to update channel data.

4.  **Loading Wi-Fi Credentials**:
    *   `credentials_file = 'wifi_credentials.txt'`: The script expects a file named `wifi_credentials.txt` in the Pico W's root directory.
    *   This file should contain two lines:
        *   Line 1: Your Wi-Fi SSID
        *   Line 2: Your Wi-Fi Password (if your network has no password, this line can be blank or omitted, but the script expects it to try and read it).
    *   It attempts to open and read these credentials.
    *   Includes `try-except` blocks to handle potential errors like the file not being found (`OSError`) or other issues during file reading.

5.  **Connecting to Wi-Fi**:
    *   Calls the `connect_to_wifi` function using the SSID and password read from the `wifi_credentials.txt` file.
    *   Pauses for 1 second after attempting connection.

6.  **Sending Data to ThingSpeak (Main Loop)**:
    *   The script enters a `for` loop that iterates 100 times.
    *   In each iteration:
        *   It prints a message indicating the data point being sent (e.g., "Sending data: 0", "Sending data: 1", etc.).
        *   It constructs the full URL for the ThingSpeak API call. This URL includes:
            *   The `base_url`.
            *   Your `api_key`.
            *   The data to be sent, formatted as `field1={i}`, where `i` is the current loop counter value. This means it will send the numbers 0 through 99 to `field1` of your ThingSpeak channel.
        *   `response = urequests.get(url)`: It makes an HTTP GET request to the constructed URL.
        *   `print(response.status_code)`: It prints the HTTP status code of the response (e.g., 200 for success).
        *   `time.sleep(16)`: It pauses for 16 seconds. This is crucial because the free version of ThingSpeak has a rate limit of approximately one update every 15 seconds per channel. Sending data faster than this will result in errors.
        *   `gc.collect()`: It calls the garbage collector to free up any unused memory, which is good practice on memory-constrained devices like the Pico.

This script provides a basic framework for reading Wi-Fi credentials from a file, connecting to a network, and periodically sending data to a ThingSpeak channel.

### Example Code

```python
import network
import time
import urequests
import gc

# Helper function to connect to WiFi
def connect_to_wifi(ssid, password=""):
    """Connect to the WiFi network with the given SSID and password."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print(f"Connecting to {ssid}...")
        wlan.connect(ssid, password)

        # Wait for connection
        max_wait = 20
        while max_wait > 0:
            if wlan.isconnected():
                break
            max_wait -= 1
            print("Waiting for connection...")
            time.sleep(1)

        if wlan.isconnected():
            print("Connected to WiFi")
            print("IP address:", wlan.ifconfig()[0])
            return True
        else:
            print("Failed to connect to WiFi")
            return False
    else:
        print("Already connected to WiFi")
        print("IP address:", wlan.ifconfig()[0])
        return True

api_key = 'YOUR_THINGSPEAK_WRITE_API_KEY'  # Replace with your Write API Key
base_url = 'https://api.thingspeak.com/update'

# Define the path to the credentials file
credentials_file = 'wifi_credentials.txt'
ssid_from_file = None
password_from_file = ""  # Default to empty password

try:
    with open(credentials_file, 'r') as f:
        lines = f.readlines()
        # Read SSID from the first line
        if len(lines) >= 1:
            ssid_from_file = lines[0].strip()
        # Read password from the second line
        if len(lines) >= 2:
            password_from_file = lines[1].strip()

        if ssid_from_file:
            print(f"Successfully read SSID '{ssid_from_file}' from {credentials_file}")
        else:
            print(f"Warning: Could not read a valid SSID from {credentials_file}")

except OSError as e:
    print(f"Error: Could not open or read file {credentials_file}: {e}")
except Exception as e:
    print(f"An unexpected error occurred while reading {credentials_file}: {e}")

connect_to_wifi(ssid_from_file, password_from_file)
time.sleep(1)

for i in range(100):
    print("Sending data:", i)
    url = f'{base_url}?api_key={api_key}&field1={i}'
    response = urequests.get(url)
    print(response.status_code)
    time.sleep(16)
    gc.collect()

```