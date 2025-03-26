import asyncio
import serial_asyncio
from message_types import MessageType

class AsyncUART:
    def __init__(self, port, baudrate=115200):
        """
        Initializes the serial communication with the specified port and baudrate.

        Args:
            port (str): The serial port to use for communication.
            baudrate (int, optional): The baud rate for the serial communication. Defaults to 115200.
        """
        self.port = port
        self.baudrate = baudrate
        self.reader = None
        self.writer = None

    async def open(self):
        """
        Opens an asynchronous serial connection.

        This method initializes the reader and writer attributes by establishing a serial connection
        using the specified port and baudrate.

        Attributes:
            reader (StreamReader): The stream reader for the serial connection.
            writer (StreamWriter): The stream writer for the serial connection.

        Raises:
            SerialException: If the serial connection cannot be established.
        """
        self.reader, self.writer = await serial_asyncio.open_serial_connection(url=self.port,
                                                                               baudrate=self.baudrate)
    async def readline(self):
        """
        Asynchronously reads a line from the reader, decodes it using UTF-8, and returns the stripped string.
        
        Returns:
            str: The decoded and stripped line if successful.
            None: If the line cannot be decoded as UTF-8.
        
        Raises:
            UnicodeDecodeError: If the line contains non-UTF-8 data.
        """
        line = await self.reader.readline()
        try:
            return line.decode('utf-8').strip()
        except UnicodeDecodeError:
            print("Received non-UTF-8 data, ignoring:", line)
            return None  # Or handle as needed

    async def write(self, message):
        # This function writes a message to an asynchronous writer, ensuring it ends with a newline character.
        """
        Write a message to the writer asynchronously.

        This method ensures that the message ends with a newline character before writing it to the writer.
        The message is encoded in UTF-8 format before being written.

        Args:
            message (str): The message to be written.

        Returns:
            None
        """
        if not message.endswith("\n"):
            message += "\n"
        self.writer.write(message.encode('utf-8'))
        await self.writer.drain()

class UARTSlave:
    def __init__(self, uart_wrapper):
        self.uart = uart_wrapper

    def decompress(self, data):
        # Decompress data compressed with simple RLE.
        result = ""
        i = 0
        while i < len(data):
            count_str = ""
            # Read number (could be multiple digits)
            while i < len(data) and data[i].isdigit():
                count_str += data[i]
                i += 1
            if not count_str:
                break
            count = int(count_str)
            if i < len(data):
                char = data[i]
                i += 1
                result += char * count
        return result

    def encrypt_decrypt(self, data, key):
        # XOR cipher: encrypts or decrypts the input data using the given key.
        return ''.join(chr(ord(c) ^ key) for c in data)

    async def handle_messages(self):
        """
        Handles incoming UART messages and responds based on the message type.
        The function continuously reads messages from the UART interface and processes them:
        - If the message is "INIT", it sends back "ACK".
        - If the message starts with "PING:", it echoes back the timestamp message.
        - If the message starts with "ECHO:", it sends back "ACK".
        - If the message starts with "DATA:", it acknowledges receipt and prints the length of the uncompressed data.
        - If the message starts with "ENC:", it acknowledges receipt and prints the length of the encrypted data.
        - If the message starts with "CMPD:", it acknowledges receipt and prints the length of the compressed data.
        - If the message starts with "CMPENC:", it acknowledges receipt and prints the length of the compressed encrypted data.
        The function includes a small delay (0.01 seconds) between iterations to prevent blocking.
        Note:
        - This function is designed to run indefinitely in an asynchronous event loop.
        """
        print("UART Slave started. Waiting for messages...")
        while True:
            message = await self.uart.readline()
            if message == MessageType.INIT:
                await self.uart.write(MessageType.ACK)
                print("Received INIT, Sent: ACK")
            elif message.startswith(MessageType.PING):
                # Immediately echo back the timestamp message.
                await self.uart.write(message)
                print("Received PING, Echoed back timestamp.")
            elif message.startswith(MessageType.ECHO):
                await self.uart.write("RCVD")
                print("Received Echo: ", message)
            elif message.startswith(MessageType.DATA):
                data = message[5:]  # Remove the "DATA:" prefix
                await self.uart.write(MessageType.ACK)
                print("Received data length:", len(data))
            elif message.startswith(MessageType.ENC):
                data = message[4:]  # Remove the "ENC:" prefix
                await self.uart.write(MessageType.ACK)
                print("Received encrypted data length:", len(data))
            elif message.startswith(MessageType.CMPD):
                data = message[5:]  # Remove the "CMPD:" prefix
                decompressed = self.decompress(data)
                await self.uart.write(MessageType.ACK)
                #print("Received compressed data length:", len(decompressed))
                print("Received compressed data:", decompressed)
            elif message.startswith(MessageType.CMPENC):
                data = message[7:]  # Remove the "CMPENC:" prefix
                # Decrypt using key 42 then decompress.
                decrypted = self.encrypt_decrypt(data, 42)
                decompressed = self.decompress(decrypted)
                await self.uart.write(MessageType.ACK)
                #print("Received compressed encrypted data length:", len(decompressed))
                print("Received compressed encrypted data: ", decompressed)
            await asyncio.sleep(0.01)

async def main():
    # Adjust the port as needed (commonly /dev/serial0 or /dev/ttyAMA0).
    uart_wrapper = AsyncUART('/dev/serial0', baudrate=115200)
    await uart_wrapper.open()
    slave = UARTSlave(uart_wrapper)
    await slave.handle_messages()

if __name__ == '__main__':
    asyncio.run(main())
