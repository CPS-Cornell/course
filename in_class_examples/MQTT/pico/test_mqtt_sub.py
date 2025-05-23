#username = 'cps_test'
#password = 'CPS_test1'
#cluster_id = 'b054c76b079f40a7b527e8031fcd14b9'
#URL = 'b054c76b079f40a7b527e8031fcd14b9.s1.eu.hivemq.cloud'
#TSL MQTT URL = 'b054c76b079f40a7b527e8031fcd14b9.s1.eu.hivemq.cloud:8883'
#TLS Websocket URL = 'b054c76b079f40a7b527e8031fcd14b9.s1.eu.hivemq.cloud:8884/mqtt'

import network
import time
import urequests
from simple import MQTTClient
import config
from time import sleep
import machine

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

credentials_file = 'wifi_credentials.txt'
ssid_from_file = None
password_from_file = "" # Default to empty password

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
    # Handle file not found or permission errors
    print(f"Error: Could not open or read file {credentials_file}: {e}")
except Exception as e:
    # Handle other potential errors during file processing
    print(f"An unexpected error occurred while reading {credentials_file}: {e}")

# Constants for MQTT Topics
MQTT_TOPIC_LED = 'pico/led'

# MQTT Parameters
MQTT_SERVER = config.mqtt_server
MQTT_PORT = 0
MQTT_USER = config.mqtt_username
MQTT_PASSWORD = config.mqtt_password
MQTT_CLIENT_ID = b"raspberrypi_picow"
MQTT_KEEPALIVE = 7200
MQTT_SSL = True   # set to False if using local Mosquitto MQTT broker
MQTT_SSL_PARAMS = {'server_hostname': MQTT_SERVER}

led = machine.Pin('LED', machine.Pin.OUT)  # Define the LED pin

# Connect to MQTT Broker
def connect_mqtt():
    try:
        client = MQTTClient(client_id=MQTT_CLIENT_ID,
                            server=MQTT_SERVER,
                            port=MQTT_PORT,
                            user=MQTT_USER,
                            password=MQTT_PASSWORD,
                            keepalive=MQTT_KEEPALIVE,
                            ssl=MQTT_SSL,
                            ssl_params=MQTT_SSL_PARAMS)
        client.connect()
        return client
    except Exception as e:
        print('Error connecting to MQTT:', e)

# Subcribe to MQTT topics
def subscribe(client, topic):
    client.subscribe(topic)
    print('Subscribe to topic:', topic)
    
# Callback function that runs when you receive a message on subscribed topic
def my_callback(topic, message):
    # Perform desired actions based on the subscribed topic and response
    print('Received message on topic:', topic)
    print('Response:', message)
    # Check the content of the received message
    if message == b'ON':
        print('Turning LED ON')
        led.value(1)  # Turn LED ON
    elif message == b'OFF':
        print('Turning LED OFF')
        led.value(0)  # Turn LED OFF
    else:
        print('Unknown command')

connect_to_wifi(ssid_from_file, password_from_file)
    
try:
    # Initialize Wi-Fi
    # Connect to MQTT broker, start MQTT client
    client = connect_mqtt()
    client.set_callback(my_callback)
    subscribe(client, MQTT_TOPIC_LED)
    
    # Continuously checking for messages
    while True:
        sleep(5)
        client.check_msg()
        print('Loop running')
except Exception as e:
    print('Error:', e)