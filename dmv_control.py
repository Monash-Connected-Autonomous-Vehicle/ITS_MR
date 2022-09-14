#!/usr/bin/env python
#Import relevant libraries
from fcntl import F_SEAL_SEAL
import numpy as np
import queue
from threading import Thread
import curses # This library does not work on Windows operating systems
import pigpio # This library does not work on Windows operating systems
import time
import atexit
from multiprocessing import Queue as MpQueue

# IGNORE COMMENTED CODE :)

# debug = False # Variable to store False bool message

# # Initialise the GPIO pins for the servo and the ESC
# pi = pigpio.pi() # Grants access to GPIO pins
# SERVO_GPIO = 17 # Servo is connected to GPIO pin 17 (Change this value corresponding to which GPIO pin it is connected to)
# ESC_GPIO = 27 # ESC is connected to GPIO pin 27 (Change this value corresponding to which GPIO pin it is connected to)
# pi.set_mode(SERVO_GPIO, pigpio.INPUT) # Sets SERVO_GPIO as an input
# pi.set_mode(ESC_GPIO, pigpio.INPUT) # Sets ESC_GPIO as an input

# #Define the keyboard inputs for the DMV
# STOP_DMV = ord(' ') # Space-bar key
# LEFT_STEER = curses.KEY_LEFT # Left arrow key
# RIGHT_STEER = curses.KEY_RIGHT # Right arrow key
# SPEED_UP = curses.KEY_UP # Up arrow key
# SPEED_DOWN = curses.KEY_DOWN # Down arrow key
# QUIT = ord('q') # q key
# MAX_KBD_QUEUE = 10 # Define a max queue size for keyboard inputs in order to prevent overflow in queue


# # Gathers keyboard inputs from user and sends them to kbd_input
# # Writes a relevant message to msgs
# # The thread will end its process once the 'Quit' character input is pressed
# def kbd_input_thread(screen, kbd_input, msgs):

#     while True:
#         char = screen.getch() # Captures keyboard character inputs

#         msgs.put_nowait([0, 0, 'Keyboard Input Character: %s at %.4f'
#                     % (str(char), time.time())]) # Initialise the non-blocking queue for msgs

#         if char == STOP_DMV: # Space-bar key
#             char_txt = 'Stop'
#         elif char == SPEED_UP: # Up arrow key
#             char_txt = 'Speed Up'
#         elif char == SPEED_DOWN: # Down arrow key
#             char_txt = 'Speed Down'
#         elif char == LEFT_STEER: # Left arrow key
#             char_txt = 'Left Steer'
#         elif char == RIGHT_STEER: # Right arrow key
#             char_txt = 'Right Steer'
#         elif char == QUIT: # q key
#             char_txt = 'Quit'
#         else:
#             char_txt = 'Unknown' # None of the keyboard inputs as defined previously
#         msgs.put_nowait([1, 0, char_txt]) # Put messages corresponding to the keyboard inputs, onto queue

#         try:
#             kbd_input.put_nowait(char) # Put keyboard inputs onto queue
#         except queue.FULL:
#             # Since there is a limit on the queue size we must check if it is full
#             pass
#             if debug:
#                 msgs.put_nowait([21, 0, 'KBD Queue is Full'])

#         if char == QUIT:
#             # Shutting down msgs queue
#             msgs.put_nowait([20, 0, 'Shutting down...'])
            
#             return

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

SERVO_GPIO_PIN = 17 # Servo is connected to GPIO pin 17 (Change this value corresponding to which GPIO pin it is connected to)
MIN_SERVO_PWM = 650 # A pulsewidth of 650us will turn the steering full lock to the right
MID_SERVO_PWM = 1150 # A pulsewidth of 1150us will turn the steering to the neutral position
MAX_SERVO_PWM = 1650 # A pulsewidth of 1650us will turn the steering full lock to the left

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

    if char == 27: # ASCII value for 'escape' key
        in_escape = True
        in_cursor = False
    elif char == 91 and in_escape: # ASCII value for '[' key
        in_cursor = True
    elif char == 68 and in_cursor: # ASCII value for 'D' key
        key = LEFT_ARROW
        in_escape = False
    elif char == 67 and in_cursor: # ASCII value for 'C' key
        key = RIGHT_ARROW
        in_escape = False
    elif char == 65 and in_cursor: # ASCII value for 'A' key
        key = UP_ARROW
        in_escape = False
    elif char == 66 and in_cursor: # ASCII value for 'B' key
        key = DOWN_ARROW
        in_escape = False
    elif char == 72 and in_cursor: # ASCII value for 'H' key
        key = HOME
        in_escape = False
    elif char == 113 or char == 81: # ASCII value for 'q and Q' key
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
