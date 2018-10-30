from evdev import InputDevice
from select import select

dev = InputDevice('/dev/input/event0') #YOURS MIGHT BE event1

while True:
    r,w,x = select([dev], [], [])
    for event in dev.read():
        # The event.code for a scroll wheel event is 8, so I do the following
        #button left 272, right 273
        if event.code == 0:
            print "rel_x"
            print(event.value)
        elif event.code == 1:
            print "rel_y"
            print(event.value)
        elif event.code == 8:
            print "wheel"
            print(event.value)
        elif event.code == 272:
            print "left button"
            print(event.value)
        elif event.code == 273:
            print "right button"
            print(event.value)
