from colour import Color
from Libs.Constants import *
from Mind import *
from Body import *

# auxiliary Agent API structs
class GeneralProfile (object):
    def __init__(self, name, helloBehavior, goodbyeBehavior, pupeteerBehavior, idleBehavior):
        self.name = name
        self.helloBehavior = helloBehavior
        self.goodbyeBehavior = goodbyeBehavior
        self.pupeteerBehavior = pupeteerBehavior
        self.idleBehavior = idleBehavior

class PersonalityProfile (object):
    def __init__(self, name, minimumTouchTimeInSeconds, attentionCallBehavior, attentionCallBehaviorDelayInSeconds, personalityBehaviorList):
        self.name = name
        self.minimumTouchTimeInSeconds = minimumTouchTimeInSeconds
        self.attentionCallBehavior = attentionCallBehavior
        self.attentionCallBehaviorDelayInSeconds = attentionCallBehaviorDelayInSeconds
        self.personalityBehaviorList = personalityBehaviorList

class CreativityProfile (object):
    def __init__(self, name, 
        risingActionTimeInMinutes, risingActionBehaviorDict, risingActionBehaviorType, 
        climaxTimeInMinutes, climaxBehaviorDict, climaxBehaviorType, 
        fallingActionTimeInMinutes, fallingActionBehaviorDict, fallingActionBehaviorType):
        self.name = name
        self.risingActionTimeInMinutes = risingActionTimeInMinutes
        self.risingActionBehaviorDict = risingActionBehaviorDict
        self.risingActionBehaviorType = risingActionBehaviorType
        self.climaxTimeInMinutes = climaxTimeInMinutes
        self.climaxBehaviorDict = climaxBehaviorDict
        self.climaxBehaviorType = climaxBehaviorType
        self.fallingActionTimeInMinutes = fallingActionTimeInMinutes
        self.fallingActionBehaviorDict = fallingActionBehaviorDict
        self.fallingActionBehaviorType = fallingActionBehaviorType

class Agent (object):
    def __init__(self, name):
        # init body as it is independent of the state of mind while interacting and needed to build behaviors
        self.body = Body() 

        self.defaultPersonalityProfile = PersonalityProfile("Default", 1, ComposedBehavior(self.body, []), 30.0, [])
        self.defaultCreativityProfile = CreativityProfile("Default", 5, {}, StoryArcBehaviorType.MIRROR, 5, {}, StoryArcBehaviorType.MIRROR, 5, {}, StoryArcBehaviorType.MIRROR)
        self.defaultGeneralProfile = self.generateGeneralProfile("Default", Color(rgb=(0.1 ,0.1 ,0.1)))
        
        self.name = name

    def __del__(self):
        self.body.__del__()
        self.mind = None

    def getBodyRef(self):
        return self.body
    
    def interact(self, generalProfile = None, personalityProfile = None, creativityProfile = None):
        
        if(isinstance(generalProfile,basestring)):
            generalPresetSwitcher = {
                "PUNK": self.generateGeneralProfile("PUNK", Color(rgb=(0.5,0.0,0.5))),
                "AFFECTIVE": self.generateGeneralProfile("AFFECTIVE", Color(rgb=(1.0,0.55,0.0))),
                "ALOOF": self.generateGeneralProfile("ALOOF", Color(rgb=(0.0,0.0,0.5)))
            }
            generalProfile = generalPresetSwitcher.get(generalProfile, None)
            
        if(isinstance(personalityProfile,basestring)):
            profilePresetSwitcher = {
                "PUNK": self.generatePunkProfilePreset(),
                "AFFECTIVE": self.generateAffectiveProfilePreset(),
                "ALOOF": self.generateAloofProfilePreset()
            }
            personalityProfile = profilePresetSwitcher.get(personalityProfile, None)
        
        if(isinstance(creativityProfile,basestring)):
            creativityPresetSwitcher = {
                "PUNK": self.generateDefaultCreativityProfile("PUNK", Color(rgb=(0.5,0.0,0.5))),
                "AFFECTIVE": self.generateDefaultCreativityProfile("AFFECTIVE", Color(rgb=(1.0,0.55,0.0))),
                "ALOOF": self.generateDefaultCreativityProfile("ALOOF", Color(rgb=(0.0,0.0,0.5)))
            }
            creativityProfile = creativityPresetSwitcher.get(creativityProfile, None)


        if(generalProfile == None):
            generalProfile = self.defaultGeneralProfile

        if(personalityProfile == None):
            personalityProfile = self.defaultPersonalityProfile

        if(creativityProfile == None):
            creativityProfile = self.defaultCreativityProfile
  

        # init new state of mind before interaction update
        self.mind = Mind(self.body, generalProfile, personalityProfile, creativityProfile)      
        
        try:
            while True:
                if(self.mind.isMindFinished == False):
                    self.mind.update()
                else:
                    break
        except KeyboardInterrupt:
            print "Application closed due to user input!"
            self.__del__()
        except Exception as e:
            print "Error: " + str(e)

        self.mind = None
        
    def generateGeneralProfile(self, name, idleColor):
        helloBehavior = self.generateHelloBehaviorPreset()
        goodbyeBehavior = self.generateGoodbyeBehaviorPreset()
        puppeteerBehavior = self.generatePupetteerBehaviorPreset()

        idleBehavior = ComposedBehavior(self.body, [BlinkBehaviorEaseInOut(self.body, idleColor, ColorBrightness.HIGH, 1, 2.0, Color(rgb=(0.0, 0.0, 0.0)))])

        return GeneralProfile(name, helloBehavior, goodbyeBehavior, puppeteerBehavior, idleBehavior)


    def generateHelloBehaviorPreset(self):
        helloBehavior = ComposedBehavior(self.body, [BlinkBehaviorEaseIn(self.body, Color(rgb=(1.0, 1.0, 1.0)), ColorBrightness.MEDIUM, 3, 2.0, Color(rgb=(0.0, 0.0, 0.0)))])
        return helloBehavior

    def generateGoodbyeBehaviorPreset(self):
        goodbyeBehavior = ComposedBehavior(self.body, [BlinkBehaviorEaseOut(self.body, Color(rgb=(1.0, 1.0, 1.0)), ColorBrightness.MEDIUM, 3, 2.0, Color(rgb=(0.0, 0.0, 0.0)))])
        return goodbyeBehavior

    def generatePupetteerBehaviorPreset(self):
        pupeteerBehavior = ComposedBehavior(self.body,[BlinkBehaviorInstant(self.body, Color(rgb=(1.0, 1.0, 1.0)), ColorBrightness.HIGH, 0, 1.0, Color(rgb=(0.0, 0.0, 0.0)))])
        return pupeteerBehavior

    def generatePunkProfilePreset(self):
        behaviorList = []
        behaviorList.append(BlinkBehaviorEaseInOut(self.body, Color(rgb=(1.0, 0.0, 0.0)), ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
        behaviorList.append(MoveBehaviorSpikes(self.body, 90, MovementDirection.ALTERNATING, 2, 1.5))
        attentionCallBehavior = ComposedBehavior(self.body, behaviorList)

        behaviorList = []
        behaviorList.append(BlinkBehaviorEaseInOut(self.body, Color(rgb=(1.0, 0.0, 0.0)), ColorBrightness.HIGH, 1, 4.5, Color(rgb=(0.0, 0.0, 0.0))))
        behaviorList.append(MoveBehaviorSpikes(self.body, 80, MovementDirection.FORWARD, 3, 1.5))
        personalityBehavior1 = ComposedBehavior(self.body, behaviorList)

        behaviorList = []
        behaviorList.append(BlinkBehaviorEaseInOut(self.body, Color(rgb=(1.0, 0.0, 0.0)), ColorBrightness.HIGH, 1, 4.5, Color(rgb=(0.0, 0.0, 0.0))))
        behaviorList.append(MoveBehaviorLoops(self.body, 80, MovementDirection.FORWARD, 3, 1.5))
        personalityBehavior2 = ComposedBehavior(self.body, behaviorList)

        behaviorList = []
        behaviorList.append(BlinkBehaviorInstant(self.body, Color(rgb=(1.0, 0.0, 0.0)), ColorBrightness.HIGH, 1, 2.5, Color(rgb=(0.0, 0.0, 0.0))))
        personalityBehavior3 = ComposedBehavior(self.body, behaviorList)

        personalityBehaviorList = []
        personalityBehaviorList.append(personalityBehavior1)
        personalityBehaviorList.append(personalityBehavior2)
        personalityBehaviorList.append(personalityBehavior3)

        
        return PersonalityProfile("PUNK", 1.0, attentionCallBehavior, 30.0, personalityBehaviorList)

    def generateAffectiveProfilePreset(self):
        behaviorList = []
        behaviorList.append(BlinkBehaviorEaseIn(self.body, Color(rgb=(1.0, 0.25, 0.0)), ColorBrightness.MEDIUM, 1.0, 1.0, Color(rgb=(0.0, 0.0, 0.0))))
        behaviorList.append(MoveBehaviorCircle(self.body, 40.0, MovementDirection.FORWARD, 3.0, 5.0))
        attentionCallBehavior = ComposedBehavior(self.body, behaviorList)

        behaviorList = []
        behaviorList.append(BlinkBehaviorEaseIn(self.body, Color(rgb=(1.0, 0.25, 0.0)), ColorBrightness.MEDIUM, 1, 1.0, Color(rgb=(0.0, 0.0, 0.0))))
        behaviorList.append(MoveBehaviorCurved(self.body, 40.0, MovementDirection.FORWARD, 2, 6.0))
        personalityBehavior1 = ComposedBehavior(self.body, behaviorList)

        behaviorList = []
        behaviorList.append(BlinkBehaviorEaseIn(self.body, Color(rgb=(1.0, 0.25, 0.0)), ColorBrightness.MEDIUM, 1, 1.0, Color(rgb=(0.0, 0.0, 0.0))))
        behaviorList.append(MoveBehaviorRect(self.body, 50.0, MovementDirection.FORWARD, 2, 6.0))
        personalityBehavior2 = ComposedBehavior(self.body, behaviorList)

        personalityBehavior3 = ComposedBehavior(self.body, [BlinkBehaviorEaseIn(self.body, Color(rgb=(1.0, 0.25, 0.0)), ColorBrightness.MEDIUM, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)))])

        personalityBehaviorList = []
        personalityBehaviorList.append(personalityBehavior1)
        personalityBehaviorList.append(personalityBehavior2)
        personalityBehaviorList.append(personalityBehavior3)

        helloBehavior = self.generateHelloBehaviorPreset()
        goodbyeBehavior = self.generateGoodbyeBehaviorPreset()
        puppeteerBehavior = self.generatePupetteerBehaviorPreset()

        return PersonalityProfile("AFFECTIVE", 1.0, attentionCallBehavior, 30.0, personalityBehaviorList)

    def generateAloofProfilePreset(self):
        attentionCallBehavior = ComposedBehavior(self.body, [])

        behaviorList = []
        behaviorList.append(BlinkBehaviorEaseInOut(self.body, Color(rgb=(0.0, 1.0, 0.0)), ColorBrightness.LOW, 1, 5.0, Color(rgb=(0.0, 0.0, 0.0))))
        behaviorList.append(MoveBehaviorStraight(self.body, 20.0, MovementDirection.FORWARD, 1, 5.0))
        personalityBehavior1 = ComposedBehavior(self.body, behaviorList)

        behaviorList = []
        behaviorList.append(BlinkBehaviorEaseInOut(self.body, Color(rgb=(0.0, 0.0, 0.1)), ColorBrightness.LOW, 1, 5.0, Color(rgb=(0.0, 0.0, 0.0))))
        behaviorList.append(MoveBehaviorStraight(self.body, 20.0, MovementDirection.REVERSE, 1, 5.0))
        personalityBehavior2 = ComposedBehavior(self.body, behaviorList)

        personalityBehavior3 = ComposedBehavior(self.body, [BlinkBehaviorEaseInOut(self.body, Color(rgb=(0.0, 0.0, 0.1)), ColorBrightness.LOW, 1, 8.0, Color(rgb=(0.0, 0.0, 0.0)))])

        personalityBehaviorList = []
        personalityBehaviorList.append(personalityBehavior1)
        personalityBehaviorList.append(personalityBehavior2)
        personalityBehaviorList.append(personalityBehavior3)

        helloBehavior = self.generateHelloBehaviorPreset()
        goodbyeBehavior = self.generateGoodbyeBehaviorPreset()
        puppeteerBehavior = self.generatePupetteerBehaviorPreset()

        return PersonalityProfile("ALOOF", 1.0, attentionCallBehavior, 30.0, personalityBehaviorList)


    def generateDefaultCreativityProfile(self, name, bodyColor):
        creativitySlowBehaviorDict = {}
        creativityFastBehaviorDict = {}

        behaviorList = []
        behaviorList.append(MoveBehaviorCurved(self.body, 95, MovementDirection.FORWARD, 2, 1.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.body, bodyColor, ColorBrightness.HIGH, 1, 1.0, Color(rgb=(0.0, 0.0, 0.0))))
        curvedFastBehavior = ComposedBehavior(self.body, behaviorList)
        creativityFastBehaviorDict[ShapeType.CURVED] = curvedFastBehavior

        behaviorList = []
        behaviorList.append(MoveBehaviorCurved(self.body, 30, MovementDirection.FORWARD, 2, 3.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.body, bodyColor, ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
        curvedSlowBehavior = ComposedBehavior(self.body, behaviorList)
        creativitySlowBehaviorDict[ShapeType.CURVED] = curvedSlowBehavior


        behaviorList = []
        behaviorList.append(MoveBehaviorLoops(self.body, 95, MovementDirection.FORWARD, 2, 1.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.body, bodyColor, ColorBrightness.HIGH, 1, 1.0, Color(rgb=(0.0, 0.0, 0.0))))
        loopsFastBehavior = ComposedBehavior(self.body, behaviorList)
        creativityFastBehaviorDict[ShapeType.LOOPS] = loopsFastBehavior


        behaviorList = []
        behaviorList.append(MoveBehaviorLoops(self.body, 30, MovementDirection.FORWARD, 2, 3.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.body, bodyColor, ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
        loopsSlowBehavior = ComposedBehavior(self.body, behaviorList)
        creativitySlowBehaviorDict[ShapeType.LOOPS] = loopsSlowBehavior

        behaviorList = []
        behaviorList.append(MoveBehaviorRect(self.body, 95, MovementDirection.FORWARD, 2, 1.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.body, bodyColor, ColorBrightness.HIGH, 1, 1.0, Color(rgb=(0.0, 0.0, 0.0))))
        rectFastBehavior = ComposedBehavior(self.body, behaviorList)
        creativityFastBehaviorDict[ShapeType.RECT] = rectFastBehavior

        behaviorList = []
        behaviorList.append(MoveBehaviorRect(self.body, 30, MovementDirection.FORWARD, 2, 3.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.body, bodyColor, ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
        rectSlowBehavior = ComposedBehavior(self.body, behaviorList)
        creativitySlowBehaviorDict[ShapeType.RECT] = rectSlowBehavior

        behaviorList = []
        behaviorList.append(MoveBehaviorSpikes(self.body, 95, MovementDirection.FORWARD, 2, 1.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.body, bodyColor, ColorBrightness.HIGH, 1, 1.0, Color(rgb=(0.0, 0.0, 0.0))))
        spikesFastBehavior = ComposedBehavior(self.body, behaviorList)
        creativityFastBehaviorDict[ShapeType.SPIKES] = spikesFastBehavior

        behaviorList = []
        behaviorList.append(MoveBehaviorSpikes(self.body, 30, MovementDirection.FORWARD, 2, 3.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.body, bodyColor, ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
        spikesSlowBehavior = ComposedBehavior(self.body, behaviorList)
        creativitySlowBehaviorDict[ShapeType.SPIKES] = spikesSlowBehavior

        behaviorList = []
        behaviorList.append(MoveBehaviorStraight(self.body, 95, MovementDirection.FORWARD, 2, 1.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.body, bodyColor, ColorBrightness.HIGH, 1, 1.0, Color(rgb=(0.0, 0.0, 0.0))))
        straightFastBehavior = ComposedBehavior(self.body, behaviorList)
        creativityFastBehaviorDict[ShapeType.STRAIGHT] = straightFastBehavior

        behaviorList = []
        behaviorList.append(MoveBehaviorStraight(self.body, 30, MovementDirection.FORWARD, 2, 1.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.body, bodyColor, ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
        straightSlowBehavior = ComposedBehavior(self.body, behaviorList)
        creativitySlowBehaviorDict[ShapeType.STRAIGHT] = straightSlowBehavior

        return CreativityProfile(name, 
            5.0, creativitySlowBehaviorDict, StoryArcBehaviorType.MIRROR, 
            3.0, creativityFastBehaviorDict, StoryArcBehaviorType.CONTRAST, 
            5.0, creativitySlowBehaviorDict, StoryArcBehaviorType.MIRROR)