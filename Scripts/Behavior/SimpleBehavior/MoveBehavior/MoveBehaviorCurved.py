import sys
import time
import numpy

from colour import Color
import pytweening as tween

from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehavior import MoveBehavior


class MoveBehaviorCurved(MoveBehavior, object):
    def __init__(self, bodyRef, movementSpeed, movementDirection, repetitions, duration):
        super(MoveBehaviorCurved, self).__init__(bodyRef, movementSpeed, movementDirection, repetitions, duration)
    
    def behaviorActions(self):
        super(MoveBehaviorCurved, self).behaviorActions()
        # create array of sin wave values
        numSamples = 48
        ix = numpy.arange(numSamples)
        amplitude = 20
        signal = numpy.sin(2 * numpy.pi * ix / float(numSamples / 2)) * amplitude
        x_dist = amplitude / (numSamples / 8)

        past_signal = 0
        totalTime = float(self.animationIntervalTime) / numSamples

        #to do a path backwards we reverse the order of the path points
        if self.currentMovementDirection == MovementDirection.REVERSE:
            signal = self.reversePath(signal)
            x_dist = - x_dist


        self.followPath(numSamples, [x_dist, signal[self.currentWaypointIndex] - past_signal])
        if self.reachedNewWaypoint(numSamples):
            past_signal = signal[self.currentWaypointIndex - 1]