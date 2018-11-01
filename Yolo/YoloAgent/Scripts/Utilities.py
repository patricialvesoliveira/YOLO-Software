class Utilities:
	@staticmethod
	def changeScale(value, leftMin, leftMax, rightMin, rightMax):
		# Figure out how 'wide' each range is
		leftSpan = leftMax - leftMin
		rightSpan = rightMax - rightMin

		# Convert the left range into a 0-1 range (float)
		valueScaled = float(value - leftMin) / float(leftSpan)

		# Convert the 0-1 range into a value in the right range.
		return rightMin + (valueScaled * rightSpan)

	def toggleApplicationMode(self,agent):
		if agent.body.applicationMode == ApplicationMode.AUTONOMOUS:
			agent.body.applicationMode = ApplicationMode.DEMO
		elif agent.body.applicationMode == ApplicationMode.DEMO:
			agent.body.applicationMode = ApplicationMode.AUTONOMOUS
		
		print ("Switched application mode to " + agent.body.applicationMode.name)