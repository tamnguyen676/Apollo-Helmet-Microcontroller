import bluetooth
import threading

from adxl345 import ADXL345
import adxl345
import os       
import picamera         # the camera video output library
from PIL import Image   # to create image using preset png
from time import sleep
import json             # for JSON object parsing

def bash_command(bash_cmd):
    import subprocess
    subprocess.Popen(bash_cmd, stdout=subprocess.PIPE, shell=True)
#bluetooth name for raspberry pi is "raspberrypi"

# function to update the LCD display
def display_update(turimport bluetooth
import threading

from adxl345 import ADXL345
import adxl345
import os       
import picamera         # the camera video output library
from PIL import Image   # to create image using preset png
from time import sleep
import json             # for JSON object parsing



# set up camera and start it 
camera = picamera.PiCamera()    
camera.resolution = (1280, 720) # set up resolution
camera.framerate = 24
camera.brightness = 70
camera.contrast = 75

# set the text color
camera.annotate_background = picamera.Color('red')
# text size
camera.annotate_text_size = 80      
camera.start_preview()                     # start the preview

def bash_command(bash_cmd):
    import subprocess
    subprocess.Popen(bash_cmd, stdout=subprocess.PIPE, shell=True)
#bluetooth name for raspberry pi is "raspberrypi"


def arrived():
    # delete all text and arrow
    bash_command("sudo killall -s SIGKILL pngview")
    # show text destination arrived
    camera.annotate_text= 'Arrived!'
    sleep(2)
    camera.annotate_text= ''
    
# function to update the LCD display
def turn_update(turn, upcoming_road, distance_left,  new_maneuver):     
    if turn in ("GO_STRAIGHT","UNDEFINED"):
        if new_maneuver == True:
            bash_command("sudo killall -s SIGKILL pngview")
            sleep(.2)
            bash_command("sudo raspidmx/pngview/pngview -n -b 0 -l 3 -x 0 -y 90 /home/pi/arrows/straight.png")
        if turn in "UNDEFINED":
            camera.annotate_text= 'Continue for ' + distance_left
        else:
            camera.annotate_text= 'Continue on ' + upcoming_road + " for " + distance_left        
    elif turn in ("LIGHT_RIGHT","QUITE RIGHT","HEAVY_RIGHT"):
        if new_maneuver == True:
            bash_command("sudo killall -s SIGKILL pngview")
            sleep(.2)
            bash_command("sudo raspidmx/pngview/pngview -n -b 0 -l 3 -x 0 -y 90 /home/pi/arrows/right.png")
        camera.annotate_text= 'Turn right onto ' + upcoming_road + " in " + distance_left
    elif turn in ("LIGHT_LEFT","QUITE_LEFT","HEAVY_LEFT"):
        if new_maneuver == True:
            bash_command("sudo killall -s SIGKILL pngview")
            sleep(.2)
            bash_command("sudo raspidmx/pngview/pngview -n -b 0 -l 3 -x 0 -y 90 /home/pi/arrows/left.png")
        camera.annotate_text= 'Turn Left onto ' + upcoming_road + " in " + distance_left            
    elif turn in ("UTURN_LEFT"):
        if new_maneuver == True:
            bash_command("sudo killall -s SIGKILL pngview")
            sleep(.2)
            bash_command("sudo raspidmx/pngview/pngview -n -b 0 -l 3 -x 0 -y 90 /home/pi/arrows/u_turn.png")
        camera.annotate_text= 'Make a U-Turn on ' + upcoming_road + " in " + distance_left
    elif turn in ("KEEP_RIGHT", "HIGHWAY_KEEP_RIGHT"):
        if new_maneuver == True:
            bash_command("sudo killall -s SIGKILL pngview")
            sleep(.2)
            bash_command("sudo raspidmx/pngview/pngview -n -b 0 -l 3 -x 0 -y 100 /home/pi/arrows/keep_right.png")
        camera.annotate_text= 'Keep right on ' + upcoming_road + " in " + distance_left 
    elif turn in ("KEEP_MIDDLE"):
        if new_maneuver == True:
            bash_command("sudo killall -s SIGKILL pngview")
            sleep(.2)
            bash_command("sudo raspidmx/pngview/pngview -n -b 0 -l 3 -x 0 -y 100 /home/pi/arrows/keep_middle.png")
        camera.annotate_text= 'Stay in the middle on ' + upcoming_road + " in " + distance_left
    elif turn in ("KEEP_LEFT","HIGHWAY_KEEP_LEFT"):
        if new_maneuver == True:
            bash_command("sudo killall -s SIGKILL pngview")
            sleep(.2)
            bash_command("sudo raspidmx/pngview/pngview -n -b 0 -l 3 -x 0 -y 100 /home/pi/arrows/keep_left.png")
        camera.annotate_text= 'Keep left on ' + upcoming_road + " in " + distance_left
       
    elif turn in ("ENTER_HIGHWAY_RIGHT_LANE","LEAVE_HIGHWAY_RIGHT_LANE"):
        if new_maneuver == True:
            bash_command("sudo killall -s SIGKILL pngview")
            sleep(.2)
            bash_command("sudo raspidmx/pngview/pngview -n -b 0 -l 3 -x 0 -y 90 /home/pi/arrows/split_right.png")
        if turn in ("ENTER_HIGHWAY_RIGHT_LANE"):
            camera.annotate_text= 'Enter Highway ' + upcoming_road + " with the right lane in " + distance_left
        else:
            camera.annotate_text= 'Leave Highway ' + upcoming_road + " with the right lane in " + distance_left
    elif turn in ("ENTER_HIGHWAY_LEFT_LANE", "LEAVE_HIGHWAY_LEFT_LANE"):
        if new_maneuver == True:
            bash_command("sudo killall -s SIGKILL pngview")
            sleep(.2)
            bash_command("sudo raspidmx/pngview/pngview -n -b 0 -l 3 -x 0 -y 90 /home/pi/arrows/split_left.png")
        if turn in ("ENTER_HIGHWAY_RIGHT_LANE"):
            camera.annotate_text= 'Enter Highway ' + upcoming_road + " with the Left lane in " + distance_left
        else:
            camera.annotate_text= 'Leave Highway ' + upcoming_road + " with the Left lane in " + distance_left

# function to decode JSON file and calles the display function
def display(json_str):
    global turn, upcoming_road 
    json_object     = json.loads(json_str)
          
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
            turn_update(turn, upcoming_road, distance_left, new_maneuver) 
        # there isnt any new turns
        else:
            distance_left   = json_object["distance"]
            turn_update(turn,upcoming_road,distance_left,new_maneuver)            
def check_g_force():
    
    while True:        
        axes = acc.getAxes(True)
        # print "ADXL345 on address 0x%x:" % (acc.address)
        if axes['x'] > MAX_G or axes['y'] > MAX_G or axes['z'] > MAX_G:
            message = "Crash"
            inputSocket.send(message.encode())
            sleep(20)

def readIncomingData(inputSocket):
    global turn, upcoming_road  
    turn          = None
    upcoming_road = None
    while True:
        data=inputSocket.recv(1024)
        print "received [%s] \n " % data
        
        # data will be a json string
        display(data)
        
        
def runServer():
    
    global serverSocket, inputSocket
    # you had indentation problems on this line:
    serverSocket=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1

    serverSocket.bind(("",port))
  
    print "Listening for connections on port: ", port   

    # wait for a message to be sent to this socket only once
    serverSocket.listen(1)
    port=serverSocket.getsockname()[1]
   
    # you were 90% there, just needed to use the pyBluez command:
    bluetooth.advertise_service( serverSocket, "SampleServer",
                        service_id = uuid,
                        service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
                        profiles = [bluetooth.SERIAL_PORT_PROFILE] 
                        )

    inputSocket,address = serverSocket.accept()
    print "Accepted connection"
    print "Got connection with" , address
    
    

try:
   

    #bash_command("sudo rpi-fbcp/build/fbcp &")   # redirect/copy the all output from fb 0 to fb1 
        
    # the max G before the RPI trigger the SMS
    MAX_G = 5

    #intialize the accerelometer
    acc = ADXL345()
    acc.setRange(adxl345.RANGE_16G)
    acc.setBandwidthRate(adxl345.BW_RATE_50HZ)
    
    name="bt_server"
    target_name="test"
    # some random uuid, generated by https://www.famkruithof.net/uuid/uuidgen
    uuid="0fee0450-e95f-11e5-a837-0800200c9a66"
    serverSocket = None
    inputSocket = None
    
    # start the bluetooth connection with android app
    #runServer()
    # start a receiving thread
    #receiveThread = threading.Thread(target=readIncomingData, args=(inputSocket,))
    #receiveThread.daemon = True
    #receiveThread.start()
        
    # start a sending thread for crash detection    
    #crashThread  = threading.Thread(target=check_g_force, args=(acc,))
    #crashThread.daemon = True
    #crashThread.start()
    distance = 280
    time = 1
    while(time > 0):
        turns= ["GO_STRAIGHT", "UTURN_RIGHT", "KEEP_RIGHT", "LIGHT_RIGHT","KEEP_MIDDLE","KEEP_LEFT","QUITE_LEFT","ENTER_HIGHWAY_RIGHT_LANE","ENTER_HIGHWAY_LEFT_LANE"]
        for turn in turns:
            upcoming_road = "Campbell Road"
            distance_left = str(distance) + "ft"
            new_maneuver = True
            turn_update(turn,upcoming_road,distance_left,new_maneuver)
            distance = distance - 1
            sleep()
        time = time - 1
    camera.stop_preview()
    camera.close()
            
        
    
    
except KeyboardInterrupt:
    serverSocket.close()
    inputSocket.close()

n, distance_left, upcoming_road, end, new_maneuver)
    
    
    camera.annotate_text= turn + " on " +    
    

# function to decode JSON file and calles the display function
def display(json_str):
    json_object     = json.loads(json_str)
    turn            = json_object["turn"]
    distance_left   = json_object["distance"]
    upcoming_road   = json_object["road"]
    # boolean flag to indicate if we reached our destination
    end             = json_object["end"]
    # boolean indictaing if we changed road or just continuing on the same road
    new_maneuver    = json_object["newManeuver"]
    display_update(turn, distance_left, upcoming_road, end,new_maneuver)    


def check_g_force():
    
    while True:        
        axes = acc.getAxes(True)
        # print "ADXL345 on address 0x%x:" % (acc.address)
        if axes['x'] > MAX_G or axes['y'] > MAX_G or axes['z'] > MAX_G:
            message = "Crash"
            inputSocket.send(message.encode())
            sleep(20)

def readIncomingData(inputSocket):
    while True:
        data=inputSocket.recv(1024)
        print "received [%s] \n " % data
        
        # data will be a json string
        display(data)
        
        
def runServer():
    
    global serverSocket, inputSocket
    # you had indentation problems on this line:
    serverSocket=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1

    serverSocket.bind(("",port))
  
    print "Listening for connections on port: ", port   

    # wait for a message to be sent to this socket only once
    serverSocket.listen(1)
    port=serverSocket.getsockname()[1]
   
    # you were 90% there, just needed to use the pyBluez command:
    bluetooth.advertise_service( serverSocket, "SampleServer",
                        service_id = uuid,
                        service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
                        profiles = [bluetooth.SERIAL_PORT_PROFILE] 
                        )

    inputSocket,address = serverSocket.accept()
    print "Accepted connection"
    print "Got connection with" , address
    
    

try:
    # set up camera and start it 
    camera = picamera.PiCamera()    
    camera.resolution = (1280, 720) # set up resolution
    camera.framerate = 24
    camera.brightness = 75
    camera.contrast = 75
    
    # set the text color
    camera.annotate_background = Color('red')
    # text size
    camera.annotate_text_size = 100      
    
        
    # the max G before the RPI trigger the SMS
    MAX_G = 5

    #intialize the accerelometer
    acc = ADXL345()
    acc.setRange(adxl345.RANGE_16G)
    acc.setBandwidthRate(adxl345.BW_RATE_50HZ)
    
    name="bt_server"
    target_name="test"
    # some random uuid, generated by https://www.famkruithof.net/uuid/uuidgen
    uuid="0fee0450-e95f-11e5-a837-0800200c9a66"
    serverSocket = None
    inputSocket = None
    
    # start the bluetooth connection with android app
    runServer()
    # start a receiving thread
    receiveThread = threading.Thread(target=readIncomingData, args=(inputSocket,))
    receiveThread.daemon = True
    receiveThread.start()
    
    
    # start a sending thread for crash detection    
    crashThread  = threading.Thread(target=check_g_force, args=(acc,))
    crashThread.daemon = True
    crashThread.start()
    
except KeyboardInterrupt:
    serverSocket.close()
    inputSocket.close()
