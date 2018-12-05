from adxl345 import ADXL345
import adxl345
global MAX_G
global acc
MAX_G = 5

def initAccelerometer():
    #intialize the accerelometer
    acc = ADXL345()
    acc.setRange(adxl345.RANGE_16G)
    acc.setBandwidthRate(adxl345.BW_RATE_50HZ)

def check_g_force():
    global MAX_G
    while True:        
        axes = acc.getAxes(True)
        # print "ADXL345 on address 0x%x:" % (acc.address)
        if axes['x'] > MAX_G or axes['y'] > MAX_G or axes['z'] > MAX_G:
            message = "Crash"
            inputSocket.send(message.encode())
            sleep(20)