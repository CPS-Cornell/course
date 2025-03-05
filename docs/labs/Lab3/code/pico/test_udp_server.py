import uasyncio as asyncio
import time
from udp_server import UDPServer, connect_to_wifi
import random
from rangefinder import Rangefinder  # Import Rangefinder
from imu import IMU
from machine import I2C, Pin
from reflectance import Reflectance 
from vcnl4040 import VCNL4040


# Network settings - replace with your values
WIFI_SSID = "RedRover"    # Your WiFi network name
WIFI_PASSWORD = ""        # Your WiFi password
LAPTOP_IP = "10.49.12.24" # Your laptop's IP address

connect_to_wifi(WIFI_SSID, WIFI_PASSWORD)

async def main():
    # Main: create and run the server
    server = UDPServer(LAPTOP_IP)
    asyncio.create_task(server.listen())
    

    #TODO: This is where the sensors are declared
    # Note, you need to disconnect the reflectance sensor and use that cable for the proximity sensor
    #i2c = I2C(id=1, scl=Pin(19), sda=Pin(18), freq=400000)
    #rangefinder = Rangefinder(trigger_pin=20, echo_pin=21)  # Create Rangefinder object
    #imu = IMU(i2c)
    #reflect = Reflectance()
    #intensity_sensor = VCNL4040(i2c)

    while True:
        # Example rage finder usage
        #ultr_distance = rangefinder.distance()  # Get distance measurement

        # Example proximity sensor usage
        #intens_distance = intensity_sensor.proximity
        #intens_distance = intensity_sensor.light

        # Example of how to format messages for the plotter
        #server.send_message(f"({imu.get_roll()}, {imu.get_pitch()}, {imu.get_yaw()})")
        #server.send_message(f"({reflect.get_left()}, {reflect.get_right()}, {0})")

        # Example of how to format messages for the data logger
        #server.send_message(f"TIME:{time.ticks_ms()},PROX:{intensity_sensor.proximity},INTENSE:{intensity_sensor.lux},RANGE:{rangefinder.distance()}")

        # This sleep function is used to control the rate at which data is collected and messages are sent
        await asyncio.sleep(0.3)  # Sleep for 300ms

if __name__ == '__main__':
    asyncio.run(main())