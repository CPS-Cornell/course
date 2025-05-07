from machine import Pin
import time

# Set up the button on GPIO pin 22
# Using pull-up resistor so button press will read 0 (low)
button = Pin(22, Pin.IN, Pin.PULL_UP)

# Initialize the counter
press_count = 0

print("Button polling program started. Press the button to see a message.")

# Main polling loop
while True:
    # Check if button is pressed (will read 0 when pressed with pull-up configuration)
    if button.value() == 0:
        press_count += 1
        print(f"Button pressed! Count: {press_count}")
        # Small delay to avoid detecting multiple presses (debouncing)
        time.sleep(0.2)
    
    # Small delay to avoid excessive CPU usage while polling
    time.sleep(0.01)
