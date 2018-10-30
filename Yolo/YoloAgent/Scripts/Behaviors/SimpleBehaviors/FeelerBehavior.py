import sys
import time

import numpy

from Libs.Constants import *
import pytweening as tween

from Scripts.Behaviors.SimpleBehaviors.Behavior import Behavior


class FeelerBehavior(Behavior):
    def __init__(self):
        Behavior.__init__(self)

        self.behaviorType = Behaviors.FEELER  # Configuration.Behaviors
        self._animationEndPause = 0
        self.extensionTransition = Transitions.LINEAR

        # value between 0 (completely retracted) and 100 (fully extended) for the agent's feelers
        self.startFeelerPosition = 0
        self.endFeelerPosition = 0

        #transition parameters - allow to keep the same average speed at the end of transition, covering the desired distance
        self.easeInSpeedMultiplier = 2.75194
        self.easeOutSpeedMultiplier = 1.5708

        return

    #NOTE: feeler position is a percentage value, between 0 - 100
    def prepareBehavior(self, body, endFeelerPosition, transition, repetitions, duration, keepBehaviorSetting=False, startDelay = 0.0, animationPause = 0.0):
        Behavior.prepareBehavior(self, body, transition, repetitions, duration, keepBehaviorSetting, startDelay)

        self.startFeelerPosition = body.getFeelerPosition()
        self.endFeelerPosition = endFeelerPosition
        self.extensionTransition = transition
        self._animationEndPause = animationPause

        totalDistance = self.endFeelerPosition - self.startFeelerPosition

        #NOTE: no point in starting if distance to travel is zero
        if numpy.isclose(totalDistance, 0):
            return

        #NOTE: if the transition is instant try to get to the end point ASAP
        if self.extensionTransition == Transitions.INSTANT:

            if totalDistance > 0:
                #Maximum positive speed to get there as quickly as possible
                topSpeed = 100
                self._behaviorDuration = topSpeed * (totalDistance * body.getGearRatio())

            else:
                # Maximum negative speed to get there as quickly as possible
                topSpeed = -100
                self._behaviorDuration = topSpeed * (totalDistance * body.getGearRatio())

            self._animationIntervalTime = self._behaviorDuration / self._maxBehaviorRepetitions
            self.extensionTransition = Transitions.LINEAR

        #NOTE: Always check if it's possible to achieve a certain point with the parameters given and correct the values if needed
        else:
            topSpeed = 100
            actualTime = body.getFeelerMovementTime(totalDistance, topSpeed)
            if actualTime > duration/repetitions:
                self._animationIntervalTime = actualTime
                self._behaviorDuration = self._animationIntervalTime * self._maxBehaviorRepetitions
                print("New timeframe for animation: " + str(actualTime) + " seconds")
        #TODO - probably will have to test if the distance can be done at the received speed and adjust the behavior accordingly
        #TODO - DONE?

        #NOTE: If using easeFunction adjust speed so that while the function changes the speed it never goes out of the motor range
        if self.extensionTransition == Transitions.EASEIN or self.extensionTransition == Transitions.EASEIN or self.extensionTransition == Transitions.EASEINOUT:

            body.getFeelerMovementTime(totalDistance, 100)

            #if body.getFeelerMovementTime(totalDistance, 100) > self._animationIntervalTime:
            #    actualTime = body.getFeelerMovementTime(totalDistance, topSpeed)
            #    self._animationIntervalTime = actualTime
            #    self._behaviorDuration = self._animationIntervalTime * self._maxBehaviorRepetitions

            #    if body.getFeelerMovementTime(totalDistance, 100) > self._animationIntervalTime:
            #        raise Exception("Animation error: Could not compensate for give timeframe")


        return

    # Body body
    def applyBehavior(self, body):

        #Note: allows for a delayed start
        if self.shouldStartBeDelayed():
            return

        totalDistance = self.endFeelerPosition - self.startFeelerPosition

        if numpy.isclose(totalDistance, 0):
            self.isOver = True

        if self.extensionTransition == Transitions.LINEAR:
            lerp = (time.time() - self._startTime) / self._animationIntervalTime
            body.setFeelerMovement(body.getFeelerSpeed(totalDistance, self._animationIntervalTime))
            #NOTE: since this animation has a constant speed we know the increase in distance covered as time progresses
            body.setFeelerPosition(self.startFeelerPosition + totalDistance * lerp)
            #print("Applying feeler mov: passed " + str((time.time() - self._startTime)) + " of " + str(
            #    self._animationIntervalTime) + ". Lerp: " + str(lerp))

        elif self.extensionTransition == Transitions.EASEIN:
            timeElapsed = time.time() - self._startTime
            lerp = tween.easeInSine(numpy.clip(timeElapsed / self._animationIntervalTime, 0, 1))
            body.setFeelerMovement(body.getFeelerSpeed(totalDistance, self._animationIntervalTime) * lerp * self.easeInSpeedMultiplier)
            body.setFeelerPosition(self.startFeelerPosition + totalDistance * lerp)

        elif self.extensionTransition == Transitions.EASEOUT:
            timeElapsed = time.time() - self._startTime
            lerp = tween.easeOutSine(numpy.clip(timeElapsed / self._animationIntervalTime, 0, 1))
            body.setFeelerMovement(body.getFeelerSpeed(totalDistance, self._animationIntervalTime) * lerp * self.easeOutSpeedMultiplier)
            body.setFeelerPosition(self.startFeelerPosition + totalDistance * lerp)

        elif self.extensionTransition == Transitions.EASEINOUT:
            totalTime = self._animationIntervalTime / 2

            if time.time() - self._startTime <= totalTime:
                timeElapsed = time.time() - self._startTime
                # TODO - watch out for the magic number - when you know the speed come back to test this
                # TODO - you might have to check from the get go if the 2.~ something multiplier makes the speed higher than the motor supports
                lerp = tween.easeInSine(numpy.clip(timeElapsed / totalTime, 0, 1))
                body.setFeelerMovement(body.getFeelerSpeed(totalDistance, self._animationIntervalTime) * lerp * self.easeInSpeedMultiplier)
                body.setFeelerPosition(self.startFeelerPosition + totalDistance * lerp)

                # print("easing in: " + lerp)
            # when the  animation is over  we pause before changing color
            elif time.time() - self._startTime >= totalTime + self._animationEndPause:
                timeElapsed = (time.time() - self._startTime - self._animationEndPause) - totalTime
                # TODO - watch out for the magic number - when you know the speed come back to test this
                # TODO - you might have to check from the get go if the 1.~ something multiplier makes the speed higher than the motor supports
                lerp = (1 - tween.easeOutSine(numpy.clip(timeElapsed / totalTime, 0, 1)))
                body.setFeelerMovement(body.getFeelerSpeed(totalDistance, self._animationIntervalTime) * lerp  * self.easeOutSpeedMultiplier)
                body.setFeelerPosition(self.startFeelerPosition + totalDistance * lerp)

                # print("easing out: " + (1 - lerp))

            print("Applying feeler mov: passed " + str((time.time() - self._startTime)) + " of " + str(
                self._animationIntervalTime) + ". Lerp: " + str(lerp))
            #print("WARNING: o setFeelerPos esta a funcionar com o lerp portanto esta perfeito, mas e um valor falso e incorrecto ")

                # when the animation is over we pause before changing color
        if time.time() - self._startTime > self._animationIntervalTime + self._animationEndPause:
            if self._currentBehaviorRepetition == self._maxBehaviorRepetitions:
                self.finalizeEffects(body)
                # print("Behavior ended")
                return
            self._currentBehaviorRepetition += 1
            self._startTime = time.time()

        return

    # Body body
    def finalizeEffects(self, body):

        body.setFeelerMovement(0)

        if self.keepBehaviorSetting == True:
            body.setFeelerPosition(self.endFeelerPosition)
            print("Setting the animation end feeler position")

        self.isOver = True

        return
