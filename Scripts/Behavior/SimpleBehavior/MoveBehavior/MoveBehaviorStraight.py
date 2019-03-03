import sys
import time
import numpy

from colour import Color
import pytweening as tween

from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehavior import MoveBehavior


class MoveBehaviorStraight(MoveBehavior):
    def __init__(self, bodyRef, movementSpeed, movementDirection, repetitions, duration):
        MoveBehavior.__init__(self, bodyRef, movementSpeed, movementDirection, repetitions, duration)
    	self.waypoints = numpy.array([[1, 0]])
    
    def behaviorActions(self):
        MoveBehavior.behaviorActions(self)

        #To do a path backwards we invert the points and their order
        if self.currentMovementDirection == MovementDirection.REVERSE:
            self.waypoints = self.reversePath(self.waypoints)

        self.followPath(len(self.waypoints), self.waypoints[self.currentWaypointIndex])