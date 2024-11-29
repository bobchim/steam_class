# At the beginning of the code, we [import] the libraries
# For every "words" you write in the code, it need to be defined,
# if it is not defined in this code or in the library, then error occurs.
from time import sleep
from machine import Pin, PWM
from wheel import Wheel
from config import *


# This create 4 wheel [instance] from the predefined wheel object
# so for example, [front_left] is an [instance of Wheel]
# According to the Wheel object __init__, we instantiate a wheel by
# giving it 2 numbers, which are the 2 pin numbers connected to the motor.
front_left = Wheel(FL[0], FL[1])
front_right = Wheel(FR[0], FR[1])
rear_left = Wheel(RL[0], [RL[1])
rear_right = Wheel(RR[0], RR[1])

# this spin the wheel at 50 percent duty cycle
front_left.spin(50)
front_right.spin(50)
rear_left.spin(50)
rear_right.spin(50)
# keep spinning for 1 second
sleep(1)
# this stops the wheels
front_left.stop()
front_right.stop()
rear_left.stop()
rear_right.stop()
