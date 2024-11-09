import time
#import numpy as np
from machine import I2C, Pin
import MPU6050


class IMU(object):
    def __init__(self, ident, sda_pin, scl_pin):
        i2c = I2C(ident, sda=Pin(sda_pin), scl=Pin(scl_pin))
        self.imu = MPU6050.MPU6050(i2c)
        self.imu.wake()
        self.imu.write_lpf_range(6)
        self.gyro_offset = [0, 0, 0]
        #self.accel_rot = np.eye(3)

    def cal_gyro(self, cycles=100):
        print('calibrating gyro... do not move')
        for i in range(cycles):
            gyro = self.imu.read_gyro_data()
            for i in range(3):
                self.gyro_offset[i] += gyro[i]
                time.sleep(0.01)
        for i in range(3):
            self.gyro_offset[i] /= cycles
        print('gyro offset: ' + str(self.gyro_offset))
        time.sleep(1)
    
    '''
    def cal_accel(self, cycles=100, accel_ref=[0, 0, 1]):
        print('calibrating accelerometer... do not move')
        accel_tmp = [0, 0, 0]
        for i in range(cycles):
            accel = self.imu.read_accel_data()
            for i in range(3):
                accel_tmp[i] += accel[i]
                time.sleep(0.01)
        for i in range(3):
            accel_tmp[i] /= cycles
        self.accel_rot = self.vec2R(accel_tmp, accel_ref)
        print('accel rotation: ' + str(self.accel_rot))
        time.sleep(1)
    '''

    def read_gyro(self):
        raw = self.imu.read_gyro_data()
        out = [0, 0, 0]
        for i in range(3):
            out[i] = raw[i] - self.gyro_offset[i]
        return out
    
    def read_accel(self):
        #raw = self.imu.read_accel_data()
        #return self.accel_rot @ raw
        return self.imu.read_accel_data()
    '''
    @staticmethod
    def vec2R(vec1, vec2):
        """ Find the rotation matrix that aligns vec1 to vec2
        vec1: A 3d "source" vector
        vec2: A 3d "destination" vector
        mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
        """
        a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
        v = np.cross(a, b)
        if any(v): #if not all zeros then
            c = np.dot(a, b)
            s = np.linalg.norm(v)
            kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
            return np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))

        else:
            return np.eye(3) #cross of all zeros only occurs on identical directions
    '''
