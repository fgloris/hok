import os
import time
import sys
import subprocess


button_dict = {
    "home": (1500,1060),
    "recover": (1600,1030),
    "summoner skill": (1780,1080),
    "skill 1": (1950,1050),
    "skill 2": (2100,850),
    "skill 3": (2300,700),
    "skill 1+": (1900,1000),
    "skill 2+": (1950,750),
    "skill 3+": (2200,550),
    }

def touch(x,y):
    os.system("adb shell input tap " + str(x) + " " + str(y))

def click(button):
    x,y = button_dict[button]
    touch(x,y)
    if button == "home":
        time.sleep(7)

def move(x,y,time):
    x = x/((x*x+y*y)**0.5)
    y = y/((x*x+y*y)**0.5)
    x*=1000
    y*=1000
    start_x = 500
    start_y = 800
    end_x = x+start_x
    end_y = y+start_y
    os.system("adb shell input swipe " + str(start_x) + " " + str(start_y)+ " " + str(end_x) + " " + str(end_y) + " " + str(time*1000))

#click("home")
click("home")
click("skill 1")
move(1,-1,7)
click("skill 1")
move(1,-1,7)
click("skill 2")
for i in range(10):
    time.sleep(0.5)