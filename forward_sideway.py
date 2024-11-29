import time
from wheel import Wheel, Chassis
from config import *


# init wheels
wheels = {
        'front_left':   Wheel(FL[0], FL[1], pwm_min=0, pwm_max=65535),
        'front_right':  Wheel(FR[0], FR[1], pwm_min=0, pwm_max=65535),
        'rear_left':    Wheel(RL[0], RL[1], pwm_min=0, pwm_max=65535),
        'rear_right':   Wheel(RR[0], RR[1], pwm_min=0, pwm_max=65535),
}

# init the car with 4 wheels
car = Chassis(wheels)

# move the car predefined
car.run(forward=30, sideway=0, rotate=0)
time.sleep(2)
car.run(forward=0, sideway=30, rotate=0)
time.sleep(2)
car.run(forward=-30, sideway=0, rotate=0)
time.sleep(2)
car.run(forward=0, sideway=-30, rotate=0)
time.sleep(2)

car.stop()
