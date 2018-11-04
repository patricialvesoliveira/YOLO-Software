import sys
import threading
import time
from Libs.Constants import *


class SimpleBehavior:
    def __init__(self, bodyRef, repetitions, duration, keepBehaviorSetting, startDelay = 0.0):
        self.behaviorType = Behaviors.BASE  # Configuration.Behaviors
        
        self.isOver = True
        self.hasStarted = False

        self.startDelay = startDelay

        self.keepBehaviorSetting = keepBehaviorSetting
        self.behaviorDuration = duration;

        self.maxBehaviorRepetitions = repetitions
        self.animationIntervalTime = self.behaviorDuration / self.maxBehaviorRepetitions
        self.currentBehaviorRepetition = 1

        self.bodyRef = bodyRef

        self.startTime = 0

    def startBehavior(self):
        if self.maxBehaviorRepetitions > 0 and self.behaviorDuration > 0.0:
            self.startTime = time.time()
            self.isOver = False
        return

    # Body agentbody
    def applyBehavior(self):
        raise NotImplementedError("Please Implement this method")

    # Body body
    def finalizeEffects(self):
        raise NotImplementedError("Please Implement this method")

    def shouldStartBeDelayed(self):
        timeDelta = 0.005
        # Note: allows for a delayed start
        if not self.hasStarted and self.startDelay - (time.time() - self.startTime) > timeDelta:
            return True
        elif not self.hasStarted and self.startDelay - (time.time() - self.startTime) < timeDelta:
            self.hasStarted = True
            self.startTime = time.time()
            return False
        else:
            return False

    # behaviors can be halted by children touching the robot, this updates the start time to account for time stopped
    def updateStartTimeAfterHalt(self, totalTimeDelay):
        self.startTime += totalTimeDelay
        return