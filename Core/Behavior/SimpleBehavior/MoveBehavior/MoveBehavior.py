import sys
import time

import numpy

from Core.Enumerations import *
from Core.Behavior.SimpleBehavior.SimpleBehavior import SimpleBehavior


class MoveBehavior(SimpleBehavior, object):
    def __init__(self, bodyRef, movementSpeed, movementDirection, maxBehaviorRepetitions, duration):
        super(MoveBehavior, self).__init__(bodyRef, maxBehaviorRepetitions, duration)
        self.waypoints = numpy.array([])
        self.movementSpeed = 0
        self.animationIntervalTime = duration
        self.movementType = ShapeType.NONE
        self.initialMovementDirection = movementDirection

        if self.initialMovementDirection == MovementDirection.ALTERNATING:
            self.currentMovementDirection = MovementDirection.FORWARD
        else:
            self.currentMovementDirection = self.initialMovementDirection
            
        self.movementSpeed = numpy.clip(movementSpeed, 0, 90)
        self.initBehavior()

    def initBehavior(self):
        self.alreadyStartedSegment = False
        self.pathLength = 1; #to avoid returning in the first iteration 
        self.currentWaypointIndex = 0
        self.startTime = time.time()

    def behaviorActions(self):
        super(MoveBehavior, self).behaviorActions()

        if self.checkForBehaviorEnd(): 
            # if this movement is alternating then change it after each repetition
            if self.initialMovementDirection == MovementDirection.ALTERNATING:
                if self.currentMovementDirection == MovementDirection.FORWARD:
                    self.currentMovementDirection = MovementDirection.REVERSE
                else:
                    self.currentMovementDirection = MovementDirection.FORWARD
            self.startTime = time.time()
            self.currentWaypointIndex = 0
            self.alreadyStartedSegment = False

    def finishBehavior(self):
        super(MoveBehavior, self).finishBehavior()
        self.bodyRef.resetWheelSetup()

    def reversePath(self, path):
        inversedPath = [-x for x in path]
        reversedPath = list(reversed(inversedPath))
        return reversedPath

    def followPath(self, pathLength, nextWaypoint):
        if(self.isOver):
            return

        self.pathLength = pathLength

        if not self.alreadyStartedSegment:
            self.alreadyStartedSegment = True
            self.bodyRef.setWheelMovement(nextWaypoint, self.movementSpeed)

        if self.reachedNewWaypoint(pathLength):
            self.currentWaypointIndex += 1
            self.alreadyStartedSegment = False
        

    def reachedNewWaypoint(self, pathLength):
        timePerWaypoint = float(self.animationIntervalTime) / (pathLength)
        return time.time() - self.startTime >= timePerWaypoint * (self.currentWaypointIndex + 1) and self.currentWaypointIndex < (pathLength)
  
    def checkForBehaviorEnd(self):
        return self.currentWaypointIndex > (self.pathLength - 1)