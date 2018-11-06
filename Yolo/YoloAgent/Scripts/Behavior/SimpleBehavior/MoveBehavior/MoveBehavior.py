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
        self.currentMovementWaypoint = 0
        self.alreadyStartedSegment = False


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

        # when the animation is over we pause before changing color
        if time.time() - self._startTime > self.animationIntervalTime:
            if self._currentBehaviorRepetition == self.maxBehaviorRepetitions:
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

            print "Repetition " + str(self._currentBehaviorRepetition + 1) + " out of " + str(self._maxBehaviorRepetitions)
            self.currentMovementWaypoint = 0
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
        reversedPath = [ -x for x in waypoints]
        path = list(reversed(negatedWaypoints))
        return reversedPath

    def followPath(self, path, currentWaypointIndex):
        pathLength = len(path)

        if reachedNewWaypoint(pathLength):
            self.currentWaypointIndex += 1
            self.alreadyStartedSegment = False

        if not self.alreadyStartedSegment:
            self.alreadyStartedSegment = True
            self.bodyRef.setWheelMovement(path[currentWaypointIndex], self.movementSpeed)
            print "Movement " + str(self.movementType) + " going to " + str(self.currentMovementWaypoint + 1) + " of " + str(pathLength) + " waypoints"
        return

    def reachedNewWaypoint(self, pathLength):
        timePerWaypoint = float(self.animationIntervalTime) / pathLength
        return time.time() - self.startTime >= timePerWaypoint * (self.currentWaypointIndex + 1) and self.currentWaypointIndex + 1 < pathLength
