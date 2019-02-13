import sys
import time
import numpy

from colour import Color
import pytweening as tween

from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehavior import MoveBehavior


class MoveBehaviorCurved(MoveBehavior):
    # Body body, int repetitions, float duration
    def __init__(self, bodyRef, movementSpeed, movementDirection, repetitions, duration, keepBehaviorSetting=False, startDelay = 0.0):
        MoveBehavior.__init__(self, bodyRef, movementSpeed, movementDirection, repetitions, duration, keepBehaviorSetting, startDelay)
        self.movementType = ShapeType.CURVED
    
    def behaviorActions(self):
        MoveBehavior.behaviorActions(self)
        
        # create array of sin wave values
        N = 48  # number of samples; 24 for quicker behavior
        ix = numpy.arange(N)
        amp = 20  # amplitude, arbitrary
        signal = numpy.sin(2 * numpy.pi * ix / float(N / 2)) * amp  # y values for 2 sine waves
        x_dist = amp / (N / 8)  # constant x value

        past_signal = 0
        totalTime = float(self.animationIntervalTime) / N

        # Note: to do a path backwards we invert the points and their order
        if self.currentMovementDirection == MovementDirection.REVERSE:
            signal = self.reversePath(signal)
            x_dist = - x_dist


        self.followPath(N, [x_dist, signal[self.currentWaypointIndex] - past_signal])
        if self.reachedNewWaypoint(N):
            past_signal = signal[self.currentWaypointIndex - 1]
        return