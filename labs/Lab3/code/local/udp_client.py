# udp_client.py (for laptop using Python)
import socket
import threading
import queue
import asyncio

class UDPClient:
    def __init__(self, listen_ip='0.0.0.0', listen_port=12345,
                 remote_ip='10.49.10.167', remote_port=12345, callback=None):
        """
        :param listen_ip: Local IP to bind the listener (default: all interfaces)
        :param listen_port: Local port to listen on for incoming UDP messages.
        :param remote_ip: Pico’s IP address.
        :param remote_port: Pico’s port number.
        :param callback: A function that will be called with each received message.
        """
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.callback = callback
        
        # Create a UDP socket for listening
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listen_sock.bind((self.listen_ip, self.listen_port))
        self.listen_sock.settimeout(0.5)
        
        # Create a separate UDP socket for sending command messages.
        self.cmd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cmd_sock.settimeout(1.0)
        
        self.listening = False

        # Queue to hold command responses (ACKs)
        self.response_queue = queue.Queue()
    
    def start_listening(self):
        """
        Starts a background thread that continuously listens for incoming UDP messages.
        Each message is passed to the callback function (if provided).
        """
        self.listening = True
        thread = threading.Thread(target=self.listen_loop, daemon=True)
        thread.start()

    async def start_listening(self):
        self.listening = True
        loop = asyncio.get_running_loop()
        while self.listening:
            try:
                data, addr = await loop.sock_recvfrom(self.listen_sock, 1024)
                message = data.decode('utf-8')
                print(f"Received from {addr}: {message}")
                # If this message looks like an ACK, place it in the queue
                if message.startswith("ACK:"):
                    await self.response_queue.put(message)
                elif self.callback:
                    self.callback(message)
            except Exception as e:
                print("Error in listening loop:", e)

    async def send_message(self, message, retries=3, timeout=1.0):
        for attempt in range(retries):
            try:
                await self.cmd_sock.sendto(message.encode('utf-8'), (self.remote_ip, self.remote_port))
                print(f"Sent command: {message} to {self.remote_ip}:{self.remote_port}")

                # Wait for a matching ACK from the queue
                try:
                    ack = await asyncio.wait_for(self.response_queue.get(), timeout)
                    if message in ack:  # Simple matching; refine as needed
                        print(f"Received ACK: {ack}")
                        return ack
                except asyncio.TimeoutError:
                    print(f"No ACK received, retrying... (attempt {attempt + 1}/{retries})")
            except Exception as e:
                print("Error in send_message:", e)
        print(f"Failed to receive ACK after {retries} attempts.")
        return None
            

    #def listen_loop(self):
    #    print("UDPClient listening for incoming messages on {}:{}".format(self.listen_ip, self.listen_port))
    #    while self.listening:
    #        try:
    #            data, addr = self.listen_sock.recvfrom(1024)
    #            message = data.decode('utf-8')
    #            print("Received from {}: {}".format(addr, message))
    #            # If this message looks like an ACK, place it in the queue
    #            if message.startswith("ACK:"):
    #                self.response_queue.put(message)
    #            elif self.callback:
    #                self.callback(message)
    #        except socket.timeout:
    #            continue
    #        except Exception as e:
    #            print("Error in listening loop:", e)

    #def send_message(self, message, retries=3, timeout=1.0):
    #    """
    #    Sends a message to the Pico and waits for an ACK response.
    #    Uses the response_queue to capture the ACK.
    #    """
    #    for attempt in range(retries):
    #        try:
    #            # Send the command message
    #            self.cmd_sock.sendto(message.encode('utf-8'), (self.remote_ip, self.remote_port))
    #            print("Sent command: {} to {}:{}".format(message, self.remote_ip, self.remote_port))
    #            
    #            # Wait for a matching ACK from the queue
    #            start_time = time.time()
    #            while time.time() - start_time < timeout:
    #                try:
    #                    # Non-blocking get with small timeout
    #                    ack = self.response_queue.get(timeout=0.1)
    #                    # Check if this ACK corresponds to the command (could use identifiers here)
    #                    if message in ack:  # Simple matching; refine as needed
    #                        print("Received ACK: {}".format(ack))
    #                        return ack
    #                except queue.Empty:
    #                    continue
    #            print("No ACK received, retrying... (attempt {}/{})".format(attempt+1, retries))
    #        except Exception as e:
    #            print("Error in send_message:", e)
    #    print("Failed to receive ACK after {} attempts.".format(retries))
    #    return None
    
    def stop_listening(self):
        """
        Stops the background listening thread.
        """
        self.listening = False

# Example usage on laptop:
# def my_callback(msg):
#     print("Callback received message:", msg)
#
# client = UDPClient(remote_ip='10.49.10.167', listen_port=12345, callback=my_callback)
# client.start_listening()
#
# # To send a command (with retries for acknowledgement):
# response = client.send_message("TURN_ON_STREAM", retries=3, timeout=1.0)
# print("Final response:", response)
