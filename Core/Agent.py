from colour import Color
from Core.Enumerations import *
from Planning import *
from Control import *

# auxiliary Agent API structs
class GeneralProfile (object):
    def __init__(self, name, helloBehavior, goodbyeBehavior, pupeteerBehavior, idleBehavior, minimumTouchTimeInSeconds):
        self.name = name
        self.helloBehavior = helloBehavior
        self.goodbyeBehavior = goodbyeBehavior
        self.pupeteerBehavior = pupeteerBehavior
        self.idleBehavior = idleBehavior
        self.minimumTouchTimeInSeconds = minimumTouchTimeInSeconds

class SocialProfile (object):
    def __init__(self, name, attentionCallBehavior, attentionCallBehaviorDelayInSeconds, socialBehaviorList):
        self.name = name
        self.attentionCallBehavior = attentionCallBehavior
        self.attentionCallBehaviorDelayInSeconds = attentionCallBehaviorDelayInSeconds
        self.socialBehaviorList = socialBehaviorList

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
        self.name = name

        # init control as it is independent of the state of planning while interacting and needed to build behaviors
        self.control = Control() 
        self.planning = None

        self.defaultSocialProfile = SocialProfile("Default", ComposedBehavior(self.control, []), 30.0, [])
        self.defaultCreativityProfile = CreativityProfile("Default", 5, {}, StoryArcBehaviorType.MIRROR, 5.0, {}, StoryArcBehaviorType.MIRROR, 5.0, {}, StoryArcBehaviorType.MIRROR)
        self.defaultGeneralProfile = self.generateGeneralProfile("Default", Color(rgb=(0.1 ,0.1 ,0.1)), 1.0)
        

    def getControlRef(self):
        return self.control
    
    def interact(self, generalProfile = None, socialProfile = None, creativityProfile = None):
        
        if(isinstance(generalProfile,basestring)):
            generalPresetSwitcher = {
                "EXUBERANT": self.generateGeneralProfile("EXUBERANT", Color(rgb=(0.5,0.0,0.5)), 1.0),
                "HARMONIOUS": self.generateGeneralProfile("HARMONIOUS", Color(rgb=(1.0,0.55,0.0)), 1.0),
                "ALOOF": self.generateGeneralProfile("ALOOF", Color(rgb=(0.0,0.0,0.5)), 1.0),
                "NEUTRAL": self.generateGeneralProfile("NEUTRAL", Color(rgb=(1.0,1.0,1.0)), 1.0)
            }
            generalProfile = generalPresetSwitcher.get(generalProfile, None)
            
        if(isinstance(socialProfile,basestring)):
            profilePresetSwitcher = {
                "EXUBERANT": self.generateEXUBERANTProfilePreset(),
                "HARMONIOUS": self.generateHARMONIOUSProfilePreset(),
                "ALOOF": self.generateAloofProfilePreset()
            }
            socialProfile = profilePresetSwitcher.get(socialProfile, None)
        
        if(isinstance(creativityProfile,basestring)):
            creativityPresetSwitcher = {
                "EXUBERANT": self.generateDefaultCreativityProfile("EXUBERANT", Color(rgb=(0.5,0.0,0.5))),
                "HARMONIOUS": self.generateDefaultCreativityProfile("HARMONIOUS", Color(rgb=(1.0,0.55,0.0))),
                "ALOOF": self.generateDefaultCreativityProfile("ALOOF", Color(rgb=(0.0,0.0,0.5))),
                "NEUTRAL": self.generateDefaultCreativityProfile("NEUTRAL", Color(rgb=(1.0,1.0,1.0)))
            }
            creativityProfile = creativityPresetSwitcher.get(creativityProfile, None)


        if(generalProfile == None):
            generalProfile = self.defaultGeneralProfile

        if(socialProfile == None):
            socialProfile = self.defaultSocialProfile

        if(creativityProfile == None):
            creativityProfile = self.defaultCreativityProfile
  

        # init new state of planning before interaction update
        self.planning = Planning(self.control, generalProfile, socialProfile, creativityProfile)      
        
        try:
            while True:
                if(self.planning.isPlanningFinished == False):
                    self.planning.update()
                else:
                    break
        except KeyboardInterrupt:
            print "Current Interaction finnished due to user input!"
        except Exception as e:
            print "Error: " + str(e)

        self.control.setColor(Color(rgb=(0.0,0.0,0.0)))
        self.planning = None
        
    def generateGeneralProfile(self, name, idleColor, minimumTouchTimeInSeconds):
        helloBehavior = self.generateHelloBehaviorPreset()
        goodbyeBehavior = self.generateGoodbyeBehaviorPreset()
        puppeteerBehavior = self.generatePupetteerBehaviorPreset()

        idleBehavior = ComposedBehavior(self.control, [BlinkBehaviorEaseInOut(self.control, idleColor, ColorBrightness.HIGH, 1, 2.0, Color(rgb=(0.0, 0.0, 0.0)))])

        return GeneralProfile(name, helloBehavior, goodbyeBehavior, puppeteerBehavior, idleBehavior, minimumTouchTimeInSeconds)


    def generateHelloBehaviorPreset(self):
        helloBehavior = ComposedBehavior(self.control, [BlinkBehaviorEaseIn(self.control, Color(rgb=(1.0, 1.0, 1.0)), ColorBrightness.MEDIUM, 3, 2.0, Color(rgb=(0.0, 0.0, 0.0)))])
        return helloBehavior

    def generateGoodbyeBehaviorPreset(self):
        goodbyeBehavior = ComposedBehavior(self.control, [BlinkBehaviorEaseOut(self.control, Color(rgb=(1.0, 1.0, 1.0)), ColorBrightness.MEDIUM, 3, 2.0, Color(rgb=(0.0, 0.0, 0.0)))])
        return goodbyeBehavior

    def generatePupetteerBehaviorPreset(self):
        pupeteerBehavior = ComposedBehavior(self.control,[BlinkBehaviorInstant(self.control, Color(rgb=(1.0, 1.0, 1.0)), ColorBrightness.HIGH, 0, 1.0, Color(rgb=(0.0, 0.0, 0.0)))])
        return pupeteerBehavior

    def generateEXUBERANTProfilePreset(self):
        behaviorList = []
        behaviorList.append(BlinkBehaviorEaseInOut(self.control, Color(rgb=(1.0, 0.0, 0.0)), ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
        behaviorList.append(MoveBehaviorSpikes(self.control, 90, MovementDirection.ALTERNATING, 2, 1.5))
        attentionCallBehavior = ComposedBehavior(self.control, behaviorList)

        behaviorList = []
        behaviorList.append(BlinkBehaviorEaseInOut(self.control, Color(rgb=(1.0, 0.0, 0.0)), ColorBrightness.HIGH, 1, 4.5, Color(rgb=(0.0, 0.0, 0.0))))
        behaviorList.append(MoveBehaviorSpikes(self.control, 80, MovementDirection.FORWARD, 3, 1.5))
        socialBehavior1 = ComposedBehavior(self.control, behaviorList)

        behaviorList = []
        behaviorList.append(BlinkBehaviorEaseInOut(self.control, Color(rgb=(1.0, 0.0, 0.0)), ColorBrightness.HIGH, 1, 4.5, Color(rgb=(0.0, 0.0, 0.0))))
        behaviorList.append(MoveBehaviorLoops(self.control, 80, MovementDirection.FORWARD, 3, 1.5))
        socialBehavior2 = ComposedBehavior(self.control, behaviorList)

        behaviorList = []
        behaviorList.append(BlinkBehaviorInstant(self.control, Color(rgb=(1.0, 0.0, 0.0)), ColorBrightness.HIGH, 1, 2.5, Color(rgb=(0.0, 0.0, 0.0))))
        socialBehavior3 = ComposedBehavior(self.control, behaviorList)

        socialBehaviorList = []
        socialBehaviorList.append(socialBehavior1)
        socialBehaviorList.append(socialBehavior2)
        socialBehaviorList.append(socialBehavior3)

        
        return SocialProfile("EXUBERANT", attentionCallBehavior, 30.0, socialBehaviorList)

    def generateHARMONIOUSProfilePreset(self):
        behaviorList = []
        behaviorList.append(BlinkBehaviorEaseIn(self.control, Color(rgb=(1.0, 0.25, 0.0)), ColorBrightness.MEDIUM, 1.0, 1.0, Color(rgb=(0.0, 0.0, 0.0))))
        behaviorList.append(MoveBehaviorCircle(self.control, 40.0, MovementDirection.FORWARD, 3.0, 5.0))
        attentionCallBehavior = ComposedBehavior(self.control, behaviorList)

        behaviorList = []
        behaviorList.append(BlinkBehaviorEaseIn(self.control, Color(rgb=(1.0, 0.25, 0.0)), ColorBrightness.MEDIUM, 1, 1.0, Color(rgb=(0.0, 0.0, 0.0))))
        behaviorList.append(MoveBehaviorCurved(self.control, 40.0, MovementDirection.FORWARD, 2, 6.0))
        socialBehavior1 = ComposedBehavior(self.control, behaviorList)

        behaviorList = []
        behaviorList.append(BlinkBehaviorEaseIn(self.control, Color(rgb=(1.0, 0.25, 0.0)), ColorBrightness.MEDIUM, 1, 1.0, Color(rgb=(0.0, 0.0, 0.0))))
        behaviorList.append(MoveBehaviorRect(self.control, 50.0, MovementDirection.FORWARD, 2, 6.0))
        socialBehavior2 = ComposedBehavior(self.control, behaviorList)

        socialBehavior3 = ComposedBehavior(self.control, [BlinkBehaviorEaseIn(self.control, Color(rgb=(1.0, 0.25, 0.0)), ColorBrightness.MEDIUM, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)))])

        socialBehaviorList = []
        socialBehaviorList.append(socialBehavior1)
        socialBehaviorList.append(socialBehavior2)
        socialBehaviorList.append(socialBehavior3)

        helloBehavior = self.generateHelloBehaviorPreset()
        goodbyeBehavior = self.generateGoodbyeBehaviorPreset()
        puppeteerBehavior = self.generatePupetteerBehaviorPreset()

        return SocialProfile("HARMONIOUS", attentionCallBehavior, 30.0, socialBehaviorList)

    def generateAloofProfilePreset(self):
        attentionCallBehavior = ComposedBehavior(self.control, [])

        behaviorList = []
        behaviorList.append(BlinkBehaviorEaseInOut(self.control, Color(rgb=(0.0, 1.0, 0.0)), ColorBrightness.LOW, 1, 5.0, Color(rgb=(0.0, 0.0, 0.0))))
        behaviorList.append(MoveBehaviorStraight(self.control, 20.0, MovementDirection.FORWARD, 1, 5.0))
        socialBehavior1 = ComposedBehavior(self.control, behaviorList)

        behaviorList = []
        behaviorList.append(BlinkBehaviorEaseInOut(self.control, Color(rgb=(0.0, 0.0, 0.1)), ColorBrightness.LOW, 1, 5.0, Color(rgb=(0.0, 0.0, 0.0))))
        behaviorList.append(MoveBehaviorStraight(self.control, 20.0, MovementDirection.REVERSE, 1, 5.0))
        socialBehavior2 = ComposedBehavior(self.control, behaviorList)

        socialBehavior3 = ComposedBehavior(self.control, [BlinkBehaviorEaseInOut(self.control, Color(rgb=(0.0, 0.0, 0.1)), ColorBrightness.LOW, 1, 8.0, Color(rgb=(0.0, 0.0, 0.0)))])

        socialBehaviorList = []
        socialBehaviorList.append(socialBehavior1)
        socialBehaviorList.append(socialBehavior2)
        socialBehaviorList.append(socialBehavior3)

        helloBehavior = self.generateHelloBehaviorPreset()
        goodbyeBehavior = self.generateGoodbyeBehaviorPreset()
        puppeteerBehavior = self.generatePupetteerBehaviorPreset()

        return SocialProfile("ALOOF", attentionCallBehavior, 30.0, socialBehaviorList)


    def generateDefaultCreativityProfile(self, name, controlColor):
        creativitySlowBehaviorDict = {}
        creativityFastBehaviorDict = {}

        behaviorList = []
        behaviorList.append(MoveBehaviorCurved(self.control, 95, MovementDirection.FORWARD, 2, 1.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.control, controlColor, ColorBrightness.HIGH, 1, 1.0, Color(rgb=(0.0, 0.0, 0.0))))
        curvedFastBehavior = ComposedBehavior(self.control, behaviorList)
        creativityFastBehaviorDict[ShapeType.CURVED] = curvedFastBehavior

        behaviorList = []
        behaviorList.append(MoveBehaviorCurved(self.control, 30, MovementDirection.FORWARD, 2, 3.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.control, controlColor, ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
        curvedSlowBehavior = ComposedBehavior(self.control, behaviorList)
        creativitySlowBehaviorDict[ShapeType.CURVED] = curvedSlowBehavior


        behaviorList = []
        behaviorList.append(MoveBehaviorLoops(self.control, 95, MovementDirection.FORWARD, 2, 1.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.control, controlColor, ColorBrightness.HIGH, 1, 1.0, Color(rgb=(0.0, 0.0, 0.0))))
        loopsFastBehavior = ComposedBehavior(self.control, behaviorList)
        creativityFastBehaviorDict[ShapeType.LOOPS] = loopsFastBehavior


        behaviorList = []
        behaviorList.append(MoveBehaviorLoops(self.control, 30, MovementDirection.FORWARD, 2, 3.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.control, controlColor, ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
        loopsSlowBehavior = ComposedBehavior(self.control, behaviorList)
        creativitySlowBehaviorDict[ShapeType.LOOPS] = loopsSlowBehavior

        behaviorList = []
        behaviorList.append(MoveBehaviorRect(self.control, 95, MovementDirection.FORWARD, 2, 1.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.control, controlColor, ColorBrightness.HIGH, 1, 1.0, Color(rgb=(0.0, 0.0, 0.0))))
        rectFastBehavior = ComposedBehavior(self.control, behaviorList)
        creativityFastBehaviorDict[ShapeType.RECT] = rectFastBehavior

        behaviorList = []
        behaviorList.append(MoveBehaviorRect(self.control, 30, MovementDirection.FORWARD, 2, 3.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.control, controlColor, ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
        rectSlowBehavior = ComposedBehavior(self.control, behaviorList)
        creativitySlowBehaviorDict[ShapeType.RECT] = rectSlowBehavior

        behaviorList = []
        behaviorList.append(MoveBehaviorSpikes(self.control, 95, MovementDirection.FORWARD, 2, 1.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.control, controlColor, ColorBrightness.HIGH, 1, 1.0, Color(rgb=(0.0, 0.0, 0.0))))
        spikesFastBehavior = ComposedBehavior(self.control, behaviorList)
        creativityFastBehaviorDict[ShapeType.SPIKES] = spikesFastBehavior

        behaviorList = []
        behaviorList.append(MoveBehaviorSpikes(self.control, 30, MovementDirection.FORWARD, 2, 3.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.control, controlColor, ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
        spikesSlowBehavior = ComposedBehavior(self.control, behaviorList)
        creativitySlowBehaviorDict[ShapeType.SPIKES] = spikesSlowBehavior

        behaviorList = []
        behaviorList.append(MoveBehaviorStraight(self.control, 95, MovementDirection.FORWARD, 2, 1.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.control, controlColor, ColorBrightness.HIGH, 1, 1.0, Color(rgb=(0.0, 0.0, 0.0))))
        straightFastBehavior = ComposedBehavior(self.control, behaviorList)
        creativityFastBehaviorDict[ShapeType.STRAIGHT] = straightFastBehavior

        behaviorList = []
        behaviorList.append(MoveBehaviorStraight(self.control, 30, MovementDirection.FORWARD, 2, 1.5))
        behaviorList.append(BlinkBehaviorEaseInOut(self.control, controlColor, ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
        straightSlowBehavior = ComposedBehavior(self.control, behaviorList)
        creativitySlowBehaviorDict[ShapeType.STRAIGHT] = straightSlowBehavior

        return CreativityProfile(name, 
            2.0, creativitySlowBehaviorDict, StoryArcBehaviorType.MIRROR, 
            5.0, creativityFastBehaviorDict, StoryArcBehaviorType.CONTRAST, 
            2.0, creativitySlowBehaviorDict, StoryArcBehaviorType.MIRROR)