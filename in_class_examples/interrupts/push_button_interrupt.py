from machine import Pin
import time

# Configure pin 22 as input with pull-up resistor
button = Pin(22, Pin.IN, Pin.PULL_UP)

# Counter to track button presses
press_count = 0

# Debounce time (in milliseconds)
debounce_time = 100
last_press_time = 0

# Callback function for button press
def button_pressed(pin):
    global press_count, last_press_time
    
    # Debounce implementation
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_press_time) > debounce_time:
        press_count += 1
        print(f"Button pressed! Count: {press_count}")
        last_press_time = current_time

# Set up interrupt handler for falling edge (when button is pressed)
button.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)

# Main loop - keep the program running
print("Button interrupt example. Press the button connected to pin 22.")
try:
    while True:
        # Main program can continue doing other things
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Program stopped")