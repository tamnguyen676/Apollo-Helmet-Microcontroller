import bluetooth
import threading

from adxl345 import ADXL345
from Queue import Queue # for bluetooth messaging processing 
import adxl345
import os       
import picamera         # the camera video output library
from PIL import Image   # to create image using preset png
from time import sleep
import json             # for JSON object parsing


def bash_command(bash_cmd):
    import subprocess
    subprocess.Popen(bash_cmd, stdout=subprocess.PIPE, shell=True)
    
# set up camera and start it, global variable so other functions can use it too
camera = picamera.PiCamera()    
camera.resolution = (1280, 720) # set up resolution
camera.framerate = 24
camera.brightness = 70
camera.contrast = 75

#make rpi bluetooth discoverable via hciconfig and noauth makes it so that we dont have to click "accept"
bash_command("sudo hciconfig hci0 piscan noauth")

# set the text color
camera.annotate_background = picamera.Color('black')
# text size
camera.annotate_text_size = 100      
#bluetooth name for raspberry pi is "raspberrypi"

json_queue = Queue()

# function to display destination arrived and delete all arrow and texts
def arrived():
    # delete all text and arrow
    bash_command("sudo killall -s SIGKILL pngview")
    # show text destination arrived
    camera.annotate_text= 'Arrived!'
    sleep(2)
    camera.annotate_text= ''

#returns a boolean if a string is valid json
def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError:
    return False
  return True
# function to update the LCD display
def turn_update(turn, upcoming_road, distance_left,  new_maneuver):      
    if turn in ("GO_STRAIGHT","UNDEFINED"):
        if new_maneuver == True:
            bash_command("sudo killall -s SIGKILL pngview")
            sleep(.2)
            bash_command("sudo /home/pi/raspidmx/pngview/pngview -n -b 0 -l 3 -x 0 -y 200 /home/pi/Project-Apollo/arrows/straight.png")
        if turn in "UNDEFINED":
            camera.annotate_text= 'Continue for:' + distance_left
        else:
            camera.annotate_text= 'Continue on ' + upcoming_road + " : " + distance_left        
    elif turn in ("LIGHT_RIGHT","QUITE_RIGHT","HEAVY_RIGHT"):
        if new_maneuver == True:
            bash_command("sudo killall -s SIGKILL pngview")
            sleep(.2)
            bash_command("sudo /home/pi/raspidmx/pngview/pngview -n -b 0 -l 3 -x 0 -y 200 /home/pi/Project-Apollo/arrows/right.png")
        if upcoming_road == "":
            camera.annotate_text= 'Turn right: ' + distance_left
        else:
            camera.annotate_text= 'Turn right onto ' + upcoming_road + " : " + distance_left
    elif turn in ("LIGHT_LEFT","QUITE_LEFT","HEAVY_LEFT"):
        if new_maneuver == True:
            bash_command("sudo killall -s SIGKILL pngview")
            sleep(.2)
            bash_command("sudo /home/pi/raspidmx/pngview/pngview -n -b 0 -l 3 -x 0 -y 200 /home/pi/Project-Apollo/arrows/left.png")
        if upcoming_road == "":
            camera.annotate_text= 'Turn left: ' + distance_left
        else:    
            camera.annotate_text= 'Turn Left onto ' + upcoming_road + " : " + distance_left            
    elif turn in ("UTURN_LEFT"):
        if new_maneuver == True:
            bash_command("sudo killall -s SIGKILL pngview")
            sleep(.2)
            bash_command("sudo /home/pi/raspidmx/pngview/pngview -n -b 0 -l 3 -x 0 -y 200 /home/pi/Project-Apollo/arrows/u_turn.png")
        if upcoming_road == "":
            camera.annotate_text= 'Make a U-Turn: ' + distance_left
        else:
            camera.annotate_text= 'Make a U-Turn on ' + upcoming_road + " : " + distance_left
    elif turn in ("KEEP_RIGHT", "HIGHWAY_KEEP_RIGHT"):
        if new_maneuver == True:
            bash_command("sudo killall -s SIGKILL pngview")
            sleep(.2)
            bash_command("sudo /home/pi/raspidmx/pngview/pngview -n -b 0 -l 3 -x 0 -y 220 /home/pi/Project-Apollo/arrows/keep_right.png")
        if upcoming_road == "":
            camera.annotate_text= 'Keep right: ' + distance_left
        else:
            camera.annotate_text= 'Keep right on ' + upcoming_road + " : " + distance_left 
    elif turn in ("KEEP_MIDDLE"):
        if new_maneuver == True:
            bash_command("sudo killall -s SIGKILL pngview")
            sleep(.2)
            bash_command("sudo /home/pi/raspidmx/pngview/pngview -n -b 0 -l 3 -x 0 -y 220 /home/pi/Project-Apollo/arrows/keep_middle.png")
        camera.annotate_text= 'Stay in the middle on ' + upcoming_road + " : " + distance_left
    elif turn in ("KEEP_LEFT","HIGHWAY_KEEP_LEFT"):
        if new_maneuver == True:
            bash_command("sudo killall -s SIGKILL pngview")
            sleep(.2)
            bash_command("sudo /home/pi/raspidmx/pngview/pngview -n -b 0 -l 3 -x 0 -y 220 /home/pi/Project-Apollo/arrows/keep_left.png")
        if upcoming_road == "":
            camera.annotate_text= 'Keep left: ' + distance_left
        else:
            camera.annotate_text= 'Keep left on ' + upcoming_road + " : " + distance_left
       
    elif turn in ("ENTER_HIGHWAY_RIGHT_LANE","LEAVE_HIGHWAY_RIGHT_LANE"):
        if new_maneuver == True:
            bash_command("sudo killall -s SIGKILL pngview")
            sleep(.2)
            bash_command("sudo /home/pi/raspidmx/pngview/pngview -n -b 0 -l 3 -x 0 -y 200 /home/pi/Project-Apollo/arrows/split_right.png")
        if turn in ("ENTER_HIGHWAY_RIGHT_LANE"):
            camera.annotate_text= 'Enter Highway ' + upcoming_road + " with right lane: " + distance_left
        else:
            camera.annotate_text= 'Leave Highway ' + upcoming_road + " with right lane: " + distance_left
    elif turn in ("ENTER_HIGHWAY_LEFT_LANE", "LEAVE_HIGHWAY_LEFT_LANE"):
        if new_maneuver == True:
            bash_command("sudo killall -s SIGKILL pngview")
            sleep(.2)
            bash_command("sudo /home/pi/raspidmx/pngview/pngview -n -b 0 -l 3 -x 0 -y 200 /home/pi/Project-Apollo/arrows/split_left.png")
        if turn in ("ENTER_HIGHWAY_RIGHT_LANE"):
            camera.annotate_text= 'Enter Highway ' + upcoming_road + " with Left lane: " + distance_left
        else:
            camera.annotate_text= 'Leave Highway ' + upcoming_road + " with Left lane: " + distance_left

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
def check_g_force(acc):
    
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
        #print "received \"%s\" \n " % data
        if "Connected" in data:
            print data
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
        display(json_str)
        sleep(2)
        q.task_done() # indicate a formerly enqueued task is done
        #it will resume q.join() if it is blocking and resume when all items has been processed
        
    
        
def runServer():
    
    global serverSocket, inputSocket
    # you had indentation problems on this line:
    serverSocket=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1
    print uuid
    serverSocket.bind(("",bluetooth.PORT_ANY))
  
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
    camera.start_preview()
    

try:
    bash_command("sudo modprobe fbtft_device fps=60 txbuflen=32768 name=adafruit18 rotate=270")

    sleep(2)    
    bash_command("sudo fbcp &")   # redirect/copy the all output from fb 0 to fb1 
        
    #turn on camera
    #camera.start_preview()
    # the max G before the RPI trigger the SMS
#    MAX_G = 5
#
#    #intialize the accerelometer
#    acc = ADXL345()
#    acc.setRange(adxl345.RANGE_16G)
#    acc.setBandwidthRate(adxl345.BW_RATE_50HZ)



    global serverSocket, inputSocket 
    name="bt_server"
    target_name="test"
    # some random uuid, generated by https://www.famkruithof.net/uuid/uuidgen
    uuid="0fee0450-e95f-11e5-a837-0800200c9a66"
    serverSocket = None
    inputSocket = None
    
    # start the bluetooth connection with android app
    runServer()
    
    # start a thread that will read from the json queue and display json if available
    displayThread = threading.Thread(target=get_from_queue, args=(json_queue,))
    displayThread.daemon = True
    displayThread.start()
    
    # start a receiving thread
    receiveThread = threading.Thread(target=readIncomingData, args=(inputSocket, json_queue,))
    receiveThread.daemon = True
    receiveThread.start()
        
    # start a sending thread for crash detection    
#    crashThread  = threading.Thread(target=check_g_force, args=(acc,))
#    crashThread.daemon = True
#    crashThread.start()
    while 1:
        sleep(1)
##    distance = 280
##    time = 1
##    while(time > 0):
##        turns= ["GO_STRAIGHT", "UTURN_RIGHT", "KEEP_RIGHT", "LIGHT_RIGHT","KEEP_MIDDLE","KEEP_LEFT","QUITE_LEFT","ENTER_HIGHWAY_RIGHT_LANE","ENTER_HIGHWAY_LEFT_LANE"]
##        for turn in turns:
##            upcoming_road = "Campbell Road"
##            distance_left = str(distance) + "ft"
##            new_maneuver = True
##            turn_update(turn,upcoming_road,distance_left,new_maneuver)
##            distance = distance - 1
##            sleep(8)
##        time = time - 1
##    camera.stop_preview()
##    camera.close()
            
        
    
    
except KeyboardInterrupt, BluetoothError:
    serverSocket.close()
    inputSocket.close()
