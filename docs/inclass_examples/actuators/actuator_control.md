# Motor Control with Raspberry Pi Pico

## Overview of [`motors.py`](motors.py)

The `motors.py` script provides a basic interface for controlling a DC motor using the Raspberry Pi Pico microcontroller. This script utilizes the MicroPython framework to access and control the Pico's hardware capabilities.

## How It Works

The script controls a motor through two GPIO pins:

1. **Phase Pin (GPIO 14)**: Controls the motor's direction of rotation
   - When set to 0: Motor rotates in one direction
   - When set to 1: Motor rotates in the opposite direction

2. **Enable Pin (GPIO 15)**: Controls the motor's speed using Pulse Width Modulation (PWM)
   - PWM generates a signal that rapidly switches on and off
   - The duty cycle (percentage of "on" time) determines the average voltage delivered to the motor
   - Higher duty cycle values result in higher motor speeds

## Hardware Connection

This code is designed for use with an H-bridge motor driver or similar motor control circuit that accepts:
- A direction control signal (connected to GPIO 14)
- A speed control PWM signal (connected to GPIO 15)

## Code Explanation

```python
from machine import Pin, PWM
import time

# Define GPIO pins for motor control
motor_phase_pin = 14  # Direction control
motor_enable_pin = 15 # Speed control

# Initialize GPIO pins
motor_phase = Pin(motor_phase_pin, Pin.OUT)     # Digital output for direction
motor_enable = PWM(Pin(motor_enable_pin))       # PWM output for speed control

# Set initial values
motor_phase.value(0)                            # Set initial direction
motor_enable.duty_u16(int(.5*65535))            # Set speed to 50% (value range: 0-65535)
```

## Running on the Raspberry Pi Pico

To use this code on your Raspberry Pi Pico:

1. Connect the Pico to your computer via USB
2. Copy the `motors.py` file to the Pico using Thonny IDE or another MicroPython tool
3. The code will run automatically when the Pico powers up (if saved as `main.py`)
4. Alternatively, import it in your own script: `import motors`

## Adjusting Motor Speed

The motor speed can be adjusted by changing the PWM duty cycle value:

```python
# Example: Change speed to 75%
motor_enable.duty_u16(int(0.75 * 65535))

# Example: Change speed to 25%
motor_enable.duty_u16(int(0.25 * 65535))

# Example: Full speed
motor_enable.duty_u16(65535)

# Example: Stop motor
motor_enable.duty_u16(0)
```

## Changing Direction

To change the motor's direction, toggle the phase pin:

```python
# Reverse direction
motor_phase.value(1)

# Return to original direction
motor_phase.value(0)
```
