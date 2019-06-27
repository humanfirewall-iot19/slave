#! /usr/bin/env python3

from gpiozero import Button
from time import sleep
from hashlib import sha256
from picamera import PiCamera

slave_callback = lambda x: None
camera = None
button = None

# get the board serial number
def get_id():
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

def ring():
    global camera
    camera.capture('/home/pi/photo.jpg')
    slave_callback('/home/pi/photo.jpg')

def register_handler(cb):
    global slave_callback
    slave_callback = cb

def device_setup_and_idle():
    global camera, button
    #initialize the button
    button = Button(3)
    #initialize the camera
    camera = PiCamera()
    #camera.resolution = (1920, 1080)
    camera.resolution = (1280, 720)
    camera.rotation = 180
    #we get the sha256 hash of the board's serial and enconde it in utf8
    serial = get_id()
    #register the callback
    button.when_pressed = ring

    while True:
        sleep(1)

