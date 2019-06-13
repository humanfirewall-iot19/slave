#! /usr/bin/env python3
from gpiozero import Button
from time import sleep
from hashlib import sha256
from picamera import PiCamera
#import requests

# get the board serial number
def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close()
        cpuserial=sha256(cpuserial.encode("utf-8")).hexdigest()
    except:
        cpuserial = "ERROR000000000"
    return cpuserial

#ring callback
def ring():
    #camera.start_preview()
    #sleep(5)
    camera.capture('/home/pi/photo.jpg')
    #camera.stop_preview()
    print("took photo")
    #sending data to server

#initialize the button
button = Button(3)
#initialize the camera
camera=PiCamera()
camera.resolution = (1920, 1080)
camera.rotation=180
#we get the sha256 hash of the board's serial and enconde it in utf8
serial=getserial()
#serial=sha256(getserial().encode("utf-8")).hexdigest()
#register the callback
button.when_pressed=ring
while True:
    sleep(1)
