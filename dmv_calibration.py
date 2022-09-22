#!/usr/bin/env python
# RUN "sudo pigpiod" IN TERMINAL BEFORE RUNNING CODE!!!!
import pigpio # Import PIGPIO library for hardware PWM values
from time import sleep # Import sleep function

pi = pigpio.pi() # Grants access to the GPIO
SERVO_GPIO = 17 # Variable that stores GPIO pin number where servo is connected
ESC_GPIO = 27 # Variable that stores GPIO pin number where ESC is connected
pi.set_mode(SERVO_GPIO, pigpio.INPUT) # Sets SERVO_GPIO as an input
pi.set_mode(ESC_GPIO, pigpio.INPUT) # Sets ESC_GPIO as an input

pi.set_servo_pulsewidth(SERVO_GPIO, 1650) # A PWM of 1650us will full lock to the left
sleep(1) # Sleep for 1 second
pi.set_servo_pulsewidth(SERVO_GPIO, 1150) # A PWM of 1150us will bring steering to neutral position
sleep(1) # Sleep for 1 second
pi.set_servo_pulsewidth(SERVO_GPIO, 650) # A PWM of 650us will full lock to the right
sleep(1) # Sleep for 1 second
pi.set_servo_pulsewidth(SERVO_GPIO, 1150) # Return to neutral position
sleep(1) # Sleep for 1 second

pi.set_servo_pulsewidth(ESC_GPIO, 1500) # Testing a PWM of 1500us on ESC (currently not working)
sleep(1)

pi.set_servo_pulsewidth(SERVO_GPIO, 0) # Acts as a GPIO cleanup for SERVO_GPIO
sleep(1) # Sleep for 1 second
pi.set_servo_pulsewidth(ESC_GPIO, 0) # Acts as a GPIO cleanup for ESC_GPIO
sleep(1) # Sleep for 1 second
pi.stop() #Release pigpio resources
