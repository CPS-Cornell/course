import pickle
import csv

class DataLogger:
    def __init__(self):
        """
        Initializes an empty data dictionary.
        The dictionary will have keys for each sensor.
        Each value is a tuple: (list_of_times, list_of_sensor_values)
        """
        self.data = {}

    def process_string(self, s):
        """
        Parses a string of sensor data and updates the internal data dictionary.

        The expected string format is:
            "SENSOR1:<value1>, SENSOR2:<value2>, ..., TIME:<time>"
        where:
            - Each sensor field is separated by a comma.
            - The TIME field is mandatory and must appear exactly once.
            - Sensor values must be either ints or floats.
        
        If the string is missing the TIME field, contains duplicate sensor names
        (or duplicate TIME fields), or has a non-numeric sensor value, a warning
        is printed and the data is discarded.
        """
        # Split the string by commas and trim spaces.
        fields = [field.strip() for field in s.split(',')]
        time_value = None
        message_data = {}  # Temporary dict to store sensor readings in this message.

        for field in fields:
            if ':' not in field:
                print("Warning: Field '{}' does not contain a colon; discarding message.".format(field))
                return

            key, value_str = field.split(':', 1)
            key = key.strip()
            value_str = value_str.strip()

            if key.upper() == "TIME":
                if time_value is not None:
                    print("Warning: Duplicate TIME field in message; discarding data.")
                    return
                try:
                    time_value = int(value_str)
                except ValueError:
                    print("Warning: TIME field '{}' is not an integer; discarding data.".format(value_str))
                    return
            else:
                if key in message_data:
                    print("Warning: Duplicate sensor '{}' in message; discarding data.".format(key))
                    return
                # Try to convert the sensor value to int or float.
                try:
                    try:
                        sensor_val = int(value_str)
                    except ValueError:
                        sensor_val = float(value_str)
                except ValueError:
                    print("Warning: Sensor '{}' value '{}' is not numeric; discarding data.".format(key, value_str))
                    return
                message_data[key] = sensor_val

        # Check that the TIME field was present.
        if time_value is None:
            print("Warning: No TIME field in message; discarding data.")
            return

        # Add each sensor's data into the logger's data dictionary.
        for sensor, val in message_data.items():
            if sensor not in self.data:
                # Automatically create an entry for a new sensor.
                self.data[sensor] = ([], [])
            # Check for duplicate time stamp for this sensor.
            if time_value in self.data[sensor][0]:
                print("Warning: Duplicate TIME {} for sensor '{}' in logger; skipping update for this sensor.".format(time_value, sensor))
            else:
                self.data[sensor][0].append(time_value)
                self.data[sensor][1].append(val)

    def get_data(self):
        """
        Returns the internal data dictionary.
        """
        return self.data

    def save_data(self, filename="data_logger.pkl"):
        """
        Pickles the internal data dictionary to a file.
        """
        try:
            with open(filename, "wb") as f:
                pickle.dump(self.data, f)
            print("Data successfully pickled to", filename)
        except Exception as e:
            print("Error pickling data:", e)
    
    def save_to_csv(self, filename="data_logger.csv"):
        """
        Saves the logged data to a CSV file.
        The first column will be TIME, and each additional column will be a sensor.
        Missing values are left blank.
        """
        if not self.data:
            print("No data to save.")
            return

        # Collect all unique timestamps
        all_times = sorted(set(time for sensor in self.data for time in self.data[sensor][0]))

        # Prepare the header
        sensors = sorted(self.data.keys())  # Sort sensor names alphabetically
        headers = ["TIME"] + sensors

        # Create a dictionary to map times to sensor values
        sensor_data_map = {time: {sensor: None for sensor in sensors} for time in all_times}

        # Populate the dictionary with sensor values
        for sensor, (times, values) in self.data.items():
            for t, v in zip(times, values):
                sensor_data_map[t][sensor] = v

        # Write to CSV
        try:
            with open(filename, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)  # Write header row
                
                for time in all_times:
                    row = [time] + [sensor_data_map[time][sensor] if sensor_data_map[time][sensor] is not None else "" for sensor in sensors]
                    writer.writerow(row)

            print("Data successfully saved to", filename)
        except Exception as e:
            print("Error saving to CSV:", e)

    def __del__(self):
        """
        Deconstructor that automatically saves the data when the object is deleted.
        """
        self.save_data()
        self.save_to_csv()


# Example usage:
#if __name__ == '__main__':
#    logger = DataLogger()
#
#    # A valid message
#    message1 = "TEMP:23.5, HUMID:45, TIME:1001"
#    logger.process_string(message1)
#
#    # A message with a duplicate sensor reading (will be discarded)
#    message2 = "TEMP:24, TEMP:25, TIME:1002"
#    logger.process_string(message2)
#
#    # A message with no TIME field (will be discarded)
#    message3 = "PRESSURE:101.3, HUMID:50"
#    logger.process_string(message3)
#
#    # A message with a duplicate TIME field (within the same message)
#    message4 = "TEMP:23, TIME:1003, HUMID:44, TIME:1004"
#    logger.process_string(message4)
#
#    # A message with a non-numeric sensor value (will be discarded)
#    message5 = "TEMP:abc, HUMID:50, TIME:1005"
#    logger.process_string(message5)
#
#    # Print the stored data
#    data = logger.get_data()
#    print("Logged Data:")
#    for sensor, (times, values) in data.items():
#        print(f"{sensor}: Times = {times}, Values = {values}")
