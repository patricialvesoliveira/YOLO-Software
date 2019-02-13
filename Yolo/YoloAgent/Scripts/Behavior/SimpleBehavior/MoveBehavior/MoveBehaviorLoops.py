import sys
import time
import numpy

from colour import Color
import pytweening as tween

from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehavior import MoveBehavior


class MoveBehaviorLoops(MoveBehavior):
    # Body body, int repetitions, float duration
    def __init__(self, bodyRef, movementSpeed, movementDirection, repetitions, duration, keepBehaviorSetting=False, startDelay = 0.0):
        MoveBehavior.__init__(self, bodyRef, movementSpeed, movementDirection, repetitions, duration, keepBehaviorSetting, startDelay)
        self.movementType = ShapeType.LOOPS
    	return
    
    def behaviorActions(self):
        MoveBehavior.behaviorActions(self)
        
        # create array of circle values
        N = 24  # number of samples; 16 for quicker behavior
        ix = numpy.arange(N)
        rad = 20  # radius, arbitrary
        xSignal = numpy.cos(2 * numpy.pi / N * ix) * rad  # x values for circle
        ySignal = numpy.sin(2 * numpy.pi / N * ix) * rad  # y values for circle
        x_dist = 4  # constant x value for forward motion

        past_signal_x = 20
        past_signal_y = 0
        totalTime = float(self.animationIntervalTime) / N

        # Note: to do a path backwards we invert the points and their order
        if self.currentMovementDirection == MovementDirection.REVERSE:
            x_dist = -x_dist

        self.followPath(N, [xSignal[self.currentWaypointIndex] - past_signal_x + x_dist, ySignal[self.currentWaypointIndex] - past_signal_y])
        if self.reachedNewWaypoint(N):
            past_signal_x = xSignal[self.currentWaypointIndex - 1]
            past_signal_y = ySignal[self.currentWaypointIndex - 1]
        return
        