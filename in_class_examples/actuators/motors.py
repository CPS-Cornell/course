from machine import Pin, PWM
import time

motor_phase_pin = 14
motor_enable_pin = 15

motor_phase = Pin(motor_phase_pin, Pin.OUT)
#motor_enable = Pin(motor_enable_pin, Pin.OUT)
motor_enable = PWM(Pin(motor_enable_pin))


motor_phase.value(0)
#motor_enable.value(0)
motor_enable.duty_u16(int(.5*65535)) # max value is 65535
