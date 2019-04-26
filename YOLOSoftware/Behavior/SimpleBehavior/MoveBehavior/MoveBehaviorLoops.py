import sys
import time
import numpy

from colour import Color
import pytweening as tween

from Libs.Constants import *
from YOLOSoftware.Behavior.SimpleBehavior.MoveBehavior.MoveBehavior import MoveBehavior


class MoveBehaviorLoops(MoveBehavior, object):
    def __init__(self, bodyRef, movementSpeed, movementDirection, repetitions, duration):
        super(MoveBehaviorLoops, self).__init__(bodyRef, movementSpeed, movementDirection, repetitions, duration)
    
    def behaviorActions(self):
        super(MoveBehaviorLoops, self).behaviorActions()
        # create array of semi-circles points
        numSamples = 24 
        ix = numpy.arange(numSamples)
        radius = 20
        xSignal = numpy.cos(2 * numpy.pi / numSamples * ix) * radius
        ySignal = numpy.sin(2 * numpy.pi / numSamples * ix) * radius
        x_dist = 4  # constant x value for forward motion

        past_signal_x = 20
        past_signal_y = 0
        totalTime = float(self.animationIntervalTime) / numSamples

        #To do a path backwards we invert the points and their order
        if self.currentMovementDirection == MovementDirection.REVERSE:
            x_dist = -x_dist

        self.followPath(numSamples, [xSignal[self.currentWaypointIndex] - past_signal_x + x_dist, ySignal[self.currentWaypointIndex] - past_signal_y])
        if self.reachedNewWaypoint(numSamples):
            past_signal_x = xSignal[self.currentWaypointIndex - 1]
            past_signal_y = ySignal[self.currentWaypointIndex - 1]
        return
        