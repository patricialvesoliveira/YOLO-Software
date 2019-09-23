from Core.Enumerations import *

class ComposedBehavior(object):
    def __init__(self, controlRef, behaviorList):
        self.controlRef = controlRef
        self.behaviorList = behaviorList
        self.isOver = False

    def applyBehavior(self):
        behaviorsToApply = list(self.behaviorList)
        areAllOver = True
        for behavior in behaviorsToApply:
            if not behavior.isOver:
                areAllOver = False
                behavior.applyBehavior()
        if areAllOver:
            self.finishBehavior()

    def resetBehavior(self):
        self.isOver = False
        for behavior in self.behaviorList:
            behavior.resetBehavior()

    def finishBehavior(self):
        for behavior in self.behaviorList:
            behavior.finishBehavior()
        self.isOver = True
