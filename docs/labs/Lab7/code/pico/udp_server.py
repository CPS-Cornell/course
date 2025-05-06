import socket
import network
import time

class UDPServer:
    def __init__(self, target_ip, target_port=5005):
        self.target_ip = target_ip
        self.target_port = target_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data: str):
        # Data should be a string or bytes
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.sock.sendto(data, (self.target_ip, self.target_port))


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