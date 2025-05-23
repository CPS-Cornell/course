from machine import Pin, PWM
from time import sleep

servo = PWM(Pin(16))  # Pin 15 is used for the servo

servo.freq(50)  # Set frequency to 50Hz (20ms period)

MICROSEC_PER_DEGREE: int = 10000
LOW_ANGLE_OFFSET: int = 500000

while True:

    servo.duty_ns(int(75* MICROSEC_PER_DEGREE + LOW_ANGLE_OFFSET))
    sleep(3)
    servo.duty_ns(int(120* MICROSEC_PER_DEGREE + LOW_ANGLE_OFFSET))
    sleep(3)