import bluetooth
import threading

import RPi.GPIO as GPIO
from navigation import *
from adxl345 import ADXL345
from Queue import Queue # for bluetooth messaging processing 
import adxl345
import os       
import picamera         # the camera video output library
from PIL import Image   # to create image using preset png

global camera   

#make rpi bluetooth discoverable via hciconfig and noauth makes it so that we dont have to click "accept"
bash_command("sudo hciconfig hci0 piscan noauth")


global json_queue
json_queue = Queue()

# function to decode JSON file and calls the display function
def display(json_object):
    global turn, upcoming_road           
    # boolean flag to indicate if we reached our destination
    # inform Tam, boolean needs to pass thru as lowercase
    end = json_object["end"]
    
    if end == True:
        arrived()
        
    elif end == False:
        # check if new manvuer is true
        new_maneuver    = json_object["newManeuver"]
        if new_maneuver == True:
            # new turn
          
            turn            = json_object["turn"]
            distance_left   = json_object["distance"]
            upcoming_road   = json_object["road"]
            turn_update(turn, upcoming_road, distance_left, new_maneuver, camera) 
        # there isnt any new turns
        else:
            distance_left   = json_object["distance"]
            turn_update(turn,upcoming_road,distance_left,new_maneuver, camera)  
            
# function to display destination arrived and delete all arrow and texts
def arrived():
    # delete all text and arrow
    bash_command("sudo killall -s SIGKILL pngview")
    # show text destination arrived
    camera.annotate_text= 'Arrived!'
    sleep(2)
    camera.annotate_text= ''

def check_g_force(acc):
    # the max G before the RPI trigger the SMS
    MAX_G = 5
    
    #intialize the accerelometer
    acc = ADXL345()
    acc.setRange(adxl345.RANGE_16G)
    acc.setBandwidthRate(adxl345.BW_RATE_50HZ)
    while True:        
        axes = acc.getAxes(True)
        # print "ADXL345 on address 0x%x:" % (acc.address)
        if axes['x'] > MAX_G or axes['y'] > MAX_G or axes['z'] > MAX_G:
            message = "Crash"
            inputSocket.send(message.encode())
            sleep(20)

def readIncomingData(inputSocket,q):
    """This Function will read data if available, in the bluetooth socket"""
    while True:
        data=inputSocket.recv(1024)
        print data
        #print "received \"%s\" \n " % data
        if "Connected" in data:
            
            camera.annotate_text= "Connected"
            pass
        else:
            #split the received data based on how many json obj there is
            # "{}{}{}" >>> ["{","{","{",""]
            json_str_list = data.split("}")
            # for every elements, add back the closing bracket
            for each in json_str_list:
                # skip the last empty element bc of .split()
                if "{" in each:
                    #store the json into a variable
                    json_obj = each + "}"
                    #push it to the queue if it is a valid json
                    if (is_json(json_obj)):
                        q.put(json_obj)
def kill_screen(state):
    #GPIO 17 is the pin for backlight
    GPIO.output(17, state)   
    if state == True:
        bash_command("sudo killall -9 fbcp")
        bash_command("sudo rmmod fb_st7735r")
    else:
        bash_command("sudo modprobe fb_st7735r")
        bash_command("sudo modprobe fbtft_device fps=60 txbuflen=32768 name=adafruit18 rotate=270")   
    
def get_from_queue(q):
    """ this thread function that will get json str from the queue one by one and pass it to the display function"""
    global turn, upcoming_road  
    turn          = None
    upcoming_road = None
    print "Getting json strings from the queue"
    while True:
        # this .get() function will block until there is item available
        json_str = q.get()
        print "json from the queue: " + json_str
        
        json_data = json.loads(json_str)
        
        ## change cras,display/blindspot to keys
        if "crashSensor" in json_data:
            state = json_data["crashSensor"]
            #turn on/off crash sensor
        elif "hud" in json_data:
            # turn on/off gpio 17
            #GPIO.output(GPIO #, True or False)\
            state = json_data["hud"]
            kill_screen(state)            
        elif "blindspotSensor" in json_data:
            state = json_data["blindspotSensor"]
            pass
        elif "end" in json_data:     
            display(json_data) # display and update the screen
        q.task_done() # indicate a formerly enqueued task is done
        #it will resume q.join() if it is blocking and resume when all items has been processed
                
def runServer():
    global serverSocket, inputSocket
    # you had indentation problems on this line:
    serverSocket=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1
    print uuid
    serverSocket.bind(("",1))
  
    print "Listening for connections on port: ", port   

    # wait for a message to be sent to this socket only once
    serverSocket.listen(1)
    print "waiting"
    port=serverSocket.getsockname()[1]
    print"store port"
   
    # you were 90% there, just needed to use the pyBluez command:
    bluetooth.advertise_service( serverSocket, "SampleServer",
                        service_id = uuid,
                        service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
                        profiles = [bluetooth.SERIAL_PORT_PROFILE] 
                        )
    print"broadcast port"

    inputSocket,address = serverSocket.accept()
    print "Accepted connection"
    print "Got connection with" , address

    try:
        readIncomingData(inputSocket, json_queue)
    except bluetooth.btcommon.BluetoothError:
        inputSocket.close()
        serverSocket.close()
        camera.close()
        print "Bluetooth connection reset"

if __name__=="__main__":
    try:
        global screenOn, crashSensorOn
        global inputSocket, serverSocket
        screenOn = True
        crashSensorOn = True
        
        #this command enable the video to be use
        bash_command("sudo modprobe fbtft_device fps=60 txbuflen=32768 name=adafruit18 rotate=270")
        # wait until the screen initialize
        sleep(2)
        
        bash_command("sudo fbcp &")   # redirect/copy the all output from fb 0 to fb1
        
        global serverSocket, inputSocket 
        name="bt_server"
        target_name="test"
        # some random uuid, generated by https://www.famkruithof.net/uuid/uuidgen
        uuid="0fee0450-e95f-11e5-a837-0800200c9a66"
        serverSocket = None
        inputSocket = None

        # start a thread that will read from the json queue and display json if available
        displayThread = threading.Thread(target=get_from_queue, args=(json_queue,))
        displayThread.daemon = True
        displayThread.start()

        while True:
            # set up camera and start it, global variable so other functions can use it too
            camera = picamera.PiCamera()    
            camera.resolution = (1280, 720) # set up resolution
            camera.framerate = 24
            camera.brightness = 70
            camera.contrast = 75
            # set the text color
            camera.annotate_background = picamera.Color('black')
            # text size
            camera.annotate_text_size = 100
#            camera.start_preview()
            runServer()
    except KeyboardInterrupt:
        inputSocket.close()
        serverSocket.close()
        camera.close()
        

# try:
#     #this command enable the video to be use
#     bash_command("sudo modprobe fbtft_device fps=60 txbuflen=32768 name=adafruit18 rotate=270")
#     # wait until the screen initialize
#     sleep(2)
    
#     bash_command("sudo fbcp &")   # redirect/copy the all output from fb 0 to fb1 
        
#     #turn on camera
#     camera.start_preview()
    
#     # the max G before the RPI trigger the SMS
#     MAX_G = 5
# #
# #    #intialize the accerelometer
# #    acc = ADXL345()
# #    acc.setRange(adxl345.RANGE_16G)
# #    acc.setBandwidthRate(adxl345.BW_RATE_50HZ)

#     global serverSocket, inputSocket 
#     name="bt_server"
#     target_name="test"
#     # some random uuid, generated by https://www.famkruithof.net/uuid/uuidgen
#     uuid="0fee0450-e95f-11e5-a837-0800200c9a66"
#     serverSocket = None
#     inputSocket = None
    
#     # start the bluetooth connection with android app
#     runServer()
    
#     # start a thread that will read from the json queue and display json if available
#     displayThread = threading.Thread(target=get_from_queue, args=(json_queue,))
#     displayThread.daemon = True
#     displayThread.start()
    
#     # start a receiving thread
#     receiveThread = threading.Thread(target=readIncomingData, args=(inputSocket, json_queue,))
#     receiveThread.daemon = True
#     receiveThread.start()
        
#     # start a sending thread for crash detection    
# #    crashThread  = threading.Thread(target=check_g_force, args=(acc,))
# #    crashThread.daemon = True
# #    crashThread.start()