import sys
import threading
import time
from Libs.Constants import *


class Behavior:
    def __init__(self, body, repetitions, duration, keepBehaviorSetting, startDelay = 0.0):
        self.behaviorType = Behaviors.BASE  # Configuration.Behaviors
        
        self.isOver = True
        self.hasStarted = False

        self.startDelay = startDelay

        self.keepBehaviorSetting = keepBehaviorSetting
        self._behaviorDuration = duration;

        self._maxBehaviorRepetitions = repetitions
        self._animationIntervalTime = self._behaviorDuration / self._maxBehaviorRepetitions
        self._currentBehaviorRepetition = 1


    def startBehavior(self):
        if self._maxBehaviorRepetitions > 0 and self._behaviorDuration > 0.0:
            self._startTime = time.time()
            self.isOver = False
        return

    # Body agentbody
    def applyBehavior(self, body):
        raise NotImplementedError("Please Implement this method")

    # Body body
    def finalizeEffects(self, body):
        raise NotImplementedError("Please Implement this method")

    def shouldStartBeDelayed(self):
        timeDelta = 0.005
        # Note: allows for a delayed start
        if not self.hasStarted and self.startDelay - (time.time() - self._startTime) > timeDelta:
            return True
        elif not self.hasStarted and self.startDelay - (time.time() - self._startTime) < timeDelta:
            self.hasStarted = True
            self._startTime = time.time()
            return False
        else:
            return False

    # behaviors can be halted by children touching the robot, this updates the start time to account for time stopped
    def updateStartTimeAfterHalt(self, totalTimeDelay):
        self._startTime += totalTimeDelay
        return