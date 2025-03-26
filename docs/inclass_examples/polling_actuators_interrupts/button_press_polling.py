from machine import Pin
import time

# Set up the button on GPIO pin 22
button_pin = Pin(22, Pin.IN, Pin.PULL_UP)

counter = 0

previous_state = button_pin.value()

while True:
    temp_button_state = button_pin.value()
    if not temp_button_state and previous_state == 1:
        previous_state = 0
        counter += 1
        print(f"Button pressed {counter} times")
    if temp_button_state and previous_state == 0:
        previous_state = 1
