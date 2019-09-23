import sys
sys.path.append('..')

from Core.Agent import *


controlColor = Color(rgb=(1.0,0.4,0.6))
agent = Agent("YOLO")
controlRef = agent.getControlRef()


helloBehavior = ComposedBehavior(controlRef, [BlinkBehaviorEaseIn(controlRef, controlColor, ColorBrightness.HIGH, 3, 2.0, Color(rgb=(0.0, 0.0, 0.0)))])
goodbyeBehavior = ComposedBehavior(controlRef, [BlinkBehaviorEaseOut(controlRef, controlColor, ColorBrightness.HIGH, 3, 2.0, Color(rgb=(0.0, 0.0, 0.0)))])
puppeteerBehavior = ComposedBehavior(controlRef,[BlinkBehaviorInstant(controlRef, controlColor, ColorBrightness.HIGH, 0, 1.0, Color(rgb=(0.0, 0.0, 0.0)))])

behaviorList = []
behaviorList.append(BlinkBehaviorEaseInOut(controlRef, controlColor, ColorBrightness.HIGH, 1, 2.0, Color(rgb=(0.0, 0.0, 0.0))))
idleBehavior = ComposedBehavior(controlRef, behaviorList)

barbieGeneralProfile = GeneralProfile("BarbieGeneral", helloBehavior, goodbyeBehavior, puppeteerBehavior, idleBehavior, 1.0)


behaviorList = []
behaviorList.append(BlinkBehaviorEaseOut(controlRef, controlColor, ColorBrightness.HIGH, 3, 1.0, Color(rgb=(0.0, 0.0, 0.0))))
attentionCallBehavior = ComposedBehavior(controlRef, behaviorList)


behaviorList = []
behaviorList.append(BlinkBehaviorEaseInOut(controlRef, controlColor, ColorBrightness.HIGH, 1, 4.5, Color(rgb=(0.0, 0.0, 0.0))))
behaviorList.append(MoveBehaviorCircle(controlRef, 90, MovementDirection.FORWARD, 3, 1.5))
socialBehavior1 = ComposedBehavior(controlRef, behaviorList)

socialBehaviorList = []
socialBehaviorList.append(socialBehavior1)

barbiesocialProfile = SocialProfile("Barbiesocial", attentionCallBehavior, 30.0, socialBehaviorList)

behaviorList = []
behaviorList.append(MoveBehaviorLoops(controlRef, 30, MovementDirection.FORWARD, 2, 1.5))
behaviorList.append(BlinkBehaviorEaseInOut(controlRef, Color(rgb=(1.0,0.3,1.0)), ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
mainCreativeBehavior = ComposedBehavior(controlRef, behaviorList)

allShapes = list(map(int, ShapeType))
creativityRABDict ={e:mainCreativeBehavior for e in allShapes}


barbieCreativityProfile = CreativityProfile("BarbieCreative", 
	3.1, creativityRABDict, StoryArcBehaviorType.MIRROR, 
	5.1, creativityRABDict, StoryArcBehaviorType.MIRROR, 
	3.1, creativityRABDict, StoryArcBehaviorType.MIRROR)


agent.interact(socialProfile = barbiesocialProfile, generalProfile=barbieGeneralProfile, creativityProfile = barbieCreativityProfile)