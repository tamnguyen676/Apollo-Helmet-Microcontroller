import RPi.GPIO as GPIO
import time
import threading
import sys
GPIO.setmode(GPIO.BCM)

LTRIG = 5 
LECHO = 13
LLED = 26

RTRIG = 6 
RECHO = 19
RLED = 20

MAX_DISTANCE = 66 # In inches

#pulse timing thread, to use pulse timer to calculate the distance of the detected object
def pulse(signal, ECHO):
    while True:
        while GPIO.input(ECHO) == 0:
            pass
        while GPIO.input(ECHO)==1:
            pulse_start = time.time()
        while GPIO.input(ECHO)==0:
            pulse_end = time.time()	
	 # Measures the time the ultrasonic pulse takes to get back
        pulse_duration = pulse_end - pulse_start
        
        cm = pulse_duration / .00005 # Our sensor has conversion of 1cm per 50us
        cm = round(cm, 2)
        inches = round(cm * 0.39, 2)

        if (inches < MAX_DISTANCE):
            print("Distance:",cm,"cm ",inches,"in")
            signal.set()    # Let the trigger thread know that it's time to
            time.sleep(60)

# Flashes the LED and buzzes 5 times.
def trigger(signal,LED):
       
    while True:
        signal.wait() 
        for i in range(5):
            GPIO.output(LED, True)
            time.sleep(0.000002)
            GPIO.output(LED, False)
            time.sleep(0.000002)
        signal.clear() # Clears the signal (resets)
            
# Main function
if __name__ == "__main__":
    print("Distance Measurement In Progress")

    # Set up pins as input or output
    GPIO.setup(LTRIG,GPIO.OUT) ########
    GPIO.setup(LECHO,GPIO.IN)
    GPIO.setup(LLED, GPIO.OUT)#####
	

    GPIO.setup(RTRIG,GPIO.OUT) ###
    GPIO.setup(RECHO,GPIO.IN)
    GPIO.setup(RLED, GPIO.OUT) ###

    GPIO.output(LLED, False)
    GPIO.output(RLED, False)
	
	
    # This sends the signal for the ultrasonic sensor to turn on
    GPIO.output(LTRIG, False)
    GPIO.output(RTRIG, False)	
    print("Waiting For Sensor To Settle")
    time.sleep(.4)
    GPIO.output(LTRIG, True)
    GPIO.output(RTRIG, True)
    time.sleep(0.00002)
    GPIO.output(LTRIG, False)
    GPIO.output(RTRIG, False)
    
    l_signal = threading.Event() # This is used to signal the Left  LED to flash
    r_signal = threading.Event() # This is used to signal the right LED to flash
    l_trigger_thread = threading.Thread(target = trigger, args = (l_signal,LLED)) # The flashLED function is run in a separate thread, non-blocking 
    r_trigger_thread = threading.Thread(target = trigger, args = (r_signal,RLED)) # The flashLED function is run in a separate thread, non-blocking 
    l_trigger_thread.start()    # Run the new left sensor thread
    r_trigger_thread.start()    # Run the new right sensor thread

    try:
        l_pulse_thread = threading.Thread(target = pulse, args = (l_signal,LECHO)) # The Pulse timer function is run in a separate thread, non-blocking 
        r_pulse_thread = threading.Thread(target = pulse, args = (r_signal,RECHO)) # The Pulse timer function is run in a separate thread, non-blocking
        l_pulse_thread.start()    # Run the new left sensor thread
        r_pulse_thread.start()    # Run the new right sensor thread
        
            
                
    except KeyboardInterrupt:
        
        GPIO.cleanup()
        print("\nExiting program")
        sys.exit()
    except:
        GPIO.cleanup()
        print("\nExiting program")
        sys.exit()
    finally:
        print("test")
        
        

