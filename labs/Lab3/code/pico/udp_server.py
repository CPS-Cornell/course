# udp_server.py (for Pico with MicroPython)
import time
import uasyncio as asyncio
import socket
import network

class UDPServer:
    def __init__(self, client_ip, local_ip='0.0.0.0', port=12345):
        self.local_ip = local_ip
        self.client_ip = client_ip
        self.port = port
        # Create and bind a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.local_ip, self.port))
        self.sock.setblocking(False)  # set socket to non-blocking mode
        print("UDPServer initialized on {}:{}".format(self.local_ip, self.port))
    
    def send_message(self, message):
        """
        Sends a message (as a string) to the given client address.
        The message is sent without waiting for a response.
        :param message: String to send.
        :param client_addr: Tuple (client_ip, client_port)
        """
        try:
            self.sock.sendto(message.encode('utf-8'), (self.client_ip, self.port))
            print("Sent message to {}: {}".format((self.client_ip, self.port), message))
        except Exception as e:
            print("Error sending message:", e)
    
    async def listen(self):
        """
        Asynchronously listens for incoming UDP messages.
        When a message is received, it prints it and sends an ACK back.
        """
        print("UDPServer listening for incoming messages...")
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)  # non-blocking call
                if data:
                    message = data.decode('utf-8')
                    print("Received from {}: {}".format(addr, message))
                    # Send an acknowledgement back to the sender
                    ack_message = "ACK: " + message
                    self.send_message(ack_message)
            except OSError:
                # No data available; yield control to allow other tasks to run
                await asyncio.sleep(0.01)
    
    def run(self):
        """
        Starts the asynchronous event loop to run the UDP listener.
        """
        loop = asyncio.get_event_loop()
        loop.create_task(self.listen())
        loop.run_forever()

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

# Example usage on Pico:
# server = UDPServer(port=12345)
# server.run()
