import serial
import time

# Serial port configuration for Raspberry Pi Zero
# The specific port might vary. Common options:
# - /dev/ttyS0 (mini UART, may require disabling Bluetooth or console)
# - /dev/serial0 (symlink to the primary UART)
# - /dev/ttyAMA0 (PL011 UART, if mini UART is used for Bluetooth)
# Check your Pi Zero's configuration.
SERIAL_PORT = '/dev/serial0'  # Or '/dev/ttyS0'
BAUD_RATE = 115200  # Must match the Pico's baud rate

def main():
    print(f"Attempting to open serial port {SERIAL_PORT} at {BAUD_RATE} baud.")
    
    try:
        # Initialize serial connection
        # Timeout is important for ser.read() if you were receiving,
        # but for sending, it's less critical.
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Serial port {SERIAL_PORT} opened successfully.")
        print("Enter messages to send to the Pico. Type 'exit' to quit.")

        while True:
            message = input("Message: ")
            if message.lower() == 'exit':
                break
            
            # Encode the message to bytes (UTF-8 is common) and send
            # Add a newline character so the Pico can easily distinguish messages
            # if it were to parse them line by line.
            ser.write((message + '\n').encode('utf-8'))
            print(f"Sent: {message}")
            time.sleep(0.1) # Small delay

    except serial.SerialException as e:
        print(f"Error opening or writing to serial port {SERIAL_PORT}: {e}")
    except KeyboardInterrupt:
        print("\nExiting program.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print(f"Serial port {SERIAL_PORT} closed.")

if __name__ == "__main__":
    main()
