import RPi.GPIO as GPIO
from time import sleep
import threading

class BlindspotSensor:
    LTRIG = 5 
    LECHO = 13
    LLED = 26

    RTRIG = 6 
    RECHO = 19
    RLED = 20

    MAX_DISTANCE = 66 # In inches

    def __init__(self):
        self.l_signal = threading.Event() # This is used to signal the Left  LED to flash
        self.r_signal = threading.Event() # This is used to signal the right LED to flash
        self.initGPIO()

    def initGPIO(self):
        print "Initializing GPIO pins..."
        GPIO.setmode(GPIO.BCM)
        
        # Set up pins as input or output
        GPIO.setup(BlindspotSensor.LTRIG,GPIO.OUT) ########
        GPIO.setup(BlindspotSensor.LECHO,GPIO.IN)
        GPIO.setup(BlindspotSensor.LLED, GPIO.OUT)#####
        

        GPIO.setup(BlindspotSensor.RTRIG,GPIO.OUT) ###
        GPIO.setup(BlindspotSensor.RECHO,GPIO.IN)
        GPIO.setup(BlindspotSensor.RLED, GPIO.OUT) ###

        GPIO.output(BlindspotSensor.LLED, False)
        GPIO.output(BlindspotSensor.RLED, False)
        
        
        # This sends the signal for the ultrasonic sensor to turn on
        GPIO.output(BlindspotSensor.LTRIG, False)
        GPIO.output(BlindspotSensor.RTRIG, False)   
        print "Waiting For Sensor To Settle"
        sleep(.4)
        GPIO.output(BlindspotSensor.LTRIG, True)
        GPIO.output(BlindspotSensor.RTRIG, True)
        sleep(0.00002)
        GPIO.output(BlindspotSensor.LTRIG, False)
        GPIO.output(BlindspotSensor.RTRIG, False)