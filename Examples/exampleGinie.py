import sys
sys.path.append('..')

from Core.Agent import *

controlColor = Color(rgb=(0.0,0.4,1.0))
agent = Agent("Ginie")
controlRef = agent.getControlRef()

#behaviors
helloBehavior = ComposedBehavior(controlRef, [BlinkBehaviorEaseIn(controlRef, controlColor, ColorBrightness.MEDIUM, 1, 5.0, Color(rgb=(1.0,1.0,1.0)))])
goodbyeBehavior = ComposedBehavior(controlRef, [BlinkBehaviorEaseOut(controlRef, controlColor, ColorBrightness.LOW, 1, 5.0, Color(rgb=(0.0,0.0,0.0)))])
puppeteerBehavior = ComposedBehavior(controlRef, [BlinkBehaviorEaseInOut(controlRef, controlColor, ColorBrightness.HIGH, 3, 1.0, Color(rgb=(1.0,1.0,1.0)))])

behaviorList = []
behaviorList.append(BlinkBehaviorInstant(controlRef, controlColor, ColorBrightness.HIGH, 1, 1.0, Color(rgb=(1.0,1.0,1.0))))
behaviorList.append(BlinkBehaviorEaseOut(controlRef, controlColor, ColorBrightness.LOW, 1, 1.0, Color(rgb=(0.0,0.0,0.0))))

idleBehavior = ComposedBehavior(controlRef, behaviorList)

ginieGeneralProfile = GeneralProfile("GinieGeneral", helloBehavior, goodbyeBehavior, puppeteerBehavior, idleBehavior, 1.0)

behaviorList = []
behaviorList.append(BlinkBehaviorEaseInOut(controlRef, controlColor, ColorBrightness.HIGH, 5, 0.5, Color(rgb=(1.0,0.0,0.0))))
attentionCallBehavior = ComposedBehavior(controlRef, behaviorList)

socialBehavior1 = ComposedBehavior(controlRef, [MoveBehaviorCircle(controlRef, 180, MovementDirection.FORWARD, 5, 3.0)])

socialBehaviorList = []
socialBehaviorList.append(socialBehavior1)

ginieSocialProfile = SocialProfile("Giniesocial", attentionCallBehavior, 15.0, socialBehaviorList)

behaviorList = []
behaviorList.append(MoveBehaviorCircle(controlRef, 180, MovementDirection.FORWARD, 5, 3.0))
behaviorList.append(BlinkBehaviorEaseOut(controlRef, controlColor, ColorBrightness.LOW, 1, 5.0, Color(rgb=(0.0,0.0,0.0))))
mainCreativeBehavior = ComposedBehavior(controlRef, behaviorList)

allShapes = list(map(int, ShapeType))
creativityRABDict = {e:mainCreativeBehavior for e in allShapes}

ginieCreativityProfile = CreativityProfile("GinieCreative", 5.1, creativityRABDict, StoryArcBehaviorType.MIRROR, 5.1, creativityRABDict, StoryArcBehaviorType.MIRROR, 5.1, creativityRABDict, StoryArcBehaviorType.MIRROR)

agent.interact(socialProfile = GiniesocialProfile, generalProfile=GinieGeneralProfile, creativityProfile = GinieCreativityProfile)