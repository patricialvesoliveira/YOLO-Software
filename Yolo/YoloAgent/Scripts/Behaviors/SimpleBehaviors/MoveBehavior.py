import sys
import time

import numpy

from Libs.Constants import *
from Scripts.Behaviors.SimpleBehaviors.Behavior import Behavior


class MoveBehavior(Behavior):
    def __init__(self):
        Behavior.__init__(self)
        self.behaviorType = Behaviors.MOVE  # Configuration.Behaviors

        self.movementTransition = None
        self.movementType = None
        self.movementSpeed = 0
        self.initialMovementDirection = MovementDirection.STANDARD
        self.currentMovementDirection = MovementDirection.STANDARD
        self.currentMovementWaypoint = 0
        self.alreadyStartedSegment = False


    # Body body, int repetitions, float duration
    def prepareBehavior(self, body, movementType, movementSpeed, movementDirection, transition, repetitions, duration, keepBehaviorSetting=False, startDelay = 0.0):
        # Behavior.prepareBehavior(self, body, transition, repetitions, duration, keepBehaviorSetting, startDelay)

        self.movementTransition = transition
        self.movementType = movementType
        self.initialMovementDirection = movementDirection
        self.movementSpeed = numpy.clip(movementSpeed, 0, 90)

        if self.initialMovementDirection == MovementDirection.STANDARD or self.initialMovementDirection == MovementDirection.REVERSE:
            self.currentMovementDirection = self.initialMovementDirection
        elif self.initialMovementDirection == MovementDirection.ALTERNATING:
            self.currentMovementDirection = MovementDirection.STANDARD
        else:
            raise Exception("Error: Type of movement is still unsupported by move behavior.")


    # Body agentbody
    def applyBehavior(self):

        # Note: allows for a delayed start
        if self.shouldStartBeDelayed():
            return

        # TODO: in the future it would be good to stop creating and/or reversing the waypoints everytime this runs
        if self.movementTransition == Transitions.LINEAR:

            if self.movementType == Shapes.SPIKES or self.movementType == Shapes.RECT or self.movementType == Shapes.FORWARD_AND_BACK or self.movementType == Shapes.STRAIGHT:
                if self.movementType == Shapes.SPIKES:
                    waypoints = numpy.array([[1, 1], [1, -1]])

                elif self.movementType == Shapes.RECT:
                    waypoints = numpy.array([[1, 0], [0, 1], [1, 0], [0, -1]])

                elif self.movementType == Shapes.FORWARD_AND_BACK:
                    waypoints = numpy.array([[1, 0], [-1, 0]])
                elif self.movementType == Shapes.STRAIGHT:
                    waypoints = numpy.array([[1, 0]])
                else:
                    raise Exception("Error: This if should only select if the movebehavior is SPIKES, RECT, STRAIGHT and FORWARD_AND_BACK but it caught something else")

                # Note: to do a path backwards we invert the points and their order
                if self.currentMovementDirection == MovementDirection.REVERSE:
                    negatedWaypoints = [ -x for x in waypoints]
                    waypoints = list(reversed(negatedWaypoints))

                totalTime = float(self.animationIntervalTime) / len(waypoints)

                if time.time() - self._startTime >= totalTime * (self.currentMovementWaypoint + 1) and self.currentMovementWaypoint + 1 < len(waypoints):
                    self.currentMovementWaypoint += 1
                    self.alreadyStartedSegment = False

                if not self.alreadyStartedSegment:
                    self.alreadyStartedSegment = True
                    self.bodyRef.setWheelMovement(self.movementType, waypoints[self.currentMovementWaypoint], self.movementSpeed)
                    print "Movement " + str(self.movementType) + " going to " + str(
                        self.currentMovementWaypoint + 1) + " of " + str(len(waypoints)) + " waypoints"

            elif self.movementType == Shapes.CURVED:
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
                    negatedSignal = [-x for x in signal]
                    signal = list(reversed(negatedSignal))
                    x_dist = - x_dist

                if time.time() - self._startTime >= totalTime * (
                            self.currentMovementWaypoint + 1) and self.currentMovementWaypoint + 1 < N:
                    self.currentMovementWaypoint += 1
                    past_signal = signal[self.currentMovementWaypoint - 1]
                    self.alreadyStartedSegment = False

                if not self.alreadyStartedSegment:
                    self.alreadyStartedSegment = True
                    self.bodyRef.setWheelMovement(self.movementType, [x_dist, signal[self.currentMovementWaypoint] - past_signal],
                                          self.movementSpeed)
                    print "Movement " + str(self.movementType) + " going to " + str(self.currentMovementWaypoint + 1) + " of " + str(N) + " waypoints"

            elif self.movementType == Shapes.LOOPS:
                # create array of circle values
                N = 24  # number of samples; 16 for quicker behavior
                # period = N*0.1 seconds
                ix = numpy.arange(N)
                rad = 20  # radius, arbitrary
                xSignal = numpy.cos(2 * numpy.pi / N * ix) * rad  # x values for circle
                ySignal = numpy.sin(2 * numpy.pi / N * ix) * rad  # y values for circle
                x_dist = 4  # constant x value for forward motion
                # alternatively: create signal array with 1024 elements and sample from it according to inputs period and speed

                past_signal_x = 20
                past_signal_y = 0
                totalTime = float(self.animationIntervalTime) / N
                # print "total time " + str(totalTime) + " of a repetition time of " + str(self.animationIntervalTime) + " divided by " + str(len(signal))

                # Note: to do a path backwards we invert the points and their order
                if self.currentMovementDirection == MovementDirection.REVERSE:
                    negatedXSignal = [-x for x in xSignal]
                    xSignal = list(reversed(negatedXSignal))
                    #negatedYSignal = [-y for y in ySignal]
                    #ySignal = list(reversed(negatedYSignal))
                    x_dist = -x_dist

                if time.time() - self._startTime >= totalTime * (self.currentMovementWaypoint + 1) and self.currentMovementWaypoint + 1 < N:
                    self.currentMovementWaypoint += 1
                    past_signal_x = xSignal[self.currentMovementWaypoint - 1]
                    past_signal_y = ySignal[self.currentMovementWaypoint - 1]
                    self.alreadyStartedSegment = False

                if not self.alreadyStartedSegment:
                    self.alreadyStartedSegment = True
                    self.bodyRef.setWheelMovement(self.movementType,
                                          [xSignal[self.currentMovementWaypoint] - past_signal_x + x_dist, ySignal[self.currentMovementWaypoint] - past_signal_y], self.movementSpeed)
                    print "Movement " + str(self.movementType) + " going to " + str(
                        self.currentMovementWaypoint + 1) + " of " + str(N) + " waypoints"

            elif self.movementType == Shapes.CIRCLE:
                # create array of circle values
                N = 24  # number of samples; 16 for quicker behavior
                # period = N*0.1 seconds
                ix = numpy.arange(N)
                rad = 20  # radius, arbitrary
                xSignal = numpy.cos(2 * numpy.pi / N * ix) * rad  # x values for circle
                ySignal = numpy.sin(2 * numpy.pi / N * ix) * rad  # y values for circle
                # alternatively: create signal array with 1024 elements and sample from it according to inputs period and speed

                past_signal_x = 0
                past_signal_y = 0
                totalTime = float(self.animationIntervalTime) / N
                # print "total time " + str(totalTime) + " of a repetition time of " + str(self.animationIntervalTime) + " divided by " + str(len(signal))

                # Note: to do a path backwards we invert the points and their order
                if self.currentMovementDirection == MovementDirection.REVERSE:
                    negatedXSignal = [-x for x in xSignal]
                    xSignal = list(reversed(negatedXSignal))
                    #negatedYSignal = [-y for y in ySignal]
                    #ySignal = list(reversed(negatedYSignal))

                if time.time() - self._startTime >= totalTime * (
                    self.currentMovementWaypoint + 1) and self.currentMovementWaypoint + 1 < N:
                    self.currentMovementWaypoint += 1
                    past_signal_x = xSignal[self.currentMovementWaypoint - 1]
                    past_signal_y = ySignal[self.currentMovementWaypoint - 1]
                    self.alreadyStartedSegment = False

                if not self.alreadyStartedSegment:
                    self.alreadyStartedSegment = True
                    self.bodyRef.setWheelMovement(self.movementType,
                                          [xSignal[self.currentMovementWaypoint] - past_signal_x,
                                           ySignal[self.currentMovementWaypoint] - past_signal_y],
                                          self.movementSpeed)
                    print "Movement " + str(self.movementType) + " going to " + str(
                        self.currentMovementWaypoint + 1) + " of " + str(N) + " waypoints"
            else:
                raise Exception("Error: Move behavior doesn't support this movement type. Please add it!")

        else:
            raise Exception("Error: Move behavior doesn't support this transition type. Please add it!")

        # when the animation is over we pause before changing color
        if time.time() - self._startTime > self.animationIntervalTime:
            if self._currentBehaviorRepetition == self._maxBehaviorRepetitions:
                self.isOver = True
                self.finalizeEffects()
                print("Behavior ended")
                return

            # if this movement is alternating then change it after each repetition
            if self.initialMovementDirection == MovementDirection.ALTERNATING:
                if self.currentMovementDirection == MovementDirection.STANDARD:
                    self.currentMovementDirection = MovementDirection.REVERSE
                else:
                    self.currentMovementDirection = MovementDirection.STANDARD

            print "Repetition " + str(self._currentBehaviorRepetition + 1) + " out of " + str(self._maxBehaviorRepetitions)
            self.currentMovementWaypoint = 0
            self._currentBehaviorRepetition += 1
            self.alreadyStartedSegment = False
            self._startTime = time.time()

        return


    # Body body
    def finalizeEffects(self):
        self.bodyRef.resetWheelSetup()
        self.isOver = True

        pass
