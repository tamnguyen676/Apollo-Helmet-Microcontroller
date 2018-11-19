def bash_command(bash_cmd):
    import subprocess
    subprocess.Popen(bash_cmd, stdout=subprocess.PIPE, shell=True)

import picamera
from PIL import Image
from time import sleep
TIME = 2

camera = picamera.PiCamera()    # set up camera

camera.resolution = (1280, 720) # set up resolution
camera.framerate = 24
camera.brightness = 75
camera.contrast = 75
camera.annotate_text= 'Hello world!' # example template for inserting text, call .annotate_text will just override it
camera.annotate_text_size = 120      # text size
sleep(1)

# set up the display, needs to be in the start up
#bash_command("sudo modprobe fbtft_device fps=60 txbuflen=32768 name=tm022hdh26 rotate=90") 


camera.start_preview()                     # start the preview

bash_command("sudo rpi-fbcp/build/fbcp &")   # redirect/copy the all output from fb 0 to fb1 
while TIME > 0:
    
    camera.annotate_text= 'Start of the loop'
    # Insert a png, put our directions here
    bash_command("sudo raspidmx/pngview/pngview -n -b 0 -l 3 -x 0 -y 80 /home/pi/Left_300.png") 
    
    wait = raw_input("presse")
    
    # clear the png (direction arrow) before changing
    bash_command("sudo killall -s SIGKILL pngview")
    sleep(.2)
    
    bash_command("sudo raspidmx/pngview/pngview -n -b 0 -l 3 -x 950 -y 80 /home/pi/Right_350.png") 
    
    
    wait = raw_input("presse")
    bash_command("sudo killall -s SIGKILL pngview")
    sleep(.2)
    
    bash_command("sudo raspidmx/pngview/pngview -n -b 0 -l 3 -x 450 -y 80 /home/pi/Straight_400.png") 

    wait = raw_input("presse")
    bash_command("sudo killall -s SIGKILL pngview")
    camera.annotate_text= 'End of the loop!'
    wait = raw_input("presse")
    TIME = TIME - 1
# Wait indefinitely until the user terminates the script

camera.stop_preview()
camera.close()
##while True:
##    sleep(1)
