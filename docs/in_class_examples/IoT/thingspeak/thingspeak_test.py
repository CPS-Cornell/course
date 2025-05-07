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

api_key = '1M0QS9NVDRM4OEB5'
base_url = 'https://api.thingspeak.com/update'

# Define the path to the credentials file
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

connect_to_wifi(ssid_from_file, password_from_file)
time.sleep(1)

for i in range(100):
    print("Sending data: ",i)
    url = f'{base_url}?api_key={api_key}&field1={i}'
    response = urequests.get(url)
    print(response.status_code)
    time.sleep(16)
    gc.collect()