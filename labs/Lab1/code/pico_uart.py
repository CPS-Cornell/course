"""
This script provides asynchronous UART communication functionalities for a Pico microcontroller.
It includes the following classes and methods:

Classes:
- AsyncUART: Handles asynchronous UART read and write operations.
  - __init__: Initializes the UART communication.
  - readline: Asynchronously reads a line from the UART interface.
  - write: Writes a message to the UART interface.

- UARTMaster: Manages higher-level UART communication tasks.
  - __init__: Initializes the instance with a UART wrapper and an optional key.
  - simple_rle_compress: Compresses a string using run-length encoding (RLE).
  - encrypt_decrypt: Encrypts or decrypts data using a simple XOR cipher.
  - handshake: Performs a handshake with a device over UART.
  - ping: Sends a ping message and calculates the round-trip time.
  - send_user_input: Prompts the user for input and sends the message over UART.
  - echo: Continuously sends user input via the master object.
  - send_data: Sends data over UART and waits for an ACK response.
  - send_compressed_data: Compresses data using RLE, sends it over UART, and waits for an ACK response.
  - send_compressed_encrypted_data: Compresses and encrypts data, sends it over UART, and waits for an ACK response.
  - test_data_transfer: Tests data transfer by sending uncompressed, compressed, and compressed & encrypted data.
  - run: Runs the handshake, ping, and data transfer tests.

The script initializes the UART interface on specific pins and runs the asynchronous master tasks.
"""

import uasyncio as asyncio
import machine
import time
from message_types import MessageType

class AsyncUART:
    def __init__(self, uart, newline=b'\n'):
        """
        Initializes the UART communication with the specified newline character.

        Args:
            uart: The UART interface to be used for communication.
            newline (bytes, optional): The newline character to be used. Defaults to b'\n'.
        """
        self.uart = uart
        self.newline = newline

    async def readline(self):
        """
        Asynchronously reads a line from the UART interface.

        This function continuously reads data from the UART interface one byte at a time until it encounters a newline character. It then returns the decoded line as a string, excluding the newline character.

        Returns:
            str: The decoded line read from the UART interface.
        """
        buf = b""
        while True:
            if self.uart.any():
                data = self.uart.read(1)
                if data:
                    buf += data
                    if data == self.newline:
                        # Return the decoded line without the newline character.
                        return buf.decode('utf-8').strip()
            await asyncio.sleep(0.01)

    async def write(self, message):
        """
        Writes a message to the UART interface, appending a newline character if not already present.

        Args:
            message (str): The message to be written to the UART interface.
        """
        # Append newline if not already present.
        if not message.endswith("\n"):
            message += "\n"
        self.uart.write(message)

class UARTMaster:
    def __init__(self, uart_wrapper, key=42):
        """
        Initializes the instance with a UART wrapper and an optional key.

        Args:
            uart_wrapper: An instance of a UART wrapper to handle UART communication.
            key (int, optional): A key for encryption or identification purposes. Defaults to 42.
        """
        self.key = key
        self.uart = uart_wrapper

    def simple_rle_compress(self, data):
        """
        Compresses a string using a simple run-length encoding (RLE) algorithm.

        Args:
            data (str): The input string to be compressed.

        Returns:
            str: The compressed string where consecutive characters are replaced 
                 by the character followed by the number of occurrences.
                 For example, 'aaabbc' becomes '3a2b1c'.
        """
        # TODO: Implement the RLE compression algorithm

    def encrypt_decrypt(self, data, key):
        """
        Encrypts or decrypts the given data using a simple XOR cipher.
        
        Args:
            data (str): The input string to be encrypted/decrypted.
            key (int): The key (integer) used for XOR operation.
        
        Returns:
            str: The resulting string after applying the XOR cipher.
        """
        # TODO: Implement the XOR cipher encryption/decryption
        # Hint: You can convert characters to integers using ord() and vice versa using chr()
        #       XOR operation can be performed using the ^ operator


    async def handshake(self):
        """
        Perform a handshake with a device over UART.

        This function sends an initialization message ("INIT") to the device and waits for an acknowledgment ("ACK").
        If no acknowledgment is received within 0.5 seconds, it retries the handshake after a 1-second delay.
        The process continues until an acknowledgment is received.

        Returns:
            None
        """
        print("Starting handshake...")
        while True:
            # Send initialization message.
            await self.uart.write(MessageType.INIT)
            try:
                # Wait up to 0.5 seconds for a reply.
                response = await asyncio.wait_for(self.uart.readline(), timeout=0.5)
            except asyncio.TimeoutError:
                print("No ACK received, retrying handshake...")
                continue
            if response == MessageType.ACK:
                print("Handshake complete.")
                return
            else:
                print("Unexpected response:", response)
                
    async def ping(self):
        """
        Sends a ping message over UART, waits for an echo response, and calculates the round-trip time.

        This asynchronous function sends a ping message containing a timestamp over UART. It then waits for an echo
        response within a 1-second timeout period. If a response is received, it calculates and prints the round-trip time.
        If no response is received or an error occurs, it prints an appropriate message.

        Args:
            None

        Returns:
            None
        """
        # Get a timestamp in milliseconds.
        timestamp = time.ticks_ms()
        message = f"{MessageType.PING}:{timestamp}"
        await self.uart.write(message)
        print("Sent timestamp:", timestamp)
        try:
            # Wait up to 1 second for the echo.
            response = await asyncio.wait_for(self.uart.readline(), timeout=1)
        except asyncio.TimeoutError:
            print("No response to ping.")
            return
        if response.startswith(MessageType.PING):
            try:
                echoed_time = int(response.split(f"{MessageType.PING}:")[1])
                now = time.ticks_ms()
                rtt = time.ticks_diff(now, echoed_time)
                print("Round-trip time (ms):", rtt)
            except Exception as e:
                print("Error processing ping response:", e)
        else:
            print("Unexpected ping response:", response)

    async def send_user_input(self):
        """
        Prompt the user for input and send the message over UART.

        This asynchronous function waits for the user to enter a message,
        then sends the message over UART with a specific message type.
        It also prints the sent message to the console.

        Returns:
            None
        """
        # Prompt user for input and send the message over UART.
        msg = input("Enter message to send over UART: ")
        await self.uart.write(f"{MessageType.ECHO}:{msg}")
        print("Sent message:", msg)

    async def echo(self):
        """
        This asynchronous function continuously sends user input via the master object.

        The function runs an infinite loop where it awaits the completion of the 
        send_user_input method from the master object.
        """
        while True:
            await master.send_user_input()

    async def send_data(self, data):
        """
        Sends data over UART and waits for an ACK response.

        Args:
            data (str): The data to be sent.

        Returns:
            bool: True if ACK received, False otherwise.
        """
        # TODO: Implement the function to send data over UART and wait for an ACK response
        # Hint: Use the MessageType.DATA to indicate the message type
        #       Consider using a try-except block to handle timeouts, 
        #       these timeouts can be set using asyncio.wait_for()
        #       See handshake() for an example

    async def send_compressed_data(self, data):
        """
        Compresses data using RLE, sends it over UART, and waits for an ACK response.

        Args:
            data (str): The data to be compressed and sent.

        Returns:
            bool: True if ACK received, False otherwise.
        """
        # TODO: Implement the function to compress data using RLE, send it over UART, and wait for an ACK response

    async def send_compressed_encrypted_data(self, data, key):
        """
        Compresses and encrypts data, sends it over UART, and waits for an ACK response.

        Args:
            data (str): The data to be compressed, encrypted, and sent.
            key (int): The key for encryption.

        Returns:
            bool: True if ACK received, False otherwise.
        """
        # TODO: Implement the function to compress and encrypt data, send it over UART, and wait for an ACK response

    async def test_data_transfer(self):
        """
        Test the data transfer by sending uncompressed, compressed, and compressed & encrypted data,
        and measure the transmission times for each.
        This function performs the following steps:
        1. Reads a large block of data from "data.txt".
        2. Sends the uncompressed data and measures the transmission time.
        3. Sends the compressed data and measures the transmission time.
        4. Sends the compressed and encrypted data and measures the transmission time.
        The transmission times for each step are printed to the console.
        Args:
            None
        Returns:
            None
        """
        # TODO: Implement the function to test data transfer by sending uncompressed, compressed, and compressed & encrypted data
        # Hint: Start by reading the large block of data from "data.txt"
        #       Use the send_data, send_compressed_data, and send_compressed_encrypted_data methods

    async def run(self):
        #await self.handshake()
        #await self.ping()
        #await self.test_data_transfer()


# Initialize UART on pins 16 (TX) and 17 (RX) at 115200 baud.
uart = machine.UART(0, baudrate=115200, tx=machine.Pin(16), rx=machine.Pin(17))
time.sleep(2)  # Allow hardware and connection to settle.
print("Pico UART initialized.")

uart_wrapper = AsyncUART(uart)
master = UARTMaster(uart_wrapper)

# Run the asynchronous master tasks.
asyncio.run(master.run())

