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
        self.isOver = False
        self.behaviorHalted = False
        self.behaviorType = ComposedBehaviorType.NONE


    def applyBehavior(self):
        behaviorsToApply = []

        #print ("Applying " + str(self.behaviorType))
        behaviorsToApply = self.behaviorList

        for behavior in behaviorsToApply:
            if not behavior.isOver:
                behavior.applyBehavior()

        #if self.isOver : print("Composed behavior is over")

    def finishBehavior(self):
        for behavior in self.behaviorList:
            behavior.finishBehavior()

        self.isOver = True
