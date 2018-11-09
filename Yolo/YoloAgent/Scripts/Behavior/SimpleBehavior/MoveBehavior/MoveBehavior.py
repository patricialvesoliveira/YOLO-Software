import sys
import time

import numpy

from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.SimpleBehavior import SimpleBehavior


class MoveBehavior(SimpleBehavior):
    def __init__(self, bodyRef, movementSpeed, movementDirection, transition, repetitions, duration, keepBehaviorSetting=False, startDelay = 0.0):
        SimpleBehavior.__init__(self, bodyRef, repetitions, duration, keepBehaviorSetting, startDelay)
        self.behaviorType = BehaviorType.MOVE  # Configuration.Behaviors

        self.waypoints = numpy.array([])

        self.movementSpeed = 0
        self.initialMovementDirection = MovementDirection.NONE
        self.currentMovementDirection = MovementDirection.NONE
        # self.currentMovementWaypointIndex = 0
        self.alreadyStartedSegment = False

        self.currentWaypointIndex = 0
        self.animationIntervalTime = duration

        self.movementTransition = transition
        self.movementType = ShapeType.NONE
        self.initialMovementDirection = movementDirection
        self.movementSpeed = numpy.clip(movementSpeed, 0, 90)

        if self.initialMovementDirection == MovementDirection.FORWARD or self.initialMovementDirection == MovementDirection.REVERSE:
            self.currentMovementDirection = self.initialMovementDirection
        elif self.initialMovementDirection == MovementDirection.ALTERNATING:
            self.currentMovementDirection = MovementDirection.FORWARD
        else:
            raise Exception("Error: Type of movement is still unsupported by move behavior.")

    # Body agentbody
    def applyBehavior(self):

        # Note: allows for a delayed start
        if self.shouldStartBeDelayed():
            return

        print "current time: " + str(time.time() - self.startTime)
        print "fart: "+ str((time.time() - self.startTime) > self.animationIntervalTime)
        # when the animation is over we pause before changing color
        if (time.time() - self.startTime) > self.animationIntervalTime:
            if self.currentBehaviorRepetition == self.maxBehaviorRepetitions:
                self.isOver = True
                self.finishBehavior()
                print("Behavior ended")
                return

            # if this movement is alternating then change it after each repetition
            if self.initialMovementDirection == MovementDirection.ALTERNATING:
                if self.currentMovementDirection == MovementDirection.FORWARD:
                    self.currentMovementDirection = MovementDirection.REVERSE
                else:
                    self.currentMovementDirection = MovementDirection.FORWARD

            print "Repetition " + str(self.currentBehaviorRepetition + 1) + " out of " + str(self.maxBehaviorRepetitions)
            # self.currentMovementWaypointIndex = 0
            self.currentBehaviorRepetition += 1
            self.alreadyStartedSegment = False
            self.startTime = time.time()
        return

    # Body body
    def finishBehavior(self):
        SimpleBehavior.finishBehavior(self)
        self.bodyRef.resetWheelSetup()
        return

    def reversePath(self, path):
        inversedPath = [-x for x in path]
        print "fudge"
        reversedPath = list(reversed(inversedPath))
        return reversedPath

    def followPath(self, pathLength, nextWaypoint):
        
        if self.reachedNewWaypoint(pathLength):
            self.currentWaypointIndex += 1
            self.alreadyStartedSegment = False
        if not self.alreadyStartedSegment:
            self.alreadyStartedSegment = True
            self.bodyRef.setWheelMovement(nextWaypoint, self.movementSpeed)
            # print "Movement " + str(self.movementType) + " going to " + str(self.currentMovementWaypoint + 1) + " of " + str(pathLength) + " waypoints"
        return

    def reachedNewWaypoint(self, pathLength):
        timePerWaypoint = float(self.animationIntervalTime) / pathLength
        return time.time() - self.startTime >= timePerWaypoint * (self.currentWaypointIndex + 1) and self.currentWaypointIndex + 1 < pathLength
