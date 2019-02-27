from colour import Color
from Libs.Constants import *
from Mind import *
from Body import *

class PersonalityProfile:
    def __init__(self, name, attentionCallBehavior, idleBehavior, personalityBehaviorList):
        self.name = name
        self.attentionCallBehavior = attentionCallBehavior
        self.idleBehavior = idleBehavior
        self.personalityBehaviorList = personalityBehaviorList

class CreativityProfile:
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

class Agent:
    def __init__(self, name):
        self.body = Body()

        self.defaultPersonalityProfile = PersonalityProfile("", ComposedBehavior(self.body), ComposedBehavior(self.body), []);
        self.defaultCreativityProfile = CreativityProfile("", 5, {}, StoryArcBehaviorType.MIRROR, 5, {}, StoryArcBehaviorType.MIRROR, 5, {}, StoryArcBehaviorType.MIRROR);
        
        self.mind = Mind(self.body, self.defaultPersonalityProfile, self.defaultCreativityProfile)
        self.name = name

    def __del__(self):
        self.body.__del__()
        self.mind = None

    def getBodyRef(self):
        return self.body
    
    def interact(self, personalityProfile = None, creativityProfile = None):
        if(isinstance(personalityProfile,basestring)):
            profilePresetSwitcher = {
                "PUNK": self.generatePunkProfilePreset(),
                "AFFECTIVE": self.generateAffectiveProfilePreset(),
                "ALOOF": self.generateAloofProfilePreset()
            }
            personalityProfile = profilePresetSwitcher.get(personalityProfile, None)
        
        if(isinstance(creativityProfile,basestring)):
            creativityPresetSwitcher = {
                "PUNK": self.generateDefaultCreativityProfile(Color(rgb=(0.5,0.0,0.5))),
                "AFFECTIVE": self.generateDefaultCreativityProfile(Color(rgb=(1.0,0.55,0.0))),
                "ALOOF": self.generateDefaultCreativityProfile(Color(rgb=(0.0,0.0,0.5)))
            }
            creativityProfile = creativityPresetSwitcher.get(creativityProfile, None)

        if(personalityProfile == None):
            personalityProfile = self.defaultPersonalityProfile

        if(creativityProfile == None):
            creativityProfile = self.defaultCreativityProfile
        
        self.mind.setBehaviorProfiles(personalityProfile, creativityProfile)
        try:
            while True:
                if(self.mind.isInteractionFinished == False):
                    self.mind.update()
        except KeyboardInterrupt:
            print "Application closed due to user input!"
        except Exception as e:
            print "Error: " + str(e)
        finally:
            self.__del__()
        

    def generatePunkProfilePreset(self):
        attentionCallBehavior = ComposedBehavior(self.body)
        attentionCallBehavior.behaviorList.append(BlinkBehaviorEaseInOut(self.body, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
        attentionCallBehavior.behaviorList.append(MoveBehaviorSpikes(self.body, 90, MovementDirection.ALTERNATING, 2, 1.5, False))

        idleBehavior = ComposedBehavior(self.body)
        idleBehavior.behaviorList.append(BlinkBehaviorEaseInOut(self.body, [Color(rgb=(0.5,0.0,0.5))], ColorBrightness.HIGH, 1, 2.0, Color(rgb=(0.0, 0.0, 0.0)), False))

        personalityBehavior1 = ComposedBehavior(self.body)
        personalityBehavior1.behaviorList.append(BlinkBehaviorEaseInOut(self.body, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 4.5, Color(rgb=(0.0, 0.0, 0.0)), False))
        personalityBehavior1.behaviorList.append(MoveBehaviorSpikes(self.body, 80, MovementDirection.FORWARD, 3, 1.5, False))

        personalityBehavior2 = ComposedBehavior(self.body)
        personalityBehavior2.behaviorList.append(BlinkBehaviorEaseInOut(self.body, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 4.5, Color(rgb=(0.0, 0.0, 0.0)), False))
        personalityBehavior2.behaviorList.append(MoveBehaviorLoops(self.body, 80, MovementDirection.FORWARD, 3, 1.5, False))

        personalityBehavior3 = ComposedBehavior(self.body)
        personalityBehavior3.behaviorList.append(BlinkBehaviorInstant(self.body, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 2.5, Color(rgb=(0.0, 0.0, 0.0)), False))

        personalityBehaviorList = []
        personalityBehaviorList.append(personalityBehavior1)
        personalityBehaviorList.append(personalityBehavior2)
        personalityBehaviorList.append(personalityBehavior3)

        return PersonalityProfile("Punk", attentionCallBehavior, idleBehavior, personalityBehaviorList)

    def generateAffectiveProfilePreset(self):
        attentionCallBehavior = ComposedBehavior(self.body)
        attentionCallBehavior.behaviorList.append(BlinkBehaviorEaseIn(self.body, [Color(rgb=(1.0, 0.25, 0.0))], ColorBrightness.MEDIUM, 1.0, 1.0, Color(rgb=(0.0, 0.0, 0.0)), True))
        attentionCallBehavior.behaviorList.append(MoveBehaviorCircle(self.body, 40.0, MovementDirection.FORWARD, 3.0, 5.0, True))

        idleBehavior = ComposedBehavior(self.body)
        idleBehavior.behaviorList.append(BlinkBehaviorEaseInOut(self.body, [Color(rgb=(1.0,0.55,0.0))], ColorBrightness.MEDIUM, 1, 2.0, Color(rgb=(0.0, 0.0, 0.0)), False))

        personalityBehavior1 = ComposedBehavior(self.body)
        personalityBehavior1.behaviorList.append(BlinkBehaviorEaseIn(self.body, [Color(rgb=(1.0, 0.25, 0.0))], ColorBrightness.MEDIUM, 1, 1.0, Color(rgb=(0.0, 0.0, 0.0)), False))
        personalityBehavior1.behaviorList.append(MoveBehaviorCurved(self.body, 40.0, MovementDirection.FORWARD, 2, 6.0, False))

        personalityBehavior2 = ComposedBehavior(self.body)
        personalityBehavior2.behaviorList.append(BlinkBehaviorEaseIn(self.body, [Color(rgb=(1.0, 0.25, 0.0))], ColorBrightness.MEDIUM, 1, 1.0, Color(rgb=(0.0, 0.0, 0.0)), False))
        personalityBehavior2.behaviorList.append(MoveBehaviorRect(self.body, 50.0, MovementDirection.FORWARD, 2, 6.0, False))

        personalityBehavior3 = ComposedBehavior(self.body)
        personalityBehavior3.behaviorList.append(BlinkBehaviorEaseIn(self.body, [Color(rgb=(1.0, 0.25, 0.0))], ColorBrightness.MEDIUM, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))

        personalityBehaviorList = []
        personalityBehaviorList.append(personalityBehavior1)
        personalityBehaviorList.append(personalityBehavior2)
        personalityBehaviorList.append(personalityBehavior3)

        return PersonalityProfile("Affective", attentionCallBehavior, idleBehavior, personalityBehaviorList)

    def generateAloofProfilePreset(self):
        attentionCallBehavior = ComposedBehavior(self.body)

        idleBehavior = ComposedBehavior(self.body)
        idleBehavior.behaviorList.append(BlinkBehaviorEaseInOut(self.body, [Color(rgb=(0.0,0.0,0.5))], ColorBrightness.LOW, 1, 7.0, self.body.getColor(), False))

        personalityBehavior1 = ComposedBehavior(self.body)
        personalityBehavior1.behaviorList.append(BlinkBehaviorEaseInOut(self.body, [Color(rgb=(0.0, 1.0, 0.0))], ColorBrightness.LOW, 1, 5.0, Color(rgb=(0.0, 0.0, 0.0)), False))
        personalityBehavior1.behaviorList.append(MoveBehaviorStraight(self.body, 20.0, MovementDirection.FORWARD, 1, 5.0, False))

        personalityBehavior2 = ComposedBehavior(self.body)
        personalityBehavior2.behaviorList.append(BlinkBehaviorEaseInOut(self.body, [Color(rgb=(0.0, 0.0, 0.1))], ColorBrightness.LOW, 1, 5.0, Color(rgb=(0.0, 0.0, 0.0)), False))
        personalityBehavior2.behaviorList.append(MoveBehaviorStraight(self.body, 20.0, MovementDirection.REVERSE, 1, 5.0, False))

        personalityBehavior3 = ComposedBehavior(self.body)
        personalityBehavior3.behaviorList.append(BlinkBehaviorEaseInOut(self.body, [Color(rgb=(0.0, 0.0, 0.1))], ColorBrightness.LOW, 1, 8.0, Color(rgb=(0.0, 0.0, 0.0)), False))

        personalityBehaviorList = []
        personalityBehaviorList.append(personalityBehavior1)
        personalityBehaviorList.append(personalityBehavior2)
        personalityBehaviorList.append(personalityBehavior3)

        return PersonalityProfile("Aloof", attentionCallBehavior, idleBehavior, personalityBehaviorList)


    def generateDefaultCreativityProfile(self, bodyColor):
        creativitySlowBehaviorDict = {}
        creativityFastBehaviorDict = {}

        curvedFastBehavior = ComposedBehavior(self.body)
        curvedFastBehavior.behaviorList.append(MoveBehaviorCurved(self.body, 95, MovementDirection.FORWARD, 2, 1.5, True))
        curvedFastBehavior.behaviorList.append(BlinkBehaviorEaseInOut(self.body, [bodyColor], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
        creativityFastBehaviorDict[ShapeType.CURVED] = curvedFastBehavior

        curvedSlowBehavior = ComposedBehavior(self.body)
        curvedSlowBehavior.behaviorList.append(MoveBehaviorCurved(self.body, 30, MovementDirection.FORWARD, 2, 3.5, True))
        curvedSlowBehavior.behaviorList.append(BlinkBehaviorEaseInOut(self.body, [bodyColor], ColorBrightness.HIGH, 1, 7.0, Color(rgb=(0.0, 0.0, 0.0)), False))
        creativitySlowBehaviorDict[ShapeType.CURVED] = curvedSlowBehavior

        loopsFastBehavior = ComposedBehavior(self.body)
        loopsFastBehavior.behaviorList.append(MoveBehaviorLoops(self.body, 95, MovementDirection.FORWARD, 2, 1.5, True))
        loopsFastBehavior.behaviorList.append(BlinkBehaviorEaseInOut(self.body, [bodyColor], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
        creativityFastBehaviorDict[ShapeType.LOOPS] = loopsFastBehavior

        loopsSlowBehavior = ComposedBehavior(self.body)
        loopsSlowBehavior.behaviorList.append(MoveBehaviorLoops(self.body, 30, MovementDirection.FORWARD, 2, 3.5, True))
        loopsSlowBehavior.behaviorList.append(BlinkBehaviorEaseInOut(self.body, [bodyColor], ColorBrightness.HIGH, 1, 7.0, Color(rgb=(0.0, 0.0, 0.0)), False))
        creativitySlowBehaviorDict[ShapeType.LOOPS] = loopsSlowBehavior

        rectFastBehavior = ComposedBehavior(self.body)
        rectFastBehavior.behaviorList.append(MoveBehaviorRect(self.body, 95, MovementDirection.FORWARD, 2, 1.5, True))
        rectFastBehavior.behaviorList.append(BlinkBehaviorEaseInOut(self.body, [bodyColor], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
        creativityFastBehaviorDict[ShapeType.RECT] = rectFastBehavior

        rectSlowBehavior = ComposedBehavior(self.body)
        rectSlowBehavior.behaviorList.append(MoveBehaviorRect(self.body, 30, MovementDirection.FORWARD, 2, 3.5, True))
        rectSlowBehavior.behaviorList.append(BlinkBehaviorEaseInOut(self.body, [bodyColor], ColorBrightness.HIGH, 1, 7.0, Color(rgb=(0.0, 0.0, 0.0)), False))
        creativitySlowBehaviorDict[ShapeType.RECT] = rectSlowBehavior

        spikesFastBehavior = ComposedBehavior(self.body)
        spikesFastBehavior.behaviorList.append(MoveBehaviorSpikes(self.body, 95, MovementDirection.FORWARD, 2, 1.5, True))
        spikesFastBehavior.behaviorList.append(BlinkBehaviorEaseInOut(self.body, [bodyColor], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
        creativityFastBehaviorDict[ShapeType.SPIKES] = spikesFastBehavior

        spikesSlowBehavior = ComposedBehavior(self.body)
        spikesSlowBehavior.behaviorList.append(MoveBehaviorSpikes(self.body, 30, MovementDirection.FORWARD, 2, 3.5, True))
        spikesSlowBehavior.behaviorList.append(BlinkBehaviorEaseInOut(self.body, [bodyColor], ColorBrightness.HIGH, 1, 7.0, Color(rgb=(0.0, 0.0, 0.0)), False))
        creativitySlowBehaviorDict[ShapeType.SPIKES] = spikesSlowBehavior

        straightFastBehavior = ComposedBehavior(self.body)
        straightFastBehavior.behaviorList.append(MoveBehaviorStraight(self.body, 95, MovementDirection.FORWARD, 2, 1.5, True))
        straightFastBehavior.behaviorList.append(BlinkBehaviorEaseInOut(self.body, [bodyColor], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
        creativityFastBehaviorDict[ShapeType.STRAIGHT] = straightFastBehavior

        straightSlowBehavior = ComposedBehavior(self.body)
        straightSlowBehavior.behaviorList.append(MoveBehaviorStraight(self.body, 30, MovementDirection.FORWARD, 2, 1.5, True))
        straightSlowBehavior.behaviorList.append(BlinkBehaviorEaseInOut(self.body, [bodyColor], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
        creativitySlowBehaviorDict[ShapeType.STRAIGHT] = straightSlowBehavior

        return CreativityProfile("Creative", 
            5, creativitySlowBehaviorDict, StoryArcBehaviorType.MIRROR, 
            3, creativityFastBehaviorDict, StoryArcBehaviorType.CONTRAST, 
            5, creativitySlowBehaviorDict, StoryArcBehaviorType.MIRROR)