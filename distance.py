import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 23 
ECHO = 24

PERCENT_CHANGE = .1

print "Distance Measurement In Progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"
time.sleep(.2)

GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

prev_cm = 1

try:
    while True:
        
        while GPIO.input(ECHO) == 0: # Waits until input == 1
            pass

        while GPIO.input(ECHO)==1:
          pulse_start = time.time()

        while GPIO.input(ECHO)==0:
          pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        
        cm = pulse_duration / .00005 # Our sensor has conversion of 1cm per 50us
        cm = round(cm, 2)
        inches = round(cm * .39,2)

        if (cm >= (1 + PERCENT_CHANGE) * prev_cm or cm <= (1 - PERCENT_CHANGE) * prev_cm):
            print "Distance:",cm,"cm ",inches,"in"

        prev_cm = cm
except KeyboardInterrupt:
    GPIO.cleanup()
    print "\nExiting program"
