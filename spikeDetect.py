# ADXL345 Python example 


from adxl345 import ADXL345
import time
import adxl345
import os

MAX_G = 10
  
acc = ADXL345()
acc.setRange(adxl345.RANGE_16G)
acc.setBandwidthRate(adxl345.BW_RATE_50HZ)

while 1:
    axes = acc.getAxes(True)
    #print "ADXL345 on address 0x%x:" % (acc.address)
    if axes['x'] > MAX_G or axes['y'] > MAX_G or axes['z'] > MAX_G:
        #os.system('clear')
        print "   x = %.3fG" % ( axes['x'] )
        print "   y = %.3fG" % ( axes['y'] )
        print "   z = %.3fG" % ( axes['z'] )
        print ""
        time.sleep(.2)
        

        
