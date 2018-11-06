import sys
import time
import numpy

from colour import Color
import pytweening as tween

from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehavior import MoveBehavior


class MoveBehaviorLoops(MoveBehavior):
    # Body body, int repetitions, float duration
    def __init__(self, bodyRef, movementSpeed, movementDirection, transition, repetitions, duration, keepBehaviorSetting=False, startDelay = 0.0):
        MoveBehavior.__init__(self, bodyRef, movementSpeed, movementDirection, transition, repetitions, duration, keepBehaviorSetting, startDelay)
        self.movementType = ShapeType.LOOPS
    	return
    
    # Body body
    def applyBehavior(self):
        MoveBehavior.applyBehavior(self)
        
        # create array of circle values
        N = 24  # number of samples; 16 for quicker behavior
        # period = N*0.1 seconds
        ix = numpy.arange(N)
        rad = 20  # radius, arbitrary
        xSignal = numpy.cos(2 * numpy.pi / N * ix) * rad  # x values for circle
        ySignal = numpy.sin(2 * numpy.pi / N * ix) * rad  # y values for circle
        x_dist = 4  # constant x value for forward motion
        # alternatively: create signal array with 1024 elements and sample from it according to inputs period and speed

        past_signal_x = 20
        past_signal_y = 0
        totalTime = float(self.animationIntervalTime) / N
        # print "total time " + str(totalTime) + " of a repetition time of " + str(self.animationIntervalTime) + " divided by " + str(len(signal))

        # Note: to do a path backwards we invert the points and their order
        if self.currentMovementDirection == MovementDirection.REVERSE:
            signal = reversePath(self, signal)
            x_dist = -x_dist

        self.followPath(N, [xSignal[self.currentMovementWaypoint] - past_signal_x + x_dist, ySignal[self.currentMovementWaypoint] - past_signal_y])
        if reachedNewWaypoint(N):
            past_signal_x = xSignal[self.currentMovementWaypoint - 1]
            past_signal_y = ySignal[self.currentMovementWaypoint - 1]
        return
        