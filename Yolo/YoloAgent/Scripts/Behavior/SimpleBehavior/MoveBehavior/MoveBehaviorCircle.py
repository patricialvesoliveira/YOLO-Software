import sys
import time
import numpy

from colour import Color
import pytweening as tween

from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehavior import MoveBehavior


class MoveBehaviorCircle(MoveBehavior):
    # Body body, int repetitions, float duration
    def __init__(self, bodyRef, movementSpeed, movementDirection, repetitions, duration, keepBehaviorSetting=False, startDelay = 0.0):
        MoveBehavior.__init__(self, bodyRef, movementSpeed, movementDirection, repetitions, duration, keepBehaviorSetting, startDelay)
        self.movementType = ShapeType.CIRCLE
    
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
        # alternatively: create signal array with 1024 elements and sample from it according to inputs period and speed

        past_signal_x = 0
        past_signal_y = 0
        totalTime = float(self.animationIntervalTime) / N
        # print "total time " + str(totalTime) + " of a repetition time of " + str(self.animationIntervalTime) + " divided by " + str(len(signal))

        # Note: to do a path backwards we invert the points and their order
        if self.currentMovementDirection == MovementDirection.REVERSE:
            xSignal = reversePath(self, xSignal)

        self.followPath(N, [xSignal[self.currentMovementWaypoint] - past_signal_x, ySignal[self.currentMovementWaypoint] - past_signal_y])
        if reachedNewWaypoint(N):
            past_signal_x = xSignal[self.currentMovementWaypoint - 1]
            past_signal_y = ySignal[self.currentMovementWaypoint - 1]
        return
        