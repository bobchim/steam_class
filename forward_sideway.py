import time
from wheel import Wheel, Chassis


# init wheels
wheels = {
        'front_left':   Wheel(11, 10, pwm_min=0, pwm_max=65535),
        'front_right':  Wheel(12, 13, pwm_min=0, pwm_max=65535),
        'rear_left':    Wheel(7, 6, pwm_min=0, pwm_max=65535),
        'rear_right':   Wheel(8, 9, pwm_min=0, pwm_max=65535),
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
