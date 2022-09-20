import gpiozero
import time
pwm = gpiozero.PWMOutputDevice(pin=12,active_high=True,initial_value=0,frequency=50000)
direction = gpiozero.OutputDevice(pin=4)
encoder = gpiozero.RotaryEncoder(a=5, b=6,max_steps=100000) 
# This class has a lot more functionality,so worth reading up on it
# Step through duty cycle values, slowly increasing the speed and changing the direction of motion
pre_steps = 0
for j in range(10):
    pwm.value = j/10
    direction.value = not direction.value
    print('Duty cycle:',pwm.value,'Direction:',direction.value)
    time.sleep(5.0)
    print('Counter:',encoder.steps,'Speed:',(encoder.steps-pre_steps)/5.0,'steps per second\n')
    pre_steps = encoder.steps
    
    #NB, if steps keeps increasing, what about integer overflows?
pwm.off()
