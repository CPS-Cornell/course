import uasyncio as asyncio
import network
import time

class TCPServer:
    def __init__(self, port=1234, callback=None):
        self.port = port
        self.callback = callback
        self.client_reader = None
        self.client_writer = None
        self.server = None

    async def start(self):
        # Connect to WiFi and print IP address.
        ip = self.connect_wifi()
        print("Pico IP Address:", ip)
        while True:
            try:
                print("Waiting for a client connection on port", self.port)
                # Start a server that handles one connection at a time.
                self.server = await asyncio.start_server(self.handle_client, "0.0.0.0", self.port)
                await self.server.wait_closed()  # Blocks until the server is closed
            except Exception as e:
                print("Server error:", e)
                await asyncio.sleep(1)  # Wait briefly before restarting the server.

    async def handle_client(self, reader, writer):
        print("Client connected")
        self.client_reader = reader
        self.client_writer = writer
        try:
            while True:
                data = await reader.readline()  # using newline as delimiter
                if not data:
                    print("Client disconnected")
                    break
                message = data.decode().strip()
                print("Received:", message)
                if self.callback:
                    self.callback(message)
        except Exception as e:
            print("Error handling client:", e)
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
            self.client_reader = None
            self.client_writer = None
            print("Connection closed. Reentering waiting state.")

    def send(self, message):
        if self.client_writer:
            try:
                self.client_writer.write((message + "\n").encode())
                #asyncio.create_task(self.client_writer.drain())
                await self.client_writer.drain()
            except Exception as e:
                print("Error sending message:", e)
        else:
            print("No client connected to send message.")

    def is_connected(self):
        # Returns True if a TCP client is connected
        return self.client_writer is not None

    def connect_wifi(self, ssid="RedRover", password=""):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print("Connecting to WiFi...")
            wlan.connect(ssid, password)
            while not wlan.isconnected():
                time.sleep(1)
        return wlan.ifconfig()[0]