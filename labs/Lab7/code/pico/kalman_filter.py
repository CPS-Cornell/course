from differential_drive import DifferentialDrive
from motor import SinglePWMMotor, DualPWMMotor
from encoder import Encoder
from encoded_motor import EncodedMotor
from imu import IMU
import asyncio
import _thread
import math
from udp_server import UDPServer, connect_to_wifi
import machine
import time
import gc
from array import array  # Add import for array support
import struct

# Network settings - replace with your values
WIFI_SSID = "RedRover"    # Your WiFi network name
WIFI_PASSWORD = ""        # Your WiFi password
LAPTOP_IP = "10.49.36.71" # Your laptop's IP address

led = machine.Pin("LED", machine.Pin.OUT)
try:
    connect_to_wifi(WIFI_SSID, WIFI_PASSWORD)
except Exception as e:
    while True:
        led.on()
        asyncio.sleep(0.5)
        led.off()
        asyncio.sleep(0.5)

led = machine.Pin("LED", machine.Pin.OUT)
led.on()

left_motor = EncodedMotor.get_default_encoded_motor(index=1)
right_motor = EncodedMotor.get_default_encoded_motor(index=2)
drivetrain = DifferentialDrive.get_default_differential_drive()
imu = IMU.get_default_imu()

# Kalman filter parameters
Q = 0.01  # Process noise covariance
R = 0.1   # Measurement noise covariance
P = 1.0   # Initial error covariance
x_hat = 0.0  # Initial state estimate

def get_encoder_yaw(drive_train):
    left_delta = drive_train.get_left_encoder_position()
    right_delta = drive_train.get_right_encoder_position()
    return ((right_delta-left_delta)/2)*360/(drive_train.track_width*math.pi)

# Make run_turn asynchronous
async def run_turn():
    # Assuming drivetrain.turn is now async or non-blocking
    # If drivetrain.turn is still blocking, this won't solve the root cause.
    try:
        print("Starting turn sequence...")
        await drivetrain.turn(70) # Use await if turn is async
        await drivetrain.turn(-25)
        await drivetrain.turn(60)
        print("Finished turn sequence.")
    except Exception as e:
        print(f"Error in run_turn: {e}")

def kalman_filter_update(previous_estimate, previous_covariance, encoder_delta, imu_measurement):
    """
    Perform one step of the Kalman filter to fuse encoder and IMU data
    
    Args:
        previous_estimate: Previous angle estimate (degrees)
        previous_covariance: Previous error covariance
        encoder_delta: Change in encoder yaw since last update (degrees)
        imu_measurement: Current IMU yaw reading (degrees)
    
    Returns:
        new_estimate: Updated angle estimate (degrees)
        new_covariance: Updated error covariance
    """
    # Prediction step
    predicted_estimate = previous_estimate + encoder_delta
    predicted_covariance = previous_covariance + Q
    
    # Update step
    kalman_gain = predicted_covariance / (predicted_covariance + R)
    new_estimate = predicted_estimate + kalman_gain * (imu_measurement - predicted_estimate)
    new_covariance = (1 - kalman_gain) * predicted_covariance
    
    return new_estimate, new_covariance

gc.collect()

# Define array size
ARRAY_SIZE = 50  # Adjust based on memory constraints

# Initialize arrays with appropriate typecodes
time_data = array('f', [0] * ARRAY_SIZE)  # 'l' for signed long (time.ticks_ms())
encoder_yaw_data = array('f', [0.0] * ARRAY_SIZE)  # 'f' for float
imu_yaw_data = array('f', [0.0] * ARRAY_SIZE)
kalman_data = array('f', [0.0] * ARRAY_SIZE)
estimate_covarience = array('f', [0.0] * ARRAY_SIZE)

# Counter for current array index
data_index = 0

print("Free memory:", gc.mem_free())

async def main():
    global x_hat, P, data_index

    # ...existing code...
    udp_server = UDPServer(LAPTOP_IP, 5005)
    previous_encoder_yaw = get_encoder_yaw(drivetrain)

    # Start the turning sequence in a separate thread
    turn_task = asyncio.create_task(run_turn()) # Start async task
    print('Started Turning thread')

    start_time = time.ticks_us()
    gyro_angle = 0

    while True:
        # Get current measurements
        current_encoder_yaw = get_encoder_yaw(drivetrain)
        imu_yaw = gyro_angle 
        print(imu_yaw)
        
        # Calculate change in encoder yaw (control input)
        delta_encoder_yaw = current_encoder_yaw - previous_encoder_yaw
        previous_encoder_yaw = current_encoder_yaw
        x_hat, P = kalman_filter_update(x_hat, P, delta_encoder_yaw, imu_yaw)

        time_data[data_index] = float(time.ticks_ms()/1000)  # Store current time
        kalman_data[data_index] = float(x_hat)  # Store Kalman estimate
        estimate_covarience[data_index] = float(P)
        encoder_yaw_data[data_index] = float(current_encoder_yaw)  # Store encoder yaw
        imu_yaw_data[data_index] = float(imu_yaw)  # Store IMU yaw 

        if data_index == ARRAY_SIZE - 1:

            packed_data = (
                struct.pack('<%df' % ARRAY_SIZE, *time_data) +
                struct.pack('<%df' % ARRAY_SIZE, *encoder_yaw_data) +
                struct.pack('<%df' % ARRAY_SIZE, *imu_yaw_data) +
                struct.pack('<%df' % ARRAY_SIZE, *kalman_data) +
                struct.pack('<%df' % ARRAY_SIZE, *estimate_covarience)
            )
            print('Sending data:', len(packed_data), ' bytes')
            udp_server.send(packed_data)
            data_index = 0

        data_index += 1
        await asyncio.sleep(.001)
        end_time = time.ticks_us()
        elapsed_time = time.ticks_diff(end_time, start_time)
        gyro_angle = gyro_angle + imu.get_gyro_z_rate() * 0.001 * elapsed_time / 1000000  # Assuming gyro rate is in degrees/sec
        #print("Elapsed time:", elapsed_time)
        start_time = end_time

asyncio.run(main())