import uasyncio as asyncio
from tcp_server import TCPServer
from machine import Pin
from imu import IMU
import time

# Dummy WiFi credentials – replace with your own.
SSID = "RedRover"
PASSWORD = ""
PORT = 1234

#TODO: Delare the LED pin and the IMU object

# Dummy sensor reading function – replace with your actual sensor code.
def read_sensor():
    #TODO: Read the IMU sensor data and return the roll, pitch, and yaw values

    # For now, return random values.
    import random
    return (random.random(), random.random(), random.random()) 

# Callback function for incoming messages from the client.
def process_message(message):
    print("Processing incoming message on Pico:", message)
    #TODO: Process the incoming message and control the LED
    # The message will be either "ON" or "OFF"
    # Turn the LED on if the message is "ON" and off if it is "OFF"

async def main():
    tcp_server = TCPServer(callback=process_message)
    # Start the server task.
    asyncio.create_task(tcp_server.start())

    # This loop hangs until a connection is established
    while not tcp_server.is_connected():
        await asyncio.sleep(.1)  # Adjustable frequency

    # Main loop: read sensor data and send it to the client.
    while True:
        sensor_data = read_sensor()
        #print("Sending sensor data:", sensor_data)
        await tcp_server.send("Sensor data: " + str(sensor_data))
        await asyncio.sleep(1) #Adjustable frequency keep this at at least .5 seconds or higher

# Run the main loop.
try:
    asyncio.run(main())
except Exception as e:
    print("Main error:", e)
