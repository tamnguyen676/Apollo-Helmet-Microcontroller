import RPi.GPIO as GPIO
import time
import threading
GPIO.setmode(GPIO.BCM)

TRIG = 23 
ECHO = 24
LED = 17

MIN_DISTANCE = 36 # In inches


# Flashes the LED and buzzes 5 times.
def trigger(signal):
    global inches
    
    while True:
        signal.wait()   # Waits for the signal from the main thread
        
        if inches < 5:
            x = 5
        else:
            x = inches
        
        delay = (x - 5) * .002581 + .02
        
        print(x, "in ", delay)
        
        for i in range(5):
            GPIO.output(LED, True)
            time.sleep(delay)
            GPIO.output(LED, False)
            time.sleep(delay)
        
        signal.clear() # Clears the signal (resets)
            
# Main function
if __name__ == "__main__":
    print("Distance Measurement In Progress")

    # Set up pins as input or output
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.setup(LED, GPIO.OUT)

    GPIO.output(LED, False)

    # This sends the signal for the ultrasonic sensor to turn on
    GPIO.output(TRIG, False)
    print("Waiting For Sensor To Settle")
    time.sleep(.2)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    signal = threading.Event() # This is used to signal the LED to flash
    trigger_thread = threading.Thread(target = trigger, args = (signal,)) # The flashLED function is run in a separate thread, non-blocking
    trigger_thread.start()    # Run the new thread
    

    try:
        while True:
            # Waits until input == 1
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
            inches = round(cm * .39,2)

            if (inches < MIN_DISTANCE):
                # print("Distance:",cm,"cm ",inches,"in")
                signal.set()    # Let the trigger thread know that it's time to
                
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nExiting program")
        

