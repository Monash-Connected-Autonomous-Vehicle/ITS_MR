''' Pseudocode for the basic movements of the DMV using keyboard inputs '''

# We will collect user inputs from the keyboard and send them to "kbd_input" which will output these inputs
# For each input we can present a message to "msgs" relevant to the action performed
# We will run this as a seperate thread
# The thread will end its process once it receives the character input set to 'quit'

def kbd_input_thread(kbd_input, msgs):
    
    infinite loop:
        char_input = block waiting to receive character inputs

        if char_input == 'a character that will control the DMV, eg. WASD'
            kbd_input.put_on_non_blocking_queue(char_input)

        msgs.put_on_non_blocking_queue('relevant message to what the input is doing')

        if char_input == 'quit'
            break

# Read messages of the "msgs" queue and display them in a seperate thread
def display_msg_thread(msgs):

    infinite loop:
        msg_input = msgs.get_from_queue()
        display or print msg_input where necessary

# Where the throttle and steering will be controlled by keyboard inputs
# Read user keyboard input from kbd_input queue 
# Using the inputs it will calulate the motor and steering commands which will be sent to the motor and servo of the DMV
# This is a seperate thread and will continue to run as stated by "perform_flag"

def motor_servo_ctrl_thread(kbd_input, msgs, perform_flag):

    # Initialise a logic model for the DMV which maps the user input characters into speed and steering commands
    
    dmv_logic = DMVLogic(msgs)

    # Initialise a driver that will send data to the motor and servo

    motor_servo_driver = MotorServoDriver(msgs)

    # Initialise motor and steering

    steering, speed = dmv_logic.get_next_steering_speed_data()
    motor_servo_driver.set_steering_speed(steering, speed)

    loop till perform_flag returns stop:

        char_input = kbd_input.retrieve_character_from_queue_non_blocking()
        dmv_logic.update_dmv_logic_kbd(char_input)

        # Update the motor and steering

        steering, speed = dmv_logic.get_next_steering_speed_data()
        motor_servo_driver.set_steering_speed(steering, speed)

        # If needed sleep() can be used to maintain constant loop timing

    # Shutting down the thread
    motor_servo_driver.stop()


# This will convert keyboard input commands into signals that will be sent off to the motor and servo
# Also will write out relevant message to "msgs"

class DMVLogic(msgs):

    # Update DMV Logic based on keyboard inputs
    def update_dmv_logic_kbd(char_input)
        depending on input this should update the vehicles speed and steering state

    def get_next_steering_speed_data():
        speed = calculate speed command based on vehicle state
        steering = calculate steering command based on vehicle State

        return steering, speed

# This will act as a driver for the motor and steering by taking the speed and steering data and converting,
# it into PWM values that will drive the ESC and the Servo

class MotorServoDriver(msgs):

    # define the three set points for the ESC being the neutral, max forward and max reverse values for the ESC
    # These values should be found when calibrating and configuring the ESC and the SERVO
    NEUTRAL_POINT = 1500
    MAX_FORWARD = 2000
    MAX_REVERSE = 1000

    # For the servo
    STEERING_NOMINAL_CENTER = 1500
    STEERING_OFFSET = -60
    STEERING_PLUS_MINUS = 190
    STEERING_CENTER = STEERING_NOMINAL_CENTER + STEERING_OFFSET

    def set_steering_speed(steering, speed)

        # clip values
        speed = clip speed to valid [-1.0 or 0.0, +1.0] range
         # -1: backwards
        # 0: neutral
        # 1: forward
        steering = clip steering to valid [-1.0, +1.0] range
        # -1: left 
        # +1: right

        #calculate the PWM values using the calibrated values 
        pwm_speed = map speed to the [MAX_REVERSE, MAX_FORWARD range]
        pwm_steering = map steering to the [STEERING_CENTER +/- STEERING_PLUS_MINUS] range

        apply the pwm pulse signals to the ESC and SERVO

# The master process to manage all threads, processes etc.
def master_dmv_process()

    perform_flag = initialise flag for controlling threads, processes etc.

    # start the output display and the "msgs" queue for receiving messages
    msgs = new message queue
    display_thread = new thread to run output_display_thread(msgs)
    display_thread.start()

    # Queue for transporting keyboard inputs
    kbd_input = new keyboard command queue

    #Queue for the motor and servo controller
    controller_thread = new thread to run motor_servo_ctrl_thread(kbd_input, msgs, perform_flag)

    controller_thread.start

    # Start keyboard input thread
    keyboard_thread = new thread to run kbd_input_thread(kbd_input, msgs)

    keyboard_thread.start()

    # Everything should be operational until user enters a 'quit' command/input
    wait for the user to terminate with 'quit' command/input

    perform_flag = reset the flag to abandon currently running thread

    sleep for a certain period of time to shutdown safely
