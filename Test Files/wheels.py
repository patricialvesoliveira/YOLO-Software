import RPi.GPIO as GPIO
import os
import time
#from Libs.Constants import *

# Pin functions
PIN_MOTOR1 = 15
PIN_MOTOR1_DIRECTION = 18
PIN_MOTOR2 = 5
PIN_MOTOR2_DIRECTION = 6
PIN_MOTOR3 = 19
PIN_MOTOR3_DIRECTION = 26


class WheelMovement:
	"""docstring for Body"""

	def __init__(self):
		# set up pins
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(PIN_MOTOR1, GPIO.OUT)
		GPIO.setup(PIN_MOTOR1_DIRECTION, GPIO.OUT)

		GPIO.setup(PIN_MOTOR2, GPIO.OUT)
		GPIO.setup(PIN_MOTOR2_DIRECTION, GPIO.OUT)

		GPIO.setup(PIN_MOTOR3, GPIO.OUT)
		GPIO.setup(PIN_MOTOR3_DIRECTION, GPIO.OUT)

		# these just reverse directions
		GPIO.output(PIN_MOTOR1_DIRECTION, 0)
		GPIO.output(PIN_MOTOR3_DIRECTION, 0)
		GPIO.output(PIN_MOTOR2_DIRECTION, 0)

		# set up PWM
		PWMFrequency = 20  # PWM frequency, motor RPM = 5
		# dc = 90         #duty cycle (0-100)
		self.Motor1 = GPIO.PWM(PIN_MOTOR1, PWMFrequency)
		self.Motor2 = GPIO.PWM(PIN_MOTOR2, PWMFrequency)
		self.Motor3 = GPIO.PWM(PIN_MOTOR3, PWMFrequency)
		self.Motor1.stop()
		self.Motor2.stop()
		self.Motor3.stop()

		# initialize clock
		start_time = time.time()

		return

	def startMovement(self, movement):

		# TODO -- missing all other behaviors
		#if movement == Shapes.SPIKES:
		#    self.performZigzag(60, 1.5)
		self.performZigzag(60, 1.5)


	def performZigzag(self, dutyCicles, stepTime):

		GPIO.output(PIN_MOTOR3_DIRECTION, 1)
		self.Motor1.start(dutyCicles)
		self.Motor3.start(dutyCicles)

		time.sleep(stepTime)

		GPIO.output(PIN_MOTOR3_DIRECTION, 0)
		self.Motor1.stop()
		self.Motor3.stop()

		GPIO.output(PIN_MOTOR1_DIRECTION, 1)
		self.Motor1.start(dutyCicles)
		self.Motor2.start(dutyCicles)

		time.sleep(stepTime)

		GPIO.output(PIN_MOTOR1_DIRECTION, 0)
		self.Motor1.stop()
		self.Motor2.stop()

	def cleanupGPIOPins(self):

		try:
			GPIO.cleanupGPIOPins()
			print("Cleaned up GPIO Successfully")
		except Exception:
			print("ERROR: There was a problem cleaning up GPIO")


if __name__ == "__main__":
	mov = WheelMovement()

	# initialize clock
	start_time = time.time()

	while (time.time() - start_time < 15):
		print 'a0'
		mov.performZigzag(60, 1.5)
		print 'a1'
		mov.performZigzag(60, 1.5)
		print 'a2'
		mov.performZigzag(100, 1.5)
		print 'a3'
		mov.performZigzag(100, 1.5)
		print 'done'

