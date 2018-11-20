import sys
import calendar
import logging
import time
import numpy
from enum import IntEnum

import traceback

from Libs.Constants import *
from Libs.MachineLearning.lib.constants import SHAPE_ARRAY
from Libs.MachineLearning.lib.util import extract_features, predict

from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseInOut import BlinkBehaviorEaseInOut
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehaviorLoops import MoveBehaviorLoops
from colour import Color



from Scripts.Behavior.ComposedBehavior.CreativeTechnique.CurvedFastBehavior import CurvedFastBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.CurvedSlowBehavior import CurvedSlowBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.LoopsFastBehavior import LoopsFastBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.LoopsSlowBehavior import LoopsSlowBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.RectFastBehavior import RectFastBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.RectSlowBehavior import RectSlowBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.SpikesFastBehavior import SpikesFastBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.SpikesSlowBehavior import SpikesSlowBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.StraightFastBehavior import StraightFastBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.StraightSlowBehavior import StraightSlowBehavior
from Behavior.ComposedBehavior.GenericBehavior.PuppeteerBehavior import PuppeteerBehavior

from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AffectivePersonality.AffectiveAttentionCallBehavior import AffectiveAttentionCallBehavior
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AffectivePersonality.AffectiveBehavior1 import AffectiveBehavior1
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AffectivePersonality.AffectiveBehavior2 import AffectiveBehavior2
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AffectivePersonality.AffectiveBehavior3 import AffectiveBehavior3
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AffectivePersonality.AffectiveIdleBehavior import AffectiveIdleBehavior

from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AloofPersonality.AloofAttentionCallBehavior import AloofAttentionCallBehavior
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AloofPersonality.AloofBehavior1 import AloofBehavior1
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AloofPersonality.AloofBehavior2 import AloofBehavior2
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AloofPersonality.AloofBehavior3 import AloofBehavior3
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AloofPersonality.AloofIdleBehavior import AloofIdleBehavior

from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.PunkPersonality.PunkAttentionCallBehavior import PunkAttentionCallBehavior
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.PunkPersonality.PunkBehavior1 import PunkBehavior1
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.PunkPersonality.PunkBehavior2 import PunkBehavior2
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.PunkPersonality.PunkBehavior3 import PunkBehavior3
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.PunkPersonality.PunkIdleBehavior import PunkIdleBehavior

from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.HelloBehavior import HelloBehavior
from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior


class Mind:
    """docstring for Mind"""

    def __init__(self, personalityType, body):
        self.personalityType = personalityType
        self.body = body

        self.currBehavior = ComposedBehavior(body)
        # self.currBehavior = MoveBehaviorLoops(self.body, 75, MovementDirection.ALTERNATING, 5, 1.5, True)

        tCurr = time.time()

        self.startTime = tCurr
        self.tLastTouchI = tCurr
        self.tLastTouchF = tCurr
        self.wasTouched = False


        self.attentionCallTriggered = False
        self.personalityOrCreativeTriggered = False

        self.currStoryArcMoment = StoryArc.NONE
        self.currRecognizedShape = ShapeType.NONE

        
        self.isFirstTimeTouch = True


        return

    def update(self):

        self.body.update()
        self.currBehavior.applyBehavior()

        tCurr = time.time()
        tSinceStart = tCurr - self.startTime
        # update curr story arc moment
        if (tSinceStart > 0 and tSinceStart <= 5*60):
            self.currStoryArcMoment = StoryArc.RISING_ACTION
        elif (tSinceStart > 5*60 and tSinceStart <= 8*60):
            self.currStoryArcMoment = StoryArc.CLIMAX
        elif (tSinceStart > 8*60 and tSinceStart <= 13*60):
            self.currStoryArcMoment = StoryArc.FALLING_ACTION


        tLastTouchDelta = self.tLastTouchF - self.tLastTouchI
        

        # pupeteer behavior stuff
        if self.hasTouchedStarted():
            print "hasTouchStarted"
            self.attentionCallTriggered = False
            self.personalityOrCreativeTriggered = False
            
            self.currBehavior.finishBehavior() # finish any pending behavior
            self.currBehavior = PuppeteerBehavior(self.body)

        elif self.hasTouchedEnded():

            print "hasTouchEnded"
            self.currBehavior.finishBehavior()

            #hello is performed on the first touch
            if  self.isFirstTimeTouch:
                self.currBehavior = HelloBehavior(self.body)
                self.isFirstTimeTouch = False

        #do nothing until first touch
        if self.isFirstTimeTouch:
            return


        # autonomous stuff
        if not self.beingTouched():
            if not self.attentionCallTriggered and (tCurr - self.tLastTouchF) > 60:
                self.attentionCallTriggered = True
                self.currBehavior = self.generateAttentionCallBehavior(self.personalityType)
            else:
                if not self.personalityOrCreativeTriggered and tLastTouchDelta > 1:
                    self.personalityOrCreativeTriggered = True
                    if (numpy.random.random_integers(0,1) > 1):
                        # personality
                        self.currBehavior = self.generatePersonalityBehavior(self.personalityType, numpy.random.random_integers(1,3))
                    else:
                        # creativity
                        self.currBehavior = self.generateCreativityBehavior(self.currStoryArcMoment, self.currRecognizedShape)

        # idle acts as fallback
        if self.currBehavior.isOver:
            self.currBehavior = self.generateIdleBehavior(self.personalityType)
            

        # check for recognized shapes
        if self.shapeWasRecognized():
            self.currRecognizedShape = self.predictShape(self.body.getOpticalSensor().getCurrentRecognizedShape())
            print self.currRecognizedShape

        return


    def generateAttentionCallBehavior(self, personalityType):
        switcher = {
            PersonalityType.AFFECTIVE : AffectiveAttentionCallBehavior(self.body),
            PersonalityType.ALOOF : AloofAttentionCallBehavior(self.body),
            PersonalityType.PUNK : PunkAttentionCallBehavior(self.body),
        }
        return switcher.get(personalityType, "Invalid Personality Name")

    def generateIdleBehavior(self, personalityType):
        switcher = {
            PersonalityType.AFFECTIVE : AffectiveIdleBehavior(self.body),
            PersonalityType.ALOOF : AloofIdleBehavior(self.body),
            PersonalityType.PUNK : PunkIdleBehavior(self.body),
        }
        return switcher.get(personalityType, "Invalid Personality Name")


    def generatePersonalityBehavior(self, personalityType, behaviorNumber):
        switcher = {
            PersonalityType.AFFECTIVE: 
            {
                1 : AffectiveBehavior1(self.body),
                2 : AffectiveBehavior2(self.body),
                3 : AffectiveBehavior3(self.body)
            }
            ,
            PersonalityType.ALOOF: 
            {
                1 : AloofBehavior1(self.body),
                2 : AloofBehavior2(self.body),
                3 : AloofBehavior3(self.body)
            }
            ,
            PersonalityType.PUNK: 
            {
                1 : PunkBehavior1(self.body),
                2 : PunkBehavior2(self.body),
                3 : PunkBehavior3(self.body)
            }
        }
        return switcher.get(personalityType ,"Invalid Personality Type.").get(behaviorNumber, "Invalid behavior number.")


    def getCreativityBehaviorFromShapeAndSpeed(self,shapeTypeName,shapeSpeed):
        switcher = {
            ShapeType.NONE.name: 
            {
                # at first when there is no shape yet...
                ShapeSpeed.SLOW : StraightSlowBehavior(self.body),
                ShapeSpeed.FAST : StraightSlowBehavior(self.body)
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
        # print switcher.get(shapeTypeName ,"Invalid Shape Type.").get(shapeSpeed,"Invalid Shape Speed")
        # print shapeSpeed

        return switcher.get(shapeTypeName ,"Invalid Shape Type.").get(shapeSpeed,"Invalid Shape Speed")


    def getContrastCreativityBehavior(self, shapeName, speed):
        # inaccessibility leads to less fine code...
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


    def beingTouched(self):
        return (self.body.getTouchSensor().getState() == TouchState.TOUCHING)

    def shapeWasRecognized(self):
        return (self.body.getOpticalSensor().getState() == OpticalState.FINISHED)


    def hasTouchedStarted(self):
        result = not self.wasTouched and self.beingTouched()
        if(result):
            self.wasTouched = True
            self.tLastTouchI = time.time()
        return result
    
    def hasTouchedEnded(self):
        result = self.wasTouched and not self.beingTouched()
        if(result):
            self.wasTouched = False
            self.tLastTouchF = time.time()
        return result

    def predictShape(self, pointDataArray):
        #print "shape recognized (length " + str(len(pointDataArray)) + "): " + str(pointDataArray)

        #print "Time feature extract start: " + time.strftime("%H:%M:%S", time.gmtime())
        features = extract_features(pointDataArray)
        prediction = predict(features)[0]
        #print "Time predict end: " + time.strftime("%H:%M:%S", time.gmtime())

        print StoryArc(self.currStoryArcMoment).name + ' arc --- Recognized a shape: ' + SHAPE_ARRAY[int(prediction)]
        logging.info(StoryArc(self.currStoryArcMoment).name + ' arc --- Recognized a shape: ' + SHAPE_ARRAY[int(prediction)])

        return SHAPE_ARRAY[int(prediction)]