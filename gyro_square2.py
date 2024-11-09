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
for i in range(4):
    # go straight forward
    car.run(forward=30, sideway=0, rotate=0)
    time.sleep(2)
    car.stop()
    time.sleep(0.1)

    # make a turn
    car.run(forward=0, sideway=0, rotate=20)
    roll = 0
    pitch = 0
    yaw = 0
    t0 = time.ticks_us()
    while True:
        # keep looping until gyroscope accumulates 90 degrees
        t1 = time.ticks_us()
        dt = (t1 - t0) * 1e-6
        t0 = t1
        _, _, dyaw = imu.read_gyro()
        yaw += dyaw * dt * 1.05
        print("Yaw: " + str([yaw]))
        time.sleep(0.005)
        if yaw <= -90 or yaw >= 90:
            break
    car.stop()
    time.sleep(0.1)

car.stop()
