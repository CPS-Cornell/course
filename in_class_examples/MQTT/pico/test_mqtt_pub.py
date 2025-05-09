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
MQTT_TOPIC_TEMPERATURE = 'pico/temperature'
MQTT_TOPIC_PRESSURE = 'pico/pressure'
MQTT_TOPIC_HUMIDITY = 'pico/humidity'

# MQTT Parameters
MQTT_SERVER = config.mqtt_server
MQTT_PORT = 0
MQTT_USER = config.mqtt_username
MQTT_PASSWORD = config.mqtt_password
MQTT_CLIENT_ID = b"raspberrypi_picow"
MQTT_KEEPALIVE = 7200
MQTT_SSL = True   # set to False if using local Mosquitto MQTT broker
MQTT_SSL_PARAMS = {'server_hostname': MQTT_SERVER}

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
        raise  # Re-raise the exception to see the full traceback

def publish_mqtt(topic, value):
    client.publish(topic, value)
    print(topic)
    print(value)
    print("Publish Done")


connect_to_wifi(ssid_from_file, password_from_file)

try:
    # Connect to MQTT broker, start MQTT client
    client = connect_mqtt()
    counter = 0
    while True:
        # Read sensor data
        #temperature, humidity, pressure = get_sensor_readings()

        # Publish as MQTT payload
        publish_mqtt(MQTT_TOPIC_TEMPERATURE, str(counter))
        publish_mqtt(MQTT_TOPIC_PRESSURE, str(counter+1))
        publish_mqtt(MQTT_TOPIC_HUMIDITY, str(counter+2))

        # Delay 10 seconds
        counter = counter + 3
        sleep(10)

except Exception as e:
    print('Error:', e)