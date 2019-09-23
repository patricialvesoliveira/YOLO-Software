import sys
sys.path.append('..')

from Core.Agent import *

mainColor = Color(rgb=(0.0,0.4,1.0))
agent = Agent("Genie")
controlRef = agent.getControlRef()

#behaviors
helloBehavior = ComposedBehavior(controlRef, [BlinkBehaviorEaseIn(controlRef, mainColor, ColorBrightness.MEDIUM, 1, 5.0, Color(rgb=(1.0,1.0,1.0)))])
goodbyeBehavior = ComposedBehavior(controlRef, [BlinkBehaviorEaseOut(controlRef, mainColor, ColorBrightness.LOW, 1, 5.0, Color(rgb=(0.0,0.0,0.0)))])
puppeteerBehavior = ComposedBehavior(controlRef, [BlinkBehaviorEaseInOut(controlRef, mainColor, ColorBrightness.HIGH, 3, 1.0, Color(rgb=(1.0,1.0,1.0)))])

behaviorList = []
behaviorList.append(BlinkBehaviorInstant(controlRef, mainColor, ColorBrightness.HIGH, 1, 1.0, Color(rgb=(1.0,1.0,1.0))))
behaviorList.append(BlinkBehaviorEaseOut(controlRef, mainColor, ColorBrightness.LOW, 1, 1.0, Color(rgb=(0.0,0.0,0.0))))

idleBehavior = ComposedBehavior(controlRef, behaviorList)

ginieGeneralProfile = GeneralProfile("GenieGeneral", helloBehavior, goodbyeBehavior, puppeteerBehavior, idleBehavior, 1.0)

behaviorList = []
behaviorList.append(BlinkBehaviorEaseInOut(controlRef, mainColor, ColorBrightness.HIGH, 5, 0.5, Color(rgb=(1.0,0.0,0.0))))
attentionCallBehavior = ComposedBehavior(controlRef, behaviorList)

socialBehavior1 = ComposedBehavior(controlRef, [MoveBehaviorCircle(controlRef, 180, MovementDirection.FORWARD, 5, 3.0)])

socialBehaviorList = []
socialBehaviorList.append(socialBehavior1)

ginieSocialProfile = SocialProfile("GenieSocial", attentionCallBehavior, 15.0, socialBehaviorList)

behaviorList = []
behaviorList.append(MoveBehaviorCircle(controlRef, 180, MovementDirection.FORWARD, 5, 3.0))
behaviorList.append(BlinkBehaviorEaseOut(controlRef, mainColor, ColorBrightness.LOW, 1, 5.0, Color(rgb=(0.0,0.0,0.0))))
mainCreativeBehavior = ComposedBehavior(controlRef, behaviorList)

allShapes = list(map(int, ShapeType))
creativityRABDict = {e:mainCreativeBehavior for e in allShapes}

ginieCreativityProfile = CreativityProfile("GenieCreative", 5.1, creativityRABDict, StoryArcBehaviorType.MIRROR, 5.1, creativityRABDict, StoryArcBehaviorType.MIRROR, 5.1, creativityRABDict, StoryArcBehaviorType.MIRROR)

agent.interact(socialProfile = ginieSocialProfile, generalProfile = ginieGeneralProfile, creativityProfile = ginieCreativityProfile)