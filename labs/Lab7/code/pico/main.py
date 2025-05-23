# filepath: c:\Users\jdj78\Documents\CPS\course\docs\labs\Lab7\code\pico\rumba.py

import time
import random
import math
import machine
from differential_drive import DifferentialDrive
from rangefinder import Rangefinder
from vcnl4040 import VCNL4040
import uasyncio as asyncio

class RumbaRobot:
    # Constants for navigation
    SAFE_DISTANCE_CM = 20  # Minimum safe distance in cm from obstacles
    BACK_PROXIMITY_THRESHOLD = 2000  # Adjust based on your proximity sensor values
    
    # Movement speeds
    FORWARD_SPEED = 15  # cm/s for forward movement
    TURN_SPEED = 10  # cm/s for turning
    
    # Movement states
    STATE_FORWARD = 0
    STATE_TURN = 1
    STATE_BACK_UP = 2
    
    def __init__(self):
        # Initialize the robot components
        self.drive = DifferentialDrive.get_default_differential_drive()
        self.rangefinder = Rangefinder(20, 21)  # Front ultrasonic sensor
        #self.proximity = VCNL4040(i2c=machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17)))
        
        # Initialize movement state
        self.current_state = self.STATE_FORWARD
        self.turn_direction = 1  # 1 for right, -1 for left
        self.state_start_time = time.time()
        self.turn_duration = 0
        
        # For random behaviors
        self.random_counter = 0
        self.random_behavior_threshold = 50  # Change random behavior after this count
    
    def get_front_distance(self):
        """Get distance from the front rangefinder in cm"""
        try:
            distance = self.rangefinder.distance()
            return distance
        except Exception as e:
            print("Rangefinder error:", e)
            return 100  # Default safe value
    
    def get_back_proximity(self):
        """Get proximity value from the back sensor"""
        try:
            return self.proximity.proximity
        except Exception as e:
            print("Proximity sensor error:", e)
            return 0  # Default safe value (no obstacle)
    
    def choose_random_turn(self):
        """Choose a random turn direction and duration"""
        # Randomly choose turn direction (left or right)
        self.turn_direction = random.choice([-1, 1])
        
        # Random turn duration between 0.5 and 2 seconds
        self.turn_duration = random.uniform(0.5, 2.0)
        
        # Reset state timer
        self.state_start_time = time.time()
    
    def update_movement(self):
        """Update robot movement based on sensor data and current state"""
        front_distance = self.get_front_distance()
        print("Front distance:", front_distance)
        #back_proximity = self.get_back_proximity()
        current_time = time.time()
        
        # Increment random counter for introducing occasional randomness
        self.random_counter += 1
        if self.random_counter > self.random_behavior_threshold:
            self.random_counter = 0
            if random.random() < 0.3:  # 30% chance to change behavior randomly
                self.current_state = self.STATE_TURN
                self.choose_random_turn()
                
        # State machine for robot movement
        if self.current_state == self.STATE_FORWARD:
            if front_distance < self.SAFE_DISTANCE_CM:
                # Obstacle detected in front, start turning
                self.current_state = self.STATE_TURN
                self.choose_random_turn()
            #elif back_proximity > self.BACK_PROXIMITY_THRESHOLD:
            #    # Obstacle detected behind, move forward faster
            #    self.drive.set_speed(self.FORWARD_SPEED * 1.5, self.FORWARD_SPEED * 1.5)
            else:
                # Normal forward movement
                self.drive.set_speed(self.FORWARD_SPEED, self.FORWARD_SPEED)
                
        elif self.current_state == self.STATE_TURN:
            # Check if turn duration has elapsed
            if current_time - self.state_start_time > self.turn_duration:
                self.current_state = self.STATE_FORWARD
            else:
                # Continue turning
                left_speed = -self.TURN_SPEED if self.turn_direction > 0 else self.TURN_SPEED
                right_speed = self.TURN_SPEED if self.turn_direction > 0 else -self.TURN_SPEED
                self.drive.set_speed(left_speed, right_speed)
                
        elif self.current_state == self.STATE_BACK_UP:
            # Check if backup duration has elapsed
            if current_time - self.state_start_time > 1.0:  # 1 second of backing up
                self.current_state = self.STATE_TURN
                self.choose_random_turn()
            else:
                # Continue backing up
                self.drive.set_speed(-self.FORWARD_SPEED, -self.FORWARD_SPEED)

    def stop(self):
        """Stop the robot"""
        self.drive.stop()
        
    async def run(self):
        """Main robot control loop"""
        try:
            while True:
                #self.update_movement()
                await asyncio.sleep(0.05)  # 50ms update interval
        except KeyboardInterrupt:
            self.stop()
            print("Robot stopped")

# Main entry point
if __name__ == "__main__":
    print("Starting Rumba-style robot...")
    robot = RumbaRobot()
    
    # Run the asyncio event loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(robot.run())
    finally:
        robot.stop()
        print("Robot program terminated")
