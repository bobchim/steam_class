import time
from wheel import Wheel, Chassis
from sensor import IMU


# init wheels
wheels = {
        'front_left':   Wheel(11, 10, pwm_min=0, pwm_max=65535),
        'front_right':  Wheel(12, 13, pwm_min=0, pwm_max=65535),
        'rear_left':    Wheel(7, 6, pwm_min=0, pwm_max=65535),
        'rear_right':   Wheel(8, 9, pwm_min=0, pwm_max=65535),
}

# init the car with 4 wheels
car = Chassis(wheels)

# init i2c interface for communicating with IMU
imu = IMU(1, 2, 3)
imu.cal_gyro(cycles=100)

# move the car predefined
car.run(forward=0, sideway=-60, rotate=8)
roll = 0
pitch = 0
yaw = 0
t0 = time.ticks_us()
while True:
    t1 = time.ticks_us()
    dt = (t1 - t0) * 1e-6
    t0 = t1
    _, _, dyaw = imu.read_gyro()
    yaw += dyaw * dt * 1.05
    print("Yaw: " + str([yaw]))
    time.sleep(0.005)
    if yaw <= -360 or yaw >= 360:
        break

car.stop()
