# At the beginning of the code, we [import] the libraries
# For every "words" you write in the code, it need to be defined,
# if it is not defined in this code or in the library, then error occurs.
from time import sleep
from machine import Pin, PWM

# This create 4 wheel [instance] from the predefined wheel object
# so for example, [front_left] is an [instance of Wheel]
# According to the Wheel object __init__, we instantiate a wheel by
# giving it 2 numbers, which are the 2 pin numbers connected to the motor.
front_left = Wheel(11, 10)
front_right = Wheel(12, 13)
rear_left = Wheel(7, 6)
rear_right = Wheel(8, 9)

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


# We created 4 [instances] of [Wheel] above,
# which is defined here.
# class Something(object) is an [object].
# def do_something() is the [function] within the class
class Wheel(object):
    def __init__(self, pin1_, pin2_, pwm_freq=500, pwm_min=0, pwm_max=65535):
        assert isinstance(pwm_freq, int)
        assert isinstance(pwm_min, int)
        assert isinstance(pwm_max, int)
        self.pwm_min = pwm_min
        self.pwm_max = pwm_max
        self.pwm_freq = 0
        self.speed = 0  # speed [-100, 100]

        pin1 = Pin(pin1_, Pin.OUT)
        pin2 = Pin(pin2_, Pin.OUT)
        self.pin1_pwm = PWM(pin1)
        self.pin2_pwm = PWM(pin2)
        self.set_pwm_freq(pwm_freq)
        self.spin(0)

    def set_pwm_freq(self, pwm_freq):
        self.pwm_freq = pwm_freq
        self.pin1_pwm.freq(pwm_freq)
        self.pin2_pwm.freq(pwm_freq)

    def speed_u16(self, speed):
        assert (speed >= 0 and speed <= 100)
        return int((self.pwm_max - self.pwm_min) * speed / 100)

    def spin(self, speed):
        if speed > 100:
            speed = 100
        if speed < -100:
            speed = -100
        self.speed = speed
        duty = self.speed_u16(abs(speed))
        if speed >= 0:
            self.pin2_pwm.duty_u16(0)
            self.pin1_pwm.duty_u16(duty)
        elif speed < 0:
            self.pin1_pwm.duty_u16(0)
            self.pin2_pwm.duty_u16(duty)

    def stop(self):
        self.pin1_pwm.duty_u16(0)
        self.pin2_pwm.duty_u16(0)

    def quit(self):
        self.pin1_pwm.deinit()
        self.pin2_pwm.deinit()
