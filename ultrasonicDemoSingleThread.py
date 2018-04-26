import RPi.GPIO as GPIO
import time
import threading
GPIO.setmode(GPIO.BCM)

TRIG = 23 
ECHO = 24
LED = 17

MIN_DISTANCE = 36 # In inches
INTERVAL = .05
MAX_ITERATIONS = 5 # Used to make sure the LED does not stay on

LED_STATE = False


# Main function
if __name__ == "__main__":
    print("Distance Measurement In Progress")

    # Set up pins as input or output
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(LED, GPIO.OUT)

    GPIO.output(LED, False)

    # This sends the signal for the ultrasonic sensor to turn on
    GPIO.output(TRIG, False)
    print("Waiting For Sensor To Settle")
    time.sleep(.2)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    previous_time = 0
    counter = 0

    try:
        while True:
            # Turn off the LED if it's stuck at being on
            if counter > MAX_ITERATIONS:
                LED_STATE = False
                GPIO.output(LED, LED_STATE)
                counter = 0

            # Waits until input == 1
            while GPIO.input(ECHO) == 0: 
                pass

            while GPIO.input(ECHO) == 1:
                pulse_start = time.time()

            while GPIO.input(ECHO) == 0:
                pulse_end = time.time()

            # Measures the time the ultrasonic pulse takes to get back
            pulse_duration = pulse_end - pulse_start
            
            cm = pulse_duration / .00005    # Our sensor has conversion of 1cm per 50us
            cm = round(cm, 2)
            inches = round(cm * .39, 2)

            if inches < MIN_DISTANCE:
                print("Distance:", cm, "cm ", inches, "in")

                if pulse_end - previous_time >= INTERVAL:
                    previous_time = pulse_end
                    LED_STATE = not LED_STATE   # Invert LED_STATE
                    GPIO.output(LED, LED_STATE)

            if LED_STATE == True: # If LED is on, increment the counter
                counter += 1

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nExiting program")
        

