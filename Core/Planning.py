import time
import numpy
from colour import Color
from Core.Enumerations import *
from MachineLearning.util import extract_features, predict

from Core.BehaviorImports import *

class Planning(object):
    def __init__(self, control, generalProfile, socialProfile, creativityProfile):

        self.generalProfile = generalProfile
        self.socialProfile = socialProfile
        self.creativityProfile = creativityProfile
        self.control = control
        self.currBehavior = ComposedBehavior(control, [])
        tCurr = time.time()

        self.startTime = tCurr
        self.tLastTouchI = tCurr
        self.tLastTouchF = tCurr
        self.wasTouched = False

        self.socialOrCreativeTriggered = False

        self.currStoryArcMoment = StoryArc.NONE
        self.currRecognizedShape = ShapeType.NONE
        
        self.isInteractionStarted = False
        self.isInteractionFinished = False
        self.isPlanningFinished = False

        self.tLastAttentionCall = tCurr
        
    def update(self):
        self.control.update()
        self.currBehavior.applyBehavior()

        tCurr = time.time()
        tSinceStart = tCurr - self.startTime

        risingActionTime = self.creativityProfile.risingActionTimeInMinutes 
        climaxTime = self.creativityProfile.climaxTimeInMinutes 
        fallingActionTime = self.creativityProfile.fallingActionTimeInMinutes 

        # update curr story arc moment
        if (tSinceStart > 0 and tSinceStart <= risingActionTime*60):
            self.currStoryArcMoment = StoryArc.RISING_ACTION
        elif (tSinceStart > risingActionTime*60 and tSinceStart <= (risingActionTime + climaxTime)*60):
            self.currStoryArcMoment = StoryArc.CLIMAX
        elif (tSinceStart > (risingActionTime+ climaxTime)*60 and tSinceStart <= (risingActionTime + climaxTime + fallingActionTime)*60):
            self.currStoryArcMoment = StoryArc.FALLING_ACTION
        elif tSinceStart > (risingActionTime + climaxTime + fallingActionTime)*60 and not self.isInteractionFinished:
            self.resetCurrAndSetNewBehavior(self.generalProfile.goodbyeBehavior)
            self.isInteractionFinished = True
            return

        tLastTouchDelta = self.tLastTouchF - self.tLastTouchI
        
        # pupeteer behavior stuff
        if self.hasTouchStarted():
            self.attentionCallTriggered = False
            self.socialOrCreativeTriggered = False
            self.resetCurrAndSetNewBehavior(self.generalProfile.pupeteerBehavior)

        elif self.hasTouchEnded():
            self.tLastAttentionCall = self.tLastTouchF;
            self.currBehavior.finishBehavior() # finish any pending behavior

            #hello is performed on the first touch
            if not self.isInteractionStarted:
                self.resetCurrAndSetNewBehavior(self.generalProfile.helloBehavior)
                self.isInteractionStarted = True

        #do nothing until first touch
        if not self.isInteractionStarted:
            # constantly reinit startTime until robot starts
            self.startTime = tCurr
            return

        # autonomous stuff
        if not self.beingTouched():
            if (tCurr - self.tLastAttentionCall) > self.socialProfile.attentionCallBehaviorDelayInSeconds:
                self.tLastAttentionCall = time.time() #simulate touch to reset timer
                self.resetCurrAndSetNewBehavior(self.socialProfile.attentionCallBehavior)
            else:
                if not self.socialOrCreativeTriggered and tLastTouchDelta > self.generalProfile.minimumTouchTimeInSeconds:
                    self.socialOrCreativeTriggered = True
                    
                    possibleBehaviors = []
                    socialBehavior = self.generatesocialBehavior()
                    if(socialBehavior):
                        print "[INFO] Adding social behavior..."
                        possibleBehaviors.append(socialBehavior)
                    creativityBehavior = self.generateCreativityBehavior(self.currStoryArcMoment, self.currRecognizedShape)
                    if(creativityBehavior):
                        print "[INFO] Adding creativity behavior..."
                        possibleBehaviors.append(creativityBehavior)

                    if(len(possibleBehaviors)==0):
                        self.resetCurrAndSetNewBehavior(ComposedBehavior(self.control, []))
                    else:
                        self.resetCurrAndSetNewBehavior(numpy.random.choice(possibleBehaviors))

        # idle acts as fallback
        if self.currBehavior.isOver:
            if(self.isInteractionFinished):
                self.isPlanningFinished = True
                return
            self.resetCurrAndSetNewBehavior(self.generalProfile.idleBehavior)

        # check for recognized shapes
        if self.shapeWasRecognized():
            self.currRecognizedShape = self.predictShape(self.control.getOpticalSensor().getCurrentRecognizedShape())
        

    def resetCurrAndSetNewBehavior(self, newBehavior):
        self.currBehavior.finishBehavior() # finish any pending behavior
        self.currBehavior = newBehavior
        self.currBehavior.resetBehavior()  #reset behavior before application

    def generatesocialBehavior(self):
        socialBehaviorList = self.socialProfile.socialBehaviorList
        if(not socialBehaviorList):
            return False
        selectedBehavior = numpy.random.choice(socialBehaviorList)
        return selectedBehavior

    def generateCreativityBehavior(self, currStoryArcMoment, recognizedShape):        
        creativityBehaviorDict = {}
        creativityBehaviorType = None

        if(currStoryArcMoment == StoryArc.NONE):
            return False
        elif(currStoryArcMoment == StoryArc.RISING_ACTION):
            creativityBehaviorDict = self.creativityProfile.risingActionBehaviorDict   
            creativityBehaviorType = self.creativityProfile.risingActionBehaviorType
        elif(currStoryArcMoment == StoryArc.CLIMAX):
            creativityBehaviorDict = self.creativityProfile.climaxBehaviorDict   
            creativityBehaviorType = self.creativityProfile.climaxBehaviorType
        elif(currStoryArcMoment == StoryArc.FALLING_ACTION):
            creativityBehaviorDict = self.creativityProfile.fallingActionBehaviorDict   
            creativityBehaviorType = self.creativityProfile.fallingActionBehaviorType

        currShapedBehavior = creativityBehaviorDict.get(recognizedShape, None)
        if(currShapedBehavior == None):
            return False

        selectedBehavior = None;
        if(creativityBehaviorType==StoryArcBehaviorType.MIRROR):
            selectedBehavior = currShapedBehavior
        elif(creativityBehaviorType==StoryArcBehaviorType.CONTRAST):
            behaviorList = list(creativityBehaviorDict.values())
            behaviorList.remove(currShapedBehavior)
            selectedBehavior = numpy.random.choice(behaviorList)
        return selectedBehavior

    def beingTouched(self):
        return (self.control.getTouchSensor().getState() == TouchState.TOUCHING)

    def shapeWasRecognized(self):
        return (self.control.getOpticalSensor().getState() == OpticalState.FINISHED)

    def hasTouchStarted(self):
        result = not self.wasTouched and self.beingTouched()
        if(result):
            self.wasTouched = True
            self.tLastTouchI = time.time()
        return result
    
    def hasTouchEnded(self):
        result = self.wasTouched and not self.beingTouched()
        if(result):
            self.wasTouched = False
            self.tLastTouchF = time.time()
        return result

    def predictShape(self, pointDataArray):
        features = extract_features(pointDataArray)
        prediction = predict(features)[0]
        print "::::::::::::::::::::::Recognized the shape: " + str(prediction) + ":::::::::::::::::::::::::::"
        return ShapeType(int(prediction)+1)