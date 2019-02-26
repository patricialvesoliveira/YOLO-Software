from Libs.Constants import *

class ComposedBehavior:
    def __init__(self, bodyRef):
        self.bodyRef = bodyRef
        self.behaviorList = []
        self.behaviorDuration = 0.0
        self.startTime = 0.0
        self.isOver = False
        self.behaviorHalted = False
        self.behaviorType = ComposedBehaviorType.NONE

    def applyBehavior(self):
        behaviorsToApply = self.behaviorList
        areAllOver = True
        for behavior in behaviorsToApply:
            if not behavior.isOver:
                areAllOver = False
                behavior.applyBehavior()
        if areAllOver:
            self.finishBehavior()
        if self.isOver : print("Composed behavior is over")

    def resetBehavior(self):
        self.startTime = 0.0
        self.isOver = False
        self.behaviorHalted = False
        for behavior in self.behaviorList:
            behavior.resetBehavior()

    def finishBehavior(self):
        for behavior in self.behaviorList:
            behavior.finishBehavior()
        self.isOver = True
