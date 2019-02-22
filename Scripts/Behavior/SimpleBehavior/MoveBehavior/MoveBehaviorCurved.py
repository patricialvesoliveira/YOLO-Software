import sys
import time
import numpy

from colour import Color
import pytweening as tween

from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehavior import MoveBehavior


class MoveBehaviorCurved(MoveBehavior):
    def __init__(self, bodyRef, movementSpeed, movementDirection, repetitions, duration, keepBehaviorSetting=False, startDelay = 0.0):
        MoveBehavior.__init__(self, bodyRef, movementSpeed, movementDirection, repetitions, duration, keepBehaviorSetting, startDelay)
        self.movementType = ShapeType.CURVED
    
    def behaviorActions(self):
        MoveBehavior.behaviorActions(self)
        
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