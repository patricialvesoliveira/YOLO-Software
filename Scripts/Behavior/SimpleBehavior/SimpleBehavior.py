import sys
import threading
import time
from Libs.Constants import *


class SimpleBehavior:
    def __init__(self, bodyRef, maxBehaviorRepetitions, duration):
        self.isOver = False
        self.duration = duration;
        self.maxBehaviorRepetitions = maxBehaviorRepetitions
        self.currentBehaviorRepetition = 0
        if self.maxBehaviorRepetitions > 0:
            self.animationIntervalTime = self.duration / self.maxBehaviorRepetitions
        else:
            self.animationIntervalTime = self.duration
        self.bodyRef = bodyRef

    def initBehavior(self):
        # to be overridden
        self.startTime = time.time()

    def behaviorActions(self):
        # to be overridden
        pass

    def resetBehavior(self):
        self.isOver = False
        self.currentBehaviorRepetition = 0
        self.startTime = time.time()
        self.initBehavior()
        
    def applyBehavior(self):
        if(not self.isOver):
            self.behaviorActions()
        else:
            print "behavior not applied as it was finished!"

    def finishBehavior(self):
        print "Behavior ended well"
        self.isOver = True
