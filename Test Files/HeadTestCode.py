import RPi.GPIO as GPIO
import time
import argparse

start_time = time.time()

#set up pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT) #pwm

#set up PWM
frequency = 50  #PWM frequency
dc = 7.5         #duty cycle (2.5 (max speed Up), 7.5 (stop), 12.5 (maxspeed down) )
h = GPIO.PWM(17,frequency)
h.start(dc)

def move(speed, timeSeconds):
    h.ChangeDutyCycle(speed) #changes wheel 1 duty cycle (speed)
    time.sleep(timeSeconds)

def main(speed, timeSeconds):
	
	try:
		#run at high speed up
		#speed = 2.5; 
		#time = .5;
		#move(speed, time)
		#
		##run at high speed down
		#speed = 12.5; 
		#time = .5;
		#move(speed, time)
		#
		##run at low speed up
		#speed = 7.0; 
		#time = .5;
		#move(speed, time)

		#run at low speed down
		#speed = 8.0 
		#move(speed, 0.5)

		#speed = 7.0 
		#move(speed, 2.5)

		#stop
		#speed = 7.5; 
		#move(speed, 0.5)

		move(speed, timeSeconds)

		h.stop() 
		GPIO.cleanup()

		# 7.5 slowly down - 8.0 quick down - 5.0 medium up - 6.5 slowly up - 7.0 stop

	except KeyboardInterrupt as e:
		h.stop() 
		GPIO.cleanup()
		raise e

	except Exception as e:
		GPIO.cleanup()
		raise e

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='head startup')
    parser.add_argument('--speed', metavar='float', type=float, default=7.0, help='Speed value to be passed for testing.')
    parser.add_argument('--time', metavar='float', type=float, default=0.25, help='Time value to be passed for testing.')
    args = parser.parse_args()
    main(speed=args.speed, timeSeconds=args.time)

