import sys
sys.path.append('..')

from Core.Agent import *


bodyColor = Color(rgb=(1.0,0.0,0.0))
agent = Agent("YOLO")
bodyRef = agent.getBodyRef()


helloBehavior = ComposedBehavior(bodyRef, [BlinkBehaviorEaseIn(bodyRef, bodyColor, ColorBrightness.HIGH, 3, 2.0, Color(rgb=(0.0, 0.0, 0.0)))])
goodbyeBehavior = ComposedBehavior(bodyRef, [BlinkBehaviorEaseOut(bodyRef, bodyColor, ColorBrightness.HIGH, 3, 2.0, Color(rgb=(0.0, 0.0, 0.0)))])
puppeteerBehavior = ComposedBehavior(bodyRef,[BlinkBehaviorInstant(bodyRef, bodyColor, ColorBrightness.HIGH, 0, 1.0, Color(rgb=(0.0, 0.0, 0.0)))])

behaviorList = []
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, bodyColor, ColorBrightness.HIGH, 1, 2.0, Color(rgb=(0.0, 0.0, 0.0))))
idleBehavior = ComposedBehavior(bodyRef, behaviorList)

mickeyGeneralProfile = GeneralProfile("MickeyGeneral", helloBehavior, goodbyeBehavior, puppeteerBehavior, idleBehavior)


behaviorList = []
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, bodyColor, ColorBrightness.HIGH, 3, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
attentionCallBehavior = ComposedBehavior(bodyRef, behaviorList)

behaviorList = []
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, bodyColor, ColorBrightness.HIGH, 1, 4.5, Color(rgb=(0.0, 0.0, 0.0))))
behaviorList.append(MoveBehaviorCircle(bodyRef, 90, MovementDirection.FORWARD, 3, 1.5))
personalityBehavior1 = ComposedBehavior(bodyRef, behaviorList)

behaviorList = []
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, bodyColor, ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
personalityBehavior2 = ComposedBehavior(bodyRef, behaviorList)

personalityBehaviorList = []
personalityBehaviorList.append(personalityBehavior1)
personalityBehaviorList.append(personalityBehavior2)

mickeyPersonalityProfile = PersonalityProfile("MickeyPersonality", 1.0, attentionCallBehavior, 30.0, personalityBehaviorList)

behaviorList = []
behaviorList.append(MoveBehaviorLoops(bodyRef, 30, MovementDirection.FORWARD, 2, 1.5))
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, Color(rgb=(1.0,0.0,0.0)), ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
mainCreativeBehavior = ComposedBehavior(bodyRef, behaviorList)

allShapes = list(map(int, ShapeType))
creativityRABDict ={e:mainCreativeBehavior for e in allShapes}


mickeyCreativityProfile = CreativityProfile("MickeyCreative", 
	3.1, creativityRABDict, StoryArcBehaviorType.MIRROR, 
	5.1, creativityRABDict, StoryArcBehaviorType.CONTRAST, 
	3.1, creativityRABDict, StoryArcBehaviorType.MIRROR)


agent.interact(personalityProfile = mickeyPersonalityProfile, generalProfile=mickeyGeneralProfile, creativityProfile = mickeyCreativityProfile)