import asyncio
from tcp_client import TCPClient
from live_plotter import LivePlotter

# This function handles user input in an asynchronous loop.
# It reads commands from the user and sends them to the TCP client.
async def user_input_loop(client):
    loop = asyncio.get_event_loop()
    while True:
        cmd = await loop.run_in_executor(None, input, "Enter command: ")
        client.send(cmd)

# This is the main function that sets up the LivePlotter and TCPClient.
# It starts the plot loop, connects to the TCP server, and starts the user input loop.
async def main():
    # Instantiate LivePlotter and start its async plot loop
    liveplotter = LivePlotter()
    asyncio.create_task(liveplotter.run_plot_loop())

    # Callback function to process incoming messages from the Pico.
    def process_incoming(message):
        liveplotter.process_incoming_data(message.strip('Sensor data: (').strip(')'))

    # Get the Pico IP address from the user
    pico_ip = input("Enter Pico IP address (from Pico terminal): ")
    client = TCPClient(host=pico_ip, callback=process_incoming)
    await client.connect()
    await user_input_loop(client)

# Entry point of the script. It runs the main function inside an asyncio event loop.
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print("Client error:", e)
