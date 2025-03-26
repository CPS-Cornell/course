from machine import Pin
import time


button_pin = Pin(22, Pin.IN, Pin.PULL_UP)

counter = 0

def button_callback(pin):
    global counter
    counter += 1
    print(f"Button pressed {counter} times")

# Attach the interrupt to the button pin
button_pin.irq(trigger=Pin.IRQ_FALLING, handler=button_callback)

while True:
    # Main loop can perform other tasks or just sleep
    continue
    # IMU
    # Range finder
    # UDP messages

