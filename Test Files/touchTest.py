import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

#set the GPIO input pins
pad1 = 16
pad2 = 12
#pad3 = 24
#pad4 = 23

GPIO.setup(pad1, GPIO.IN)
GPIO.setup(pad2, GPIO.IN)
#PIO.setup(pad3, GPIO.IN)
#GPIO.setup(pad4, GPIO.IN)

pad1alreadyPressed = False
pad2alreadyPressed = False
#pad3alreadyPressed = False
#pad4alreadyPressed = False


while True:
    pad1pressed = not GPIO.input(pad1)
    pad2pressed = not GPIO.input(pad2)
#    pad3pressed = not GPIO.input(pad3)
    #pad4pressed = not GPIO.input(pad4)
    
    if pad1pressed and not pad1alreadyPressed:
        print "Pad 1 pressed"
    pad1alreadyPressed = pad1pressed

    if pad2pressed and not pad2alreadyPressed:
        print "Pad 2 pressed"
    pad2alreadyPressed = pad2pressed

    time.sleep(0.1)