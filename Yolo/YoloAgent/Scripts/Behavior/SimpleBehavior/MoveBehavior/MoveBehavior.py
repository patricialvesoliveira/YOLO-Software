import sys
import time

import numpy

from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.SimpleBehavior import SimpleBehavior


class MoveBehavior(SimpleBehavior):
    def __init__(self, bodyRef, movementSpeed, movementDirection, repetitions, duration, keepBehaviorSetting=False, startDelay = 0.0):
        SimpleBehavior.__init__(self, bodyRef, repetitions, duration, keepBehaviorSetting, startDelay)
        self.behaviorType = BehaviorType.MOVE  # Configuration.Behaviors

        self.waypoints = numpy.array([])

        self.movementSpeed = 0
        self.initialMovementDirection = MovementDirection.NONE
        self.currentMovementDirection = MovementDirection.NONE
        self.alreadyStartedSegment = False

        self.currentWaypointIndex = 0
        self.animationIntervalTime = duration

        self.movementType = ShapeType.NONE
        self.initialMovementDirection = movementDirection
        self.movementSpeed = numpy.clip(movementSpeed, 0, 90)

        self.startTime = time.time()

    # Body agentbody
    def applyBehavior(self):
        # Note: allows for a delayed start
        if self.shouldStartBeDelayed():
            return
        return

    # Body body
    def finishBehavior(self):
        SimpleBehavior.finishBehavior(self)
        self.bodyRef.resetWheelSetup()
        self.currentBehaviorRepetition = 0
        return

    def reversePath(self, path):
        inversedPath = [-x for x in path]
        print "fudge"
        reversedPath = list(reversed(inversedPath))
        return reversedPath

    def followPath(self, pathLength, nextWaypoint):
        
        if not self.alreadyStartedSegment:
            self.alreadyStartedSegment = True
            self.bodyRef.setWheelMovement(nextWaypoint, self.movementSpeed)
            # print "Movement " + str(self.movementType) + " going to " + str(self.currentMovementWaypoint + 1) + " of " + str(pathLength) + " waypoints"
        
        if self.reachedNewWaypoint(pathLength):
            self.currentWaypointIndex += 1
            self.alreadyStartedSegment = False

        # account for last waypoint
        if self.currentWaypointIndex >= pathLength: 
            print self.currentBehaviorRepetition
            if self.currentBehaviorRepetition == self.maxBehaviorRepetitions:
                self.finishBehavior()
                print("Behavior ended")

            # if this movement is alternating then change it after each repetition
            if self.initialMovementDirection == MovementDirection.ALTERNATING:
                if self.currentMovementDirection == MovementDirection.FORWARD:
                    self.currentMovementDirection = MovementDirection.REVERSE
                else:
                    self.currentMovementDirection = MovementDirection.FORWARD

            print "Repetition " + str(self.currentBehaviorRepetition + 1) + " out of " + str(self.maxBehaviorRepetitions)
            self.currentWaypointIndex = 0
            self.currentBehaviorRepetition += 1
            self.alreadyStartedSegment = False
            self.startTime = time.time()
        return

    def reachedNewWaypoint(self, pathLength):
        timePerWaypoint = float(self.animationIntervalTime) / (pathLength)
        return time.time() - self.startTime >= timePerWaypoint * (self.currentWaypointIndex + 1) and self.currentWaypointIndex < pathLength
