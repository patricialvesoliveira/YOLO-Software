import sys
sys.path.append('..')

from Core.Agent import *

bodyColor = Color(rgb=(0.0,0.4,1.0))
agent = Agent("Ginie")
bodyRef = agent.getBodyRef()

#behaviors
helloBehavior = ComposedBehavior(bodyRef, [BlinkBehaviorEaseIn(bodyRef, bodyColor, ColorBrightness.MEDIUM, 1, 5.0, Color(rgb=(1.0,1.0,1.0)))])
goodbyeBehavior = ComposedBehavior(bodyRef, [BlinkBehaviorEaseOut(bodyRef, bodyColor, ColorBrightness.LOW, 1, 5.0, Color(rgb=(0.0,0.0,0.0)))])
puppeteerBehavior = ComposedBehavior(bodyRef, [BlinkBehaviorEaseInOut(bodyRef, bodyColor, ColorBrightness.HIGH, 3, 1.0, Color(rgb=(1.0,1.0,1.0)))])

behaviorList = []
behaviorList.append(BlinkBehaviorInstant(bodyRef, bodyColor, ColorBrightness.HIGH, 1, 1.0, Color(rgb=(1.0,1.0,1.0))))
behaviorList.append(BlinkBehaviorEaseOut(bodyRef, bodyColor, ColorBrightness.LOW, 1, 1.0, Color(rgb=(0.0,0.0,0.0))))

idleBehavior = ComposedBehavior(bodyRef, behaviorList)

GinieGeneralProfile = GeneralProfile("GinieGeneral", helloBehavior, goodbyeBehavior, puppeteerBehavior, idleBehavior, 1.0)

behaviorList = []
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, bodyColor, ColorBrightness.HIGH, 5, 0.5, Color(rgb=(1.0,0.0,0.0))))
attentionCallBehavior = ComposedBehavior(bodyRef, behaviorList)

personalityBehavior1 = ComposedBehavior(bodyRef, [MoveBehaviorCircle(bodyRef, 180, MovementDirection.FORWARD, 5, 3.0)])

personalityBehaviorList = []
personalityBehaviorList.append(personalityBehavior1)

GiniePersonalityProfile = PersonalityProfile("GiniePersonality", attentionCallBehavior, 15.0, personalityBehaviorList)

behaviorList = []
behaviorList.append(MoveBehaviorCircle(bodyRef, 180, MovementDirection.FORWARD, 5, 3.0))
behaviorList.append(BlinkBehaviorEaseOut(bodyRef, bodyColor, ColorBrightness.LOW, 1, 5.0, Color(rgb=(0.0,0.0,0.0))))
mainCreativeBehavior = ComposedBehavior(bodyRef, behaviorList)

allShapes = list(map(int, ShapeType))
creativityRABDict = {e:mainCreativeBehavior for e in allShapes}

GinieCreativityProfile = CreativityProfile("GinieCreative", 5.1, creativityRABDict, StoryArcBehaviorType.MIRROR, 5.1, creativityRABDict, StoryArcBehaviorType.MIRROR, 5.1, creativityRABDict, StoryArcBehaviorType.MIRROR)

agent.interact(personalityProfile = GiniePersonalityProfile, generalProfile=GinieGeneralProfile, creativityProfile = GinieCreativityProfile)