#!/usr/bin/env python
#Import relevant libraries
import curses # This library does not work on Windows operating systems
import pigpio # This library does not work on Windows operating systems
import time
import atexit


SERVO_GPIO_PIN = 17 # Servo is connected to GPIO pin 17 (Change this value corresponding to which GPIO pin it is connected to)
MIN_SERVO_PWM = 650 # A pulsewidth of 650us will turn the steering full lock to the right
MID_SERVO_PWM = 1150 # A pulsewidth of 1150us will turn the steering to the neutral position
MAX_SERVO_PWM = 1650 # A pulsewidth of 1650us will turn the steering full lock to the left

# Assigning integer values to each key
NONE = 0
LEFT_ARROW = 1
RIGHT_ARROW = 2
UP_ARROW = 3
DOWN_ARROW = 4
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
    elif char == 68 and in_cursor: 
        key = LEFT_ARROW
        in_escape = False
    elif char == 67 and in_cursor: 
        key = RIGHT_ARROW
        in_escape = False
    elif char == 65 and in_cursor: 
        key = UP_ARROW
        in_escape = False
    elif char == 66 and in_cursor: 
        key = DOWN_ARROW
        in_escape = False
    elif char == 72 and in_cursor: 
        key = HOME
        in_escape = False
    elif char == 113 or char == 81: 
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

atexit.register(cleanup) # This makes sure that the original screen is restored

in_escape = False
in_cursor = False

pwm = MID_SERVO_PWM
pi.set_servo_pulsewidth(SERVO_GPIO_PIN, pwm)

while True:
    time.sleep(0.01)
    char = getch()

    if char == QUIT:
        break
    pulsewidth = pwm

    if char == HOME:
        pulsewidth = MID_SERVO_PWM # Stop
    elif char == UP_ARROW:
        pulsewidth = MIN_SERVO_PWM # Fastest Clockwise
    elif char == DOWN_ARROW:
        pulsewidth = MAX_SERVO_PWM # Fastest Clockwise
    elif char == LEFT_ARROW:
        pulsewidth = pulsewidth - 5 # Shorten pulse
        if pulsewidth < MAX_SERVO_PWM:
            pulsewidth = MAX_SERVO_PWM
    elif char == RIGHT_ARROW:
        pulsewidth = pulsewidth + 5 # Lengthen pulse
        if pulsewidth > MIN_SERVO_PWM:
            pulsewidth = MIN_SERVO_PWM
    if pulsewidth != pwm:
        pwm = pulsewidth
        pi.set_servo_pulsewidth(SERVO_GPIO_PIN, pwm)
