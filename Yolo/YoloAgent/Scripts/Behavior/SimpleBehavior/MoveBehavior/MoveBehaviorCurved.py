import sys
import time
import numpy

from colour import Color
import pytweening as tween

from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehavior import MoveBehavior


class MoveBehaviorCurved(MoveBehavior):
    # Body body, int repetitions, float duration
    def __init__(self, bodyRef, movementSpeed, movementDirection, transition, repetitions, duration, keepBehaviorSetting=False, startDelay = 0.0):
        MoveBehavior.__init__(self, bodyRef, movementSpeed, movementDirection, transition, repetitions, duration, keepBehaviorSetting, startDelay)
        self.movementType = ShapeType.CURVED
    
    # Body body
    def applyBehavior(self):
        MoveBehavior.applyBehavior(self)
        
        # create array of sin wave values
        N = 48  # number of samples; 24 for quicker behavior
        # period = (N/2)*0.1 seconds
        ix = numpy.arange(N)
        amp = 20  # amplitude, arbitrary
        signal = numpy.sin(2 * numpy.pi * ix / float(N / 2)) * amp  # y values for 2 sine waves
        x_dist = amp / (N / 8)  # constant x value
        # alternatively: create signal array with 1024 elements and sample from it according to inputs period and speed

        past_signal = 0
        totalTime = float(self.animationIntervalTime) / N
        #print "total time " + str(totalTime) + " of a repetition time of " + str(self.animationIntervalTime) + " divided by " + str(len(signal))

        # Note: to do a path backwards we invert the points and their order
        if self.currentMovementDirection == MovementDirection.REVERSE:
            signal = reversePath(self, signal)
            x_dist = - x_dist


        self.followPath(N, [x_dist, signal[self.currentMovementWaypoint] - past_signal])
        if reachedNewWaypoint(N):
            past_signal = signal[self.currentMovementWaypoint - 1]
        return