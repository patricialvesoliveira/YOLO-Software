from Libs.Constants import *
import time


class ComposedBehavior:
    def __init__(self, bodyRef):
        # standard behaviors
        self.bodyRef = bodyRef
        self.behaviorList = []

        # generic variables
        self.behaviorDuration = 0.0
        self.startTime = 0.0
        self.isOver = True
        self.behaviorHalted = False
        self.behaviorType = ComposedBehaviorType.NONE

    def startBehavior(self):
        self.startTime = time.time()
        self.isOver = False

        for behavior in self.behaviorList:
            behavior.startBehavior()

        print("Starting " + self.behaviorType.name)

    def applyBehavior(self):
        self.isOver = True
        behaviorsToApply = []

        #print ("Applying " + str(self.behaviorType))
        behaviorsToApply = self.behaviorList

        for behavior in behaviorsToApply:
            if not behavior.isOver:
                behavior.applyBehavior()
                if self.isOver:
                    self.isOver = False

        #if self.isOver : print("Composed behavior is over")

    def updateStartTimeAfterHalt(self, totalTimeDelay):
        for behavior in self.behaviorList:
            behavior.updateStartTimeAfterHalt(totalTimeDelay)

    def haltAndFinishBehavior(self):
        for behavior in self.behaviorList:
            behavior.finishBehavior()
