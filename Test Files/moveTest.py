import RPi.GPIO as GPIO
import os
import time
import numpy as np
  
#set up pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT) #motor 2 pwm
GPIO.setup(27,GPIO.OUT) #motor 2 direction
GPIO.setup(20,GPIO.OUT)  #motor 3 pwm
GPIO.setup(21,GPIO.OUT)  #motor 3 direction
GPIO.setup(19,GPIO.OUT) #motor 1 pwm
GPIO.setup(26,GPIO.OUT) #motor 1 direction

#set up PWM
frequency = 20  #PWM frequency, motor RPM = 5
dc = 0         #duty cycle (0-100)
a = GPIO.PWM(19,frequency) #motor 1
b = GPIO.PWM(17,frequency) #motor 2
c = GPIO.PWM(20,frequency)  #motor 3
a.start(dc)
b.start(dc)
c.start(dc)

global A1
global B1
global C1
global A2
global B2
global C2
A1=0
B1=0
C1=0
A2=1
B2=1
C2=1

start_time = time.time()

def transform(x,y,w):
    initial = [[y],[x],[w]]
    transform = [[0.333,-0.577,0.333],[-0.667,0,0.333],[0.333,0.577,0.333]]
    forces = np.matmul(transform,initial)
    return forces


def Eastmove2point(x,y,max_speed):
    global A1
    global B1
    global C1
    global A2
    global B2
    global C2
    controls=transform(x,y,0)
    MAX=max(abs(controls))[0]
    A1new=abs(controls[0])
    B1new=abs(controls[1])
    C1new=abs(controls[2])
    A2new=np.sign(controls[0])
    B2new=np.sign(controls[1])
    C2new=np.sign(controls[2])
    if (A1new != A1):
        ANEW=(A1new/MAX)*max_speed #scaler: usually 100 for fast, 60 for slow
        a.ChangeDutyCycle(ANEW) #changes wheel 1 duty cycle (speed)
        A1=A1new #updates compare value with current value
    if (B1new != B1):
        BNEW=(B1new/MAX)*max_speed
        b.ChangeDutyCycle(BNEW)
        B1=B1new
    if (C1new != C1):
        CNEW=(C1new/MAX)*max_speed
        c.ChangeDutyCycle(CNEW)
        C1=C1new
    if (A2new != A2):
        #change pin output to high or low; 1 is low, -1 is high
        if (A2new<0):
            GPIO.output(26,1)
        else:
            GPIO.output(26,0)
        A2=A2new
    if (B2new != B2):
        if (B2new<0):
            GPIO.output(27,1)
        else:
            GPIO.output(27,0)
        B2=B2new
    if (C2new != C2):
        if (C2new<0):
            GPIO.output(21,1)
        else:
            GPIO.output(21,0)
        C2=C2new


#def Pathmove2point(x,y,w):


def linear(speed,leg_time):
    Eastmove2point(1,0,speed)
    time.sleep(leg_time)
    A1=0
    B1=0
    C1=0
    A2=1
    B2=1
    C2=1


def serious(speed,leg_time):
    #set of points for one serious motion
    points = np.array([[1,0],[0,1],[1,0],[0,-1]])
    for j in range(2): #repeat 2 times
        for i in range(points.shape[0]):
            Eastmove2point(points[i,0],points[i,1],speed)
            time.sleep(leg_time)
    A1=0
    B1=0
    C1=0
    A2=1
    B2=1
    C2=1


def spikes(speed,leg_time):
    #set of points for one spike motion
    points = np.array([[1,1],[1,-1]])
    for j in range(4): #repeat 4 times
        for i in range(points.shape[0]):
            Eastmove2point(points[i,0],points[i,1],speed)
            time.sleep(leg_time)
    A1=0
    B1=0
    C1=0
    A2=1
    B2=1
    C2=1


def curly(speed):
    #create array of sin wave values
    N = 48 #number of samples; 24 for quicker behavior
        #period = (N/2)*0.1 seconds
    ix = np.arange(N)
    amp = 20 #amplitude, arbitrary
    signal = np.sin(2*np.pi*ix/float(N/2))*amp #y values for 2 sine waves
    x_dist = amp/(N/8) #constant x value
        #alternatively: create signal array with 1024 elements and sample from it according to inputs period and speed

    past_signal = 0
    for i in range(N):
        Eastmove2point(x_dist,signal[i]-past_signal,speed)
        time.sleep(0.1)
        past_signal=signal[i]
    A1=0
    B1=0
    C1=0
    A2=1
    B2=1
    C2=1


def loops(speed):
    #create array of circle values
    N = 24 #number of samples; 16 for quicker behavior
        #period = N*0.1 seconds
    ix = np.arange(N)
    rad = 20 #radius, arbitrary
    xSignal = np.cos(2*np.pi/N*ix)*rad #x values for circle
    ySignal = np.sin(2*np.pi/N*ix)*rad #y values for circle
    x_dist = 4 #constant x value for forward motion
        #alternatively: create signal array with 1024 elements and sample from it according to inputs period and speed

    past_signal_x = 20
    past_signal_y = 0
    for j in range(3): #repeat 3 times
        for i in range(N):
            Eastmove2point(xSignal[i]-past_signal_x+x_dist,ySignal[i]-past_signal_y,speed)
            time.sleep(0.1)
            past_signal_x=xSignal[i]
            past_signal_y=ySignal[i]
    A1=0
    B1=0
    C1=0
    A2=1
    B2=1
    C2=1


def circle(speed):
    # create array of circle values
    N = 24  # number of samples; 16 for quicker behavior
    # period = N*0.1 seconds
    ix = np.arange(N)
    rad = 20  # radius, arbitrary
    xSignal = np.cos(2 * np.pi / N * ix) * rad  # x values for circle
    ySignal = np.sin(2 * np.pi / N * ix) * rad  # y values for circle
    x_dist = 0  # constant x value for forward motion
    # alternatively: create signal array with 1024 elements and sample from it according to inputs period and speed

    past_signal_x = 0
    past_signal_y = 0
    for j in range(2):  # repeat 2 times
        for i in range(N):
            Eastmove2point(xSignal[i] - past_signal_x + x_dist, ySignal[i] - past_signal_y, speed)
            time.sleep(0.1)
            past_signal_x = xSignal[i]
            past_signal_y = ySignal[i]

    # should be run every time a behavior is finished
    A1=0
    B1=0
    C1=0
    A2=1
    B2=1
    C2=1

def main():        
    try:
        while (time.time()-start_time < 10):
            speed = 60
            circle(speed)
            #print 'linear'
            #linear(speed,2)
            #print 'spikes'
            #spikes(speed,0.5)
            #print 'serious'
            #serious(speed,0.5)
            #print 'curly'
            #curly(speed)
            #print 'loops'
            #loops(speed)
            print 'done'
        GPIO.output(26,0)
        GPIO.output(27,0)
        GPIO.output(21,0)
        a.stop()
        b.stop()
        c.stop()
        GPIO.cleanup()
    except KeyboardInterrupt:
        GPIO.output(26,0)
        GPIO.output(27,0)
        GPIO.output(21,0)
        a.stop()
        b.stop()
        c.stop()
        GPIO.cleanup()  

if __name__=="__main__":
    main()

