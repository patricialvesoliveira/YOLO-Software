import time
import numpy
from colour import Color
from Libs.Constants import *
from Libs.MachineLearning.lib.constants import SHAPE_ARRAY
from Libs.MachineLearning.lib.util import extract_features, predict

from Scripts.BehaviorImports import *

class Mind:
    def __init__(self, body, personalityProfile, creativityProfile):

        self.personalityProfile = personalityProfile
        self.creativityProfile = creativityProfile
        self.body = body
        self.currBehavior = ComposedBehavior(body)
        tCurr = time.time()

        self.startTime = tCurr
        self.tLastTouchI = tCurr
        self.tLastTouchF = tCurr
        self.wasTouched = False

        self.personalityOrCreativeTriggered = False

        self.currStoryArcMoment = StoryArc.NONE
        self.currRecognizedShape = "NONE"
        
        self.isInteractionStarted = False
        self.isInteractionFinished = False

        self.tLastAttentionCall = tCurr

    def update(self):
        self.body.update()
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
            self.currBehavior.finishBehavior() # finish any pending behavior
            self.currBehavior = HelloBehavior(self.body)
            self.isInteractionFinished = True

        tLastTouchDelta = self.tLastTouchF - self.tLastTouchI
        
        # pupeteer behavior stuff
        if self.hasTouchStarted():
            self.attentionCallTriggered = False
            self.personalityOrCreativeTriggered = False

            self.currBehavior.finishBehavior() # finish any pending behavior
            self.currBehavior = PuppeteerBehavior(self.body)

        elif self.hasTouchEnded():
            self.tLastAttentionCall = self.tLastTouchF;
            self.currBehavior.finishBehavior()

            #hello is performed on the first touch
            if  not self.isInteractionStarted:
                self.currBehavior = HelloBehavior(self.body)
                self.isInteractionStarted = True

        #do nothing until first touch
        if not self.isInteractionStarted or self.isInteractionFinished:
            # constantly reinit startTime until robot starts
            self.startTime = tCurr
            return

        # autonomous stuff
        if not self.beingTouched():
            # print "attCall: "+str(tCurr - self.tLastAttentionCall)
            if (tCurr - self.tLastAttentionCall) > 30:
                self.tLastAttentionCall = time.time() #simulate touch to reset timer
                self.currBehavior = self.generateAttentionCallBehavior()
            else:
                if not self.personalityOrCreativeTriggered and tLastTouchDelta > 1:
                    self.personalityOrCreativeTriggered = True
                    if (numpy.random.random_integers(0,1) == 1):
                        # personality
                        self.currBehavior = self.generatePersonalityBehavior(numpy.random.random_integers(0, len(self.personalityProfile.personalityBehaviorList) - 1))
                    else:
                        # creativity
                        self.currBehavior = self.generateCreativityBehavior(self.currStoryArcMoment, self.currRecognizedShape)

        # idle acts as fallback
        if self.currBehavior.isOver:
            self.currBehavior = self.generateIdleBehavior()

        # check for recognized shapes
        if self.shapeWasRecognized():
            self.currRecognizedShape = self.predictShape(self.body.getOpticalSensor().getCurrentRecognizedShape())
            print self.currRecognizedShape

    def generateAttentionCallBehavior(self):
        self.personalityProfile.attentionCallBehavior.resetBehavior()
        return self.personalityProfile.attentionCallBehavior

    def generateIdleBehavior(self):
        self.personalityProfile.idleBehavior.resetBehavior()
        return  self.personalityProfile.idleBehavior

    def generatePersonalityBehavior(self, behaviorNumber):
        self.personalityProfile.personalityBehaviorList[behaviorNumber].resetBehavior()
        return self.personalityProfile.personalityBehaviorList[behaviorNumber]

    def getCreativityBehaviorFromShapeAndSpeed(self, shapeTypeName, shapeSpeed):
        switcher = {
            ShapeType.NONE.name: 
            {
                # at first when there is no shape yet, generate empty behavior...
                ShapeSpeed.SLOW : ComposedBehavior(self.body),
                ShapeSpeed.FAST : ComposedBehavior(self.body)
            }
            ,
            ShapeType.SPIKES.name: 
            {
                ShapeSpeed.SLOW : SpikesSlowBehavior(self.body),
                ShapeSpeed.FAST : SpikesFastBehavior(self.body)
            }
            ,
            ShapeType.CURVED.name: 
            {
                ShapeSpeed.SLOW : CurvedSlowBehavior(self.body),
                ShapeSpeed.FAST : CurvedFastBehavior(self.body)
            }
            ,
            ShapeType.LOOPS.name: 
            {
                ShapeSpeed.SLOW : LoopsSlowBehavior(self.body),
                ShapeSpeed.FAST : LoopsFastBehavior(self.body)
            }
            ,
            ShapeType.STRAIGHT.name: 
            {
                ShapeSpeed.SLOW : StraightSlowBehavior(self.body),
                ShapeSpeed.FAST : StraightFastBehavior(self.body)
            }
            ,
            ShapeType.RECT.name: 
            {
                ShapeSpeed.SLOW : RectSlowBehavior(self.body),
                ShapeSpeed.FAST : RectFastBehavior(self.body)
            }
        }
        return switcher.get(shapeTypeName ,"Invalid Shape Type.").get(shapeSpeed,"Invalid Shape Speed")

    def getContrastCreativityBehavior(self, shapeName, speed):
        consideredShapesNames = ['NONE','SPIKES','CURVED','LOOPS','STRAIGHT','RECT']
        consideredShapesNames.remove(shapeName)
        selectedShapeName = consideredShapesNames[numpy.random.random_integers(0, len(consideredShapesNames)-1)]
        return self.getCreativityBehaviorFromShapeAndSpeed(selectedShapeName, speed) #contrast
            
    def getMirrorCreativityBehavior(self, shapeName, speed):
        return self.getCreativityBehaviorFromShapeAndSpeed(shapeName, speed) #mirror


    def generateCreativityBehavior(self, currStoryArcMoment, recognizedShape):
        switcher = {
            StoryArc.RISING_ACTION : self.getMirrorCreativityBehavior(recognizedShape, ShapeSpeed.SLOW), #mirror
            StoryArc.CLIMAX : self.getContrastCreativityBehavior(recognizedShape, ShapeSpeed.FAST),
            StoryArc.FALLING_ACTION : self.getMirrorCreativityBehavior(recognizedShape, ShapeSpeed.SLOW) #mirror
        }
        return switcher.get(currStoryArcMoment, "Invalid current story arc moment")

    def setBehaviorProfiles(self, personalityProfile, creativityProfile):
        self.personalityProfile = personalityProfile
        self.creativityProfile = creativityProfile

    def beingTouched(self):
        return (self.body.getTouchSensor().getState() == TouchState.TOUCHING)

    def shapeWasRecognized(self):
        return (self.body.getOpticalSensor().getState() == OpticalState.FINISHED)

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
        logText = "Recognized the shape: " + SHAPE_ARRAY[int(prediction)] + "at the story arc: " + StoryArc(self.currStoryArcMoment).name
        print logText
        logging.info(logText)
        return SHAPE_ARRAY[int(prediction)]