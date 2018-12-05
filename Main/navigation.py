import json # for JSON object parsing
from time import sleep

#returns a boolean if a string is valid json
def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError:
    return False
  return True

def bash_command(bash_cmd):
    import subprocess
    subprocess.Popen(bash_cmd, stdout=subprocess.PIPE, shell=True)
    
# function to update the LCD display
def turn_update(turn, upcoming_road, distance_left, new_maneuver, camera):      
    
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
