import sys
import calendar
import logging
import time
import numpy

import traceback

from Libs.Constants import *
from Libs.MachineLearning.lib.constants import SHAPE_ARRAY
from Libs.MachineLearning.lib.util import extract_features, predict

from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseIn import BlinkBehaviorEaseIn
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehaviorStraight import MoveBehaviorStraight
from colour import Color



from Scripts.Behavior.ComposedBehavior.CreativeTechnique.CurvedFastBehavior import CurvedFastBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.CurvedSlowBehavior import CurvedSlowBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.LoopsFastBehavior import LoopsFastBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.LoopsSlowBehavior import LoopsSlowBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.RectFastBehavior import RectFastBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.RectSlowBehavior import RectSlowBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.SpikesFastBehavior import SpikesFastBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.SpikesSlowBehavior import SpikesSlowBehavior
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

        self.isFirstTimeTouch = True
        self.currBehavior = ComposedBehavior(body)


        tCurr = time.time()

        self.startTime = tCurr
        self.tLastTouchI = tCurr
        self.tLastTouchF = tCurr
        self.wasTouched = False


        self.attentionCallTriggered = False
        self.personalityOrCreativeTriggered = False

        self.currStoryArcMoment = StoryArc.NONE
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


        #hello behavior stuff
        tLastTouchDelta = self.tLastTouchF - self.tLastTouchI
        

        # pupeteer behavior stuff
        if self.hasTouchedStarted():
            print "hasTouchStarted"
            self.attentionCallTriggered = False
            self.personalityOrCreativeTriggered = False
            self.isFirstTimeTouch = False
            
            self.currBehavior.finishBehavior() # finish any pending behavior

            self.currBehavior = PuppeteerBehavior(self.body)

        elif self.hasTouchedEnded():
            print "hasTouchEnded"
            self.currBehavior.finishBehavior()


        # autonomous stuff
        if not self.beingTouched():

            if self.isFirstTimeTouch:
                self.currBehavior = HelloBehavior(self.body)


            if not self.attentionCallTriggered and (tCurr - self.tLastTouchF) > 60:
                self.attentionCallTriggered = True
                self.currBehavior = self.generateAttentionCallBehavior(self.personalityType)
            else:
                if not self.personalityOrCreativeTriggered and tLastTouchDelta > 2:
                    print (tLastTouchDelta)
                    self.personalityOrCreativeTriggered = True
                    if (numpy.random.random_integers(0,1) == 1):
                        # personality
                        self.currBehavior = self.generatePersonalityBehavior(self.personalityType, numpy.random.random_integers(1,3))
                    else:
                        # creativity
                        self.currBehavior = self.generateCreativityBehavior(self.currStoryArcMoment)

                

        # idle acts as fallback
        if self.currBehavior.isOver:
            self.currBehavior = self.generateIdleBehavior(self.personalityType)
            
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



    def generateCreativityBehavior(self, currStoryArcMoment):
        switcher = {
            StoryArc.RISING_ACTION : CurvedSlowBehavior(self.body),
            StoryArc.CLIMAX : CurvedFastBehavior(self.body),
            StoryArc.FALLING_ACTION : CurvedSlowBehavior(self.body),
        }
        return switcher.get(currStoryArcMoment, "Invalid current story arc moment")



    def beingTouched(self):
        return (self.body.getTouchSensorState() == TouchState.TOUCHING)

    def hasTouchedStarted(self):
        result = not self.wasTouched and self.beingTouched()
        if(result):
            self.wasTouched = True
            self.tLastTouchI = time.time()
        return result
    
    def hasTouchedEnded(self):
        if(self.isFirstTimeTouch):
            self.isFirstTimeTouch = False

        result = self.wasTouched and not self.beingTouched()
        
        if(result):
            self.wasTouched = False
            self.tLastTouchF = time.time()
        return result