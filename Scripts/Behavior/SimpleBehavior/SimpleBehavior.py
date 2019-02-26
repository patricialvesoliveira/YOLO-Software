import sys
import threading
import time
from Libs.Constants import *


class SimpleBehavior:
    def __init__(self, bodyRef, repetitions, duration, keepBehaviorSetting, startDelay = 0.0):
        self.behaviorType = BehaviorType.NONE
        self.isOver = False
        self.hasStarted = False
        self.startDelay = startDelay
        self.keepBehaviorSetting = keepBehaviorSetting
        self.duration = duration;
        self.maxBehaviorRepetitions = repetitions

        if self.maxBehaviorRepetitions > 0:
            self.animationIntervalTime = self.duration / self.maxBehaviorRepetitions
        else:
            self.animationIntervalTime = self.duration

        self.currentBehaviorRepetition = 1
        self.bodyRef = bodyRef
        self.startTime = time.time()

    def resetBehavior(self):
        self.isOver = False
        self.hasStarted = False
        self.currentBehaviorRepetition = 1
        self.startTime = time.time()
        
    def applyBehavior(self):
        if(not self.isOver):
            self.behaviorActions()
        else:
            print "behavior not applied as it was finished!"

    def behaviorActions(self):
        # to be overridden
        return

    def finishBehavior(self):
        print "Behavior ended well"
        self.isOver = True
