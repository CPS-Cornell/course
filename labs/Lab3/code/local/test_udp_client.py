# udp_client.py (Python on Laptop)
import time
from udp_client import UDPClient
from live_plotter import LivePlotter
import threading
import asyncio
from data_logger import DataLogger
import sys

async def main():
# Main: create and use the client

    # Create an instance of LivePlotter, uncomment to enable plotting
    #plotter = LivePlotter()

    # Create an instance of DataLogger to store incoming data, uncomment to enable logging
    logger = DataLogger()

    # Callback function to process incoming messages from the Pico.
    def process_incoming(message):
        # TODO: This is where the incoming data is processed. The data can be printed to the console, plotted, or logged.

        # This is an example of how to process incoming data for plotting. Currently,
        # the plotter only handles three values at once example: (roll, pitch, yaw).
        # The incoming data needs to be processed to match this format before plotting.
        #plotter.process_incoming_data(message.strip('(').strip(')'))

        # Alteratively, you can use the logger to store the data in a pickle file or csv for later use.
        # View the data_logger.py file for more information on how these messages should be formatted.
        #logger.process_string(message)

    # TODO: you can hardcode the pico's IP address here or uncomment the input line to enter it manually
    #pico_ip = input("Enter Pico IP address (from Pico terminal): ")

    # Create a UDP client to listen for incoming messages from the Pico
    client = UDPClient(remote_ip='10.49.10.167', listen_port=12345, callback=process_incoming)
    asyncio.create_task(client.start_listening())
    await asyncio.sleep(1) # Give the listener a moment to start up

    # Start the plotter's async loop in a separate thread, uncomment this line to enable plotting
    #asyncio.create_task(plotter.run_plot_loop())
    
    # Send a test command to the server (Pico), currently doesn't do anything on the Pico
    #response = client.send_message("TURN_ON_STREAM", retries=3, timeout=1.0)
    
    # Keep the client running to continue receiving streamed messages.
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        client.stop_listening()
        print("UDPClient stopped.")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print("Client error:", e)
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Saving data before exit...")
        sys.exit(0)