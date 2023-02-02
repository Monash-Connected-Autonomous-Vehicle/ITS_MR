# DMV Motor Testing
import pigpio
from time import sleep

pi = pigpio.pi() # Grants access to the GPIO
SERVO_GPIO = 4 # Variable that stores GPIO pin number where ESC is connected
pi.set_mode(SERVO_GPIO, pigpio.INPUT) # Sets ESC_GPIO as an input

pi.set_servo_pulsewidth(SERVO_GPIO, 1150) # Testing a PWM of 1500us on ESC (currently not working)
sleep(1)
pi.set_servo_pulsewidth(SERVO_GPIO, 1650) # Testing a PWM of 1500us on ESC (currently not working)
sleep(1)
pi.set_servo_pulsewidth(SERVO_GPIO, 650) # Testing a PWM of 1500us on ESC (currently not working)
sleep(1)
pi.set_servo_pulsewidth(SERVO_GPIO, 1150) # Testing a PWM of 1500us on ESC (currently not working)
sleep(1)

pi.set_servo_pulsewidth(SERVO_GPIO, 0) # Acts as a GPIO cleanup for ESC_GPIO
sleep(1) # Sleep for 1 second
pi.stop() #Release pigpio resources






'''
#!/usr/bin/env python
#Import relevant librariesdaws
import os
import curses # This library does not work on Windows operating systems
import pigpio # This library does not work on Windows operating systems
import time
import atexit


# Servo is connected to GPIO pin 4 (Change this value corresponding to which GPIO pin it is connected to)
SERVO_GPIO_PIN = 4
#ESC_GPIO_PIN = 27
MIN_SERVO_PWM = 650  # A pulsewidth of 650us will turn the steering full lock to the right
MID_SERVO_PWM = 1150 # A pulsewidth of 1150us will turn the steering to the neutral position
MAX_SERVO_PWM = 1650 # A pulsewidth of 1650us will turn the steering full lock to the left
#MIN_ESC_PWM = 1350 # A pulseidth of 1350us is the max decceleration of the DMV
#MID_ESC_PWM = 1500 # A pulsewidth of 1500us is the neutral position of the DMV
#MAX_ESC_PWM = 1650 # A pulsewidth of 1650us is the max acceleration of the DMV

# Assigning integer values to each key
NONE = 0
LEFT_ARROW = 1
RIGHT_ARROW = 2
#UP_ARROW = 3
#DOWN_ARROW = 4
HOME = 5
QUIT = 6


def getch():
    global in_escape, in_cursor
    char = stdscr.getch()

    key = NONE

    if char == 27:
        in_escape = True
        in_cursor = False
    elif char == 91 and in_escape:
        in_cursor = True
    elif char == 67 and in_cursor: # ASCII value for 'left arrow' key
        key = LEFT_ARROW
        in_escape = False
    elif char == 68 and in_cursor: # ASCII value for 'right arrow' key
        key = RIGHT_ARROW
        in_escape = False
    elif char == 65 and in_cursor: # ASCII value for 'up arrow' key
        key = UP_ARROW
        in_escape = False
    elif char == 66 and in_cursor: # ASCII value for 'down arrow' key
        key = DOWN_ARROW
        in_escape = False
    elif char == 104 and in_cursor: # ASCII value for 'h' key
        key = HOME
        in_escape = False
    elif char == 113 or char == 81: # ASCII value for 'q' or 'Q' key
        key = QUIT
    else:
        in_escape = False
        in_cursor = False

    return key


def cleanup():
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    pi.stop()


pi = pigpio.pi()

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()

# This makes sure that the original screen is restored
atexit.register(cleanup)

in_escape = False
in_cursor = False

pwm_servo = MID_SERVO_PWM
#pwm_esc = MID_ESC_PWM
pi.set_servo_pulsewidth(SERVO_GPIO_PIN, pwm_servo)
#pi.set_servo_pulsewidth(ESC_GPIO_PIN, pwm_esc)

# CALIBRATING AND ARMING THE ESC
#pi.set_servo_pulsewidth(ESC, 0)
#print("Disconnect the battery and press Enter")
#inp = input()
#if inp == '':
#    pi.set_servo_pulsewidth(ESC, max_value)
#    print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
#    inp = input()
#    if inp == '':            
#        pi.set_servo_pulsewidth(ESC, min_value)
#        print ("Wierd eh! Special tone")
#        time.sleep(7)  
#        print ("Wait for it ....")
#        time.sleep (5)
#        print ("Im working on it, DONT WORRY JUST WAIT.....")
#        pi.set_servo_pulsewidth(ESC, 0)
#        time.sleep(2)
#        print ("Arming ESC now...")
#        pi.set_servo_pulsewidth(ESC, min_value)
#        time.sleep(1)
#        print ("See.... uhhhhh")

while True and range(650, 1650):
    time.sleep(0.01)
    char = getch()

    if char == QUIT:
        break
    pulsewidth_servo = pwm_servo
    #pulsewidth_esc = pwm_esc

    if char == HOME:
        pulsewidth_servo = MID_SERVO_PWM # Neutral steering position
        #pulsewidth_esc = MID_ESC_PWM # Neutral speed
    elif char == LEFT_ARROW:
        pulsewidth_servo = pulsewidth_servo - 100 # Shorten pulse
        if pulsewidth_servo < MIN_SERVO_PWM:
            pulsewidth_servo = MAX_SERVO_PWM
    elif char == RIGHT_ARROW:
        pulsewidth_servo = pulsewidth_servo + 100 # Lengthen pulse
        if pulsewidth_servo > MAX_SERVO_PWM:
            pulsewidth_servo = MIN_SERVO_PWM
    elif char == UP_ARROW:
        pulsewidth_esc = pulsewidth_esc + 50 # Lengthen pulse
        if pulsewidth_esc > MAX_ESC_PWM:
            pulsewidth_esc = pulsewidth_esc - 50
    elif char == DOWN_ARROW:
        pulsewidth_esc = pulsewidth_esc - 50 # Shorten pulse
        if pulsewidth_esc < MIN_ESC_PWM:
            pulsewidth_esc = pulsewidth_esc + 50
    if pulsewidth != pwm:
        pwm_servo = pulsewidth_servo
        pi.set_servo_pulsewidth(SERVO_GPIO_PIN, pwm_servo)
        pwm_esc = pulsewidth_esc
        pi.set_servo_pulsewidth(ESC_GPIO_PIN, pwm_esc)
'''