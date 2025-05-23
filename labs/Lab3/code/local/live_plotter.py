#import threading
import asyncio
from collections import deque
import numpy as np  
import matplotlib.pyplot as plt
import asyncio  # added to support async loop

class LivePlotter:
    """
    A class to asynchronously update and plot roll, pitch, and yaw values in real time.
    """
    def __init__(self, buffer_size=100):
        """
        Initialize the plot with a fixed-length buffer.

        :param buffer_size: The number of data points to store for plotting.
        """
        self.buffer_size = buffer_size
        self.roll_data = deque([0] * buffer_size, maxlen=buffer_size)  # Circular buffer
        self.pitch_data = deque([0] * buffer_size, maxlen=buffer_size)
        self.yaw_data = deque([0] * buffer_size, maxlen=buffer_size)
        self.time_data = deque(np.linspace(-buffer_size, 0, buffer_size), maxlen=buffer_size)  # X-axis

        # Create figure and axis
        self.fig, self.ax = plt.subplots()
        self.ax.set_ylim(-180, 180)  # Assuming roll, pitch, yaw are in degrees
        self.ax.set_xlim(-buffer_size, 0)
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Angle (degrees)")
        self.ax.set_title("Real-time Roll, Pitch, Yaw")

        # Initialize empty line objects
        self.line_roll, = self.ax.plot([], [], label="Roll", color="r")
        self.line_pitch, = self.ax.plot([], [], label="Pitch", color="g")
        self.line_yaw, = self.ax.plot([], [], label="Yaw", color="b")
        self.ax.legend()

        #plt.ion()  # Enable interactive mode
        plt.show(block=False)
        # Removed threading in favor of an async plot loop running in the main thread

    def update_plot(self, n_points=1000):
        """ Update the plot with new data. """
        self.line_roll.set_data(self.time_data, self.roll_data)
        self.line_pitch.set_data(self.time_data, self.pitch_data)
        self.line_yaw.set_data(self.time_data, self.yaw_data)

        self.ax.set_xlim(min(self.time_data), max(self.time_data))  # Keep x-axis moving
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def process_incoming_data(self, message):
        """
        Callback function to process incoming data and update the buffer.

        :param message: A comma-separated string "roll,pitch,yaw".
        """
        try:
            roll, pitch, yaw = map(float, message.split(","))
            self.roll_data.append(roll)
            self.pitch_data.append(pitch)
            self.yaw_data.append(yaw)
            self.time_data.append(self.time_data[-1] + 1)  # Increment time

            #self.update_plot()  # Update the plot
        except ValueError:
            print("Invalid data format:", message)

    async def run_plot_loop(self):
        """ Async loop to keep the matplotlib GUI responsive. """
        while True:
            self.update_plot()  # Update the plot
            plt.pause(1)  # Allow GUI event loop to run
            await asyncio.sleep(0.1)

# ...existing code if any...