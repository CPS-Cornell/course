from udp_client import UDPClient
import struct
from data_logger import DataLogger

data_logger = DataLogger()

def print_message(data, addr):

    global data_logger

    # Define the expected array size
    ARRAY_SIZE = 50  # This should match the size used in the Pico code

    # Calculate expected data length (5 arrays of floats, each float is 4 bytes)
    # Be sure to update this if you change the ARRAY_SIZE or the number of arrays in the Pico code
    expected_length = 5 * ARRAY_SIZE * 4

    # Check if received data has the expected length
    if len(data) == expected_length:
        floats = struct.unpack('<%df' % (5 * ARRAY_SIZE), data)
        # Split into arrays
        time_data = floats[0:ARRAY_SIZE]
        encoder_yaw_data = floats[ARRAY_SIZE:2*ARRAY_SIZE]
        imu_yaw_data = floats[2*ARRAY_SIZE:3*ARRAY_SIZE]
        kalman_data = floats[3*ARRAY_SIZE:4*ARRAY_SIZE]
        estimate_covarience = floats[4*ARRAY_SIZE:5*ARRAY_SIZE]
        # Now you can use these arrays as needed
        print("Received data:", len(data), " bytes")

        data_dict = {
            "TIME": time_data,
            "ENCODER_YAW": encoder_yaw_data,
            "IMU_YAW": imu_yaw_data,
            "KALMAN": kalman_data,
            "ESTIMATE_COVARIANCE": estimate_covarience
        }

        data_logger.process_dict(data_dict)

        #for t, ey, iy, k, ec in zip(time_data, encoder_yaw_data, imu_yaw_data, kalman_data, estimate_covarience):
        #    # Log the data using the DataLogger
        #    data_logger.process_string(f"TIME:{int(1000*t)}, ENC:{ey}, IMU:{iy}, KALMAN:{k}, ESTCOV:{ec}")

    else:
        print(f"Warning: Received data length ({len(data)} bytes) doesn't match expected length ({expected_length} bytes)")
        return

if __name__ == "__main__":
    client = UDPClient(listen_port=5005)
    print("Listening for UDP float messages on port 5005...")
    client.start(print_message)
    try:
        while True:
            pass  # Keep the main thread alive
    except KeyboardInterrupt:
        print("\nStopping UDP client.")
        data_logger.save_to_csv("sensor_data.csv")  
        client.stop()
