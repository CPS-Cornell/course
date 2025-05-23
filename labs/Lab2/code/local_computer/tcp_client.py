import asyncio

class TCPClient:
    def __init__(self, host, port=1234, callback=None):
        """
        Initialize a TCP client.

        This class creates a client that can connect to a TCP server.

        Args:
            host (str): The hostname or IP address of the server.
            port (int, optional): The port number to connect on. Default is 1234.
            callback (callable, optional): Function to call when data is received. 
                The callback should accept a string argument. Default is None.

        Attributes:
            host (str): The hostname or IP address of the server.
            port (int): The port number to connect on.
            callback (callable or None): Function to call when data is received.
            reader (asyncio.StreamReader or None): Stream reader for receiving data.
            writer (asyncio.StreamWriter or None): Stream writer for sending data.
        """
        self.host = host
        self.port = port
        self.callback = callback
        self.reader = None
        self.writer = None

    async def connect(self):
        """
        Establishes an asynchronous TCP connection to a remote host (Raspberry Pi Pico).
        
        This method attempts to open a connection to the configured host and port,
        creates a reader and writer for communication, and starts a separate
        asynchronous task to listen for incoming messages.
        
        Returns:
            None
            
        Raises:
            Exception: If connection fails, the error is caught and printed to console.
        """
        try:
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            print(f"Connected to Pico at {self.host}:{self.port}")
            asyncio.create_task(self.listen())
        except Exception as e:
            print("Connection error:", e)

    async def listen(self):
        """
        Listens for incoming messages from the server continuously.
        
        This asynchronous method reads line-delimited messages from the connected server
        until the connection is closed or an error occurs. Each received message is decoded
        and passed to the callback function if one is registered.
        
        If the server closes the connection (empty data received) or an exception occurs,
        the connection will be closed.
        
        Returns:
            None
        
        Raises:
            Exception: Any exception that occurs during the reading process will be caught,
                      printed, and the connection will be closed.
        """
        try:
            while True:
                data = await self.reader.readline()  # expecting newline-delimited messages
                if not data:
                    print("Connection closed by server")
                    break
                message = data.decode().strip()
                #print("Received from Pico:", message)
                if self.callback:
                    self.callback(message)
        except Exception as e:
            print("Error while listening:", e)
        finally:
            self.close()

    def send(self, message):
        """
        Sends a message to the connected device.

        This function encodes the message, adds a newline character, and sends it
        over the established TCP connection. It also schedules the writer to drain
        asynchronously to avoid blocking.

        Args:
            message (str): The message to send to the connected device.

        Note:
            If not connected (self.writer is None), a message is printed to the console.
            Any exceptions during sending are caught and printed.
        """
        if self.writer:
            try:
                self.writer.write((message + "\n").encode())
                asyncio.create_task(self.writer.drain())
            except Exception as e:
                print("Error sending message:", e)
        else:
            print("Not connected to Pico.")

    def close(self):
        """
        Close the TCP connection if a writer exists.

        This method will clean up the connection by closing the writer object,
        which releases any resources used for the connection. It also prints a
        message indicating the connection has been closed.

        Returns:
            None
        """
        if self.writer:
            self.writer.close()
            print("Connection closed.")