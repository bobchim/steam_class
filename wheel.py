from machine import Pin, PWM


class Chassis(object):
    def __init__(self, wheels):
        self._wheels = wheels
        self._speeds = {
            'front_left':   0,
            'front_right':  0,
            'rear_left':    0,
            'rear_right':   0,
        }

    def __forward(self, speed):
        # forward is positive
        self._speeds['front_left'] += speed
        self._speeds['front_right'] += speed
        self._speeds['rear_left'] += speed
        self._speeds['rear_right'] += speed

    def __sideway(self, speed):
        # right is positive
        self._speeds['front_left'] += speed
        self._speeds['front_right'] -= speed
        self._speeds['rear_left'] -= speed
        self._speeds['rear_right'] += speed

    def __rotate(self, speed):
        # clockwise is positive
        self._speeds['front_left'] += speed
        self._speeds['front_right'] -= speed
        self._speeds['rear_left'] += speed
        self._speeds['rear_right'] -= speed

    def __reset_speed(self):
        for key in self._speeds:
            self._speeds[key] = 0

    def stop(self):
        for key in self._wheels:
            self._wheels[key].stop()
        self.__reset_speed()

    def run(self, forward=0, sideway=0, rotate=0):
        self.__reset_speed()
        self.__forward(forward)
        self.__sideway(sideway)
        self.__rotate(rotate)
        for key in self._wheels:
            self._wheels[key].spin(self._speeds[key])


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
