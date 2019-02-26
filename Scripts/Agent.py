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
        risingActionTimeInMinutes, risingActionBehaviorList, risingActionBehaviorType, 
        climaxTimeInMinutes, climaxBehaviorList, climaxBehaviorType, 
        fallingActionTimeInMinutes, fallingActionBehaviorList, fallingActionBehaviorType):
        self.name = name
        self.risingActionTimeInMinutes = risingActionTimeInMinutes
        self.risingActionBehaviorList = risingActionBehaviorList
        self.risingActionBehaviorType = risingActionBehaviorType
        self.climaxTimeInMinutes = climaxTimeInMinutes
        self.climaxBehaviorList = climaxBehaviorList
        self.climaxBehaviorType = climaxBehaviorType
        self.fallingActionTimeInMinutes = fallingActionTimeInMinutes
        self.fallingActionBehaviorList = fallingActionBehaviorList
        self.fallingActionBehaviorType = fallingActionBehaviorType

class Agent:
    def __init__(self, name):
        defaultBodyColor = Color(rgb=(0.5,0.0,0.5))
        self.body = Body(defaultBodyColor)
        
        defaultPersonalityProfile = PersonalityProfile("", ComposedBehavior(self.body), ComposedBehavior(self.body), []);
        defaultCreativityProfile = CreativityProfile("", 0, [], StoryArcBehaviorType.MIRROR, 0, [], StoryArcBehaviorType.MIRROR, 0, [], StoryArcBehaviorType.MIRROR);
        
        self.mind = Mind(self.body, defaultPersonalityProfile, defaultCreativityProfile)
        self.name = name

    def __del__(self):
        self.body.__del__()
        self.mind = None

    def getBodyRef(self):
        return self.body
    
    def interact(self, stimulusColor, personalityProfile, creativityProfile):

        self.body.setStimulusColor(stimulusColor)
        self.mind.setBehaviorProfiles(personalityProfile, creativityProfile)
        try:
            while True:
                self.mind.update()
        except KeyboardInterrupt:
            print "Application closed due to user input!"
        except Exception as e:
            print "Error: " + str(e)
        finally:
            self.__del__()
        

def generatePunkProfilePreset():
    attentionCallBehavior = ComposedBehavior(bodyRef)
    attentionCallBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
    attentionCallBehavior.behaviorList.append(MoveBehaviorSpikes(bodyRef, 90, MovementDirection.ALTERNATING, 2, 1.5, False))

    idleBehavior = ComposedBehavior(bodyRef)
    idleBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 2.0, Color(rgb=(0.0, 0.0, 0.0)), False))

    personalityBehavior1 = ComposedBehavior(bodyRef)
    personalityBehavior1.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 4.5, Color(rgb=(0.0, 0.0, 0.0)), False))
    personalityBehavior1.behaviorList.append(MoveBehaviorSpikes(bodyRef, 80, MovementDirection.FORWARD, 3, 1.5, False))

    personalityBehavior2 = ComposedBehavior(bodyRef)
    personalityBehavior2.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 4.5, Color(rgb=(0.0, 0.0, 0.0)), False))
    personalityBehavior2.behaviorList.append(MoveBehaviorLoops(bodyRef, 80, MovementDirection.FORWARD, 3, 1.5, False))

    personalityBehavior3 = ComposedBehavior(bodyRef)
    personalityBehavior3.behaviorList.append(BlinkBehaviorInstant(bodyRef, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 2.5, Color(rgb=(0.0, 0.0, 0.0)), False))

    personalityBehaviorList = []
    personalityBehaviorList.append(personalityBehavior1)
    personalityBehaviorList.append(personalityBehavior2)
    personalityBehaviorList.append(personalityBehavior3)

    return personalityProfile = PersonalityProfile("Punk", attentionCallBehavior, idleBehavior, personalityBehaviorList)

def generateAffectiveProfilePreset():
    attentionCallBehavior = ComposedBehavior(bodyRef)
    attentionCallBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
    attentionCallBehavior.behaviorList.append(MoveBehaviorSpikes(bodyRef, 90, MovementDirection.ALTERNATING, 2, 1.5, False))

    idleBehavior = ComposedBehavior(bodyRef)
    idleBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 2.0, Color(rgb=(0.0, 0.0, 0.0)), False))

    personalityBehavior1 = ComposedBehavior(bodyRef)
    personalityBehavior1.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 4.5, Color(rgb=(0.0, 0.0, 0.0)), False))
    personalityBehavior1.behaviorList.append(MoveBehaviorSpikes(bodyRef, 80, MovementDirection.FORWARD, 3, 1.5, False))

    personalityBehavior2 = ComposedBehavior(bodyRef)
    personalityBehavior2.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 4.5, Color(rgb=(0.0, 0.0, 0.0)), False))
    personalityBehavior2.behaviorList.append(MoveBehaviorLoops(bodyRef, 80, MovementDirection.FORWARD, 3, 1.5, False))

    personalityBehavior3 = ComposedBehavior(bodyRef)
    personalityBehavior3.behaviorList.append(BlinkBehaviorInstant(bodyRef, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 2.5, Color(rgb=(0.0, 0.0, 0.0)), False))

    personalityBehaviorList = []
    personalityBehaviorList.append(personalityBehavior1)
    personalityBehaviorList.append(personalityBehavior2)
    personalityBehaviorList.append(personalityBehavior3)

    return personalityProfile = PersonalityProfile("Affective", attentionCallBehavior, idleBehavior, personalityBehaviorList)

def generateAloofProfilePreset():
    attentionCallBehavior = ComposedBehavior(bodyRef)
    attentionCallBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
    attentionCallBehavior.behaviorList.append(MoveBehaviorSpikes(bodyRef, 90, MovementDirection.ALTERNATING, 2, 1.5, False))

    idleBehavior = ComposedBehavior(bodyRef)
    idleBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 2.0, Color(rgb=(0.0, 0.0, 0.0)), False))

    personalityBehavior1 = ComposedBehavior(bodyRef)
    personalityBehavior1.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 4.5, Color(rgb=(0.0, 0.0, 0.0)), False))
    personalityBehavior1.behaviorList.append(MoveBehaviorSpikes(bodyRef, 80, MovementDirection.FORWARD, 3, 1.5, False))

    personalityBehavior2 = ComposedBehavior(bodyRef)
    personalityBehavior2.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 4.5, Color(rgb=(0.0, 0.0, 0.0)), False))
    personalityBehavior2.behaviorList.append(MoveBehaviorLoops(bodyRef, 80, MovementDirection.FORWARD, 3, 1.5, False))

    personalityBehavior3 = ComposedBehavior(bodyRef)
    personalityBehavior3.behaviorList.append(BlinkBehaviorInstant(bodyRef, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 2.5, Color(rgb=(0.0, 0.0, 0.0)), False))

    personalityBehaviorList = []
    personalityBehaviorList.append(personalityBehavior1)
    personalityBehaviorList.append(personalityBehavior2)
    personalityBehaviorList.append(personalityBehavior3)

    return personalityProfile = PersonalityProfile("Aloof", attentionCallBehavior, idleBehavior, personalityBehaviorList)