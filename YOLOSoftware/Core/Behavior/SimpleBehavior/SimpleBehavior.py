import sys
import threading
import time
from Libs.Constants import *


class SimpleBehavior(object):
    def __init__(self, bodyRef, maxBehaviorRepetitions, duration):
        self.isOver = False
        self.duration = duration;
        self.maxBehaviorRepetitions = maxBehaviorRepetitions
        self.currentBehaviorRepetition = 0
        self.bodyRef = bodyRef
        self.startTime = time.time()

    def behaviorActions(self):
        if(self.isOver):
            return     
        if(self.checkForBehaviorEnd()):
            if(self.maxBehaviorRepetitions == 0):
                # infinite repetitions OO
                self.resetBehavior()
                return
            self.currentBehaviorRepetition += 1
            if(self.currentBehaviorRepetition >= self.maxBehaviorRepetitions):
                self.finishBehavior()
            else:
                self.startTime = time.time()
        
    def resetBehavior(self):
        self.startTime = time.time()
        self.isOver = False
        self.currentBehaviorRepetition = 0
        
    def applyBehavior(self):
        # print "cr: " + str(self.currentBehaviorRepetition)
        if(not self.isOver):
            self.behaviorActions()
        else:
            print "behavior not applied as it was finished!"

    def finishBehavior(self):
        print "Behavior ended well"
        self.isOver = True
