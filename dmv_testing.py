# DMV Motor Testing
import pigpio
from time import sleep

pi = pigpio.pi() # Grants access to the GPIO
ESC_GPIO = 27 # Variable that stores GPIO pin number where ESC is connected
pi.set_mode(ESC_GPIO, pigpio.INPUT) # Sets ESC_GPIO as an input

pi.set_servo_pulsewidth(ESC_GPIO, 1500) # Testing a PWM of 1500us on ESC (currently not working)
sleep(1)

pi.set_servo_pulsewidth(ESC_GPIO, 0) # Acts as a GPIO cleanup for ESC_GPIO
sleep(1) # Sleep for 1 second
pi.stop() #Release pigpio resources