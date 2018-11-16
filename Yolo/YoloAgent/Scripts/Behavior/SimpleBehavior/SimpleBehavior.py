import sys
import threading
import time
from Libs.Constants import *


class SimpleBehavior:
    def __init__(self, bodyRef, repetitions, duration, keepBehaviorSetting, startDelay = 0.0):
        self.behaviorType = BehaviorType.NONE  # Configuration.Behaviors
        
        self.isOver = False
        self.hasStarted = False

        self.startDelay = startDelay

        self.keepBehaviorSetting = keepBehaviorSetting
        self.behaviorDuration = duration;

        self.maxBehaviorRepetitions = repetitions

        if self.maxBehaviorRepetitions > 0:
            self.animationIntervalTime = self.behaviorDuration / self.maxBehaviorRepetitions
        else:
            self.animationIntervalTime = self.behaviorDuration

        self.currentBehaviorRepetition = 1

        self.bodyRef = bodyRef

        self.startTime = time.time()
        return
        

    # Body agentbody
    def applyBehavior(self):
        if(not self.isOver):
            self.behaviorActions()
        else:
            print "aaaaaaaaaaaaaaaaaaa"
        return

    def behaviorActions(self):
        return

    # Body body
    def finishBehavior(self):
        self.isOver = True
        return

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