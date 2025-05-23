import socket
import threading

class UDPClient:
    def __init__(self, listen_ip='0.0.0.0', listen_port=5005, buffer_size=1024):
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.buffer_size = buffer_size
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.listen_ip, self.listen_port))
        self.running = False

    def start(self, callback):
        """
        Start receiving data. The callback is called with each received message (as bytes).
        """
        self.running = True
        def listen():
            while self.running:
                data, addr = self.sock.recvfrom(self.buffer_size)
                callback(data, addr)
        thread = threading.Thread(target=listen, daemon=True)
        thread.start()

    def stop(self):
        self.running = False
        self.sock.close()
