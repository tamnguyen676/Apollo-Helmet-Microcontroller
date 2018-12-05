from adxl345 import ADXL345
import adxl345
from time import sleep
global crashSensorOn
class Accelerometer:
    MAX_G = 5
    
    def __init__(self):
        self.acc = ADXL345()
        self.initAccelerometer()

    def initAccelerometer(self):
        #intialize the accerelometer
        self.acc.setRange(adxl345.RANGE_16G)
        self.acc.setBandwidthRate(adxl345.BW_RATE_50HZ)