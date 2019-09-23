import sys
sys.path.append('..')

from Core.Agent import *


controlColor = Color(rgb=(1.0,0.0,0.0))
agent = Agent("YOLO")
controlRef = agent.getControlRef()


helloBehavior = ComposedBehavior(controlRef, [BlinkBehaviorEaseInOut(controlRef, Color(rgb=(0.0,1.0,0.0)), ColorBrightness.LOW, 2, 3.0, Color(rgb=(0.0, 0.0, 0.0)))])
goodbyeBehavior = ComposedBehavior(controlRef, [BlinkBehaviorEaseInOut(controlRef, Color(rgb=(0.0,1.0,0.0)), ColorBrightness.LOW, 2, 3.0, Color(rgb=(0.0, 0.0, 0.0)))])
puppeteerBehavior = ComposedBehavior(controlRef,[BlinkBehaviorEaseInOut(controlRef, Color(rgb=(0.05,0.05,0.05)), ColorBrightness.LOW, 0, 1.0, Color(rgb=(0.0, 0.0, 0.0)))])

idleBehavior = ComposedBehavior(controlRef, [BlinkBehaviorEaseInOut(controlRef,  Color(rgb=(0.05,0.05,0.05)), ColorBrightness.LOW, 1, 2.0, Color(rgb=(1.0, 0.4, 0.0)))])

bugsBunnyGeneralProfile = GeneralProfile("BugsBunnyGeneral", helloBehavior, goodbyeBehavior, puppeteerBehavior, idleBehavior, 1.0)


attentionCallBehavior = ComposedBehavior(controlRef, [BlinkBehaviorInstant(controlRef, Color(rgb=(0.05,0.05,0.05)), ColorBrightness.HIGH, 4, 2.0, Color(rgb=(0.0, 0.0, 0.0)))])


behaviorList = []
behaviorList.append(BlinkBehaviorEaseInOut(controlRef, Color(rgb=(0.05,0.05,0.05)), ColorBrightness.LOW, 1, 4.0, Color(rgb=(0.0, 0.0, 0.0))))
behaviorList.append(MoveBehaviorStraight(controlRef, 30, MovementDirection.FORWARD, 2, 1.5))
socialBehavior1 = ComposedBehavior(controlRef, behaviorList)

behaviorList = []
behaviorList.append(BlinkBehaviorEaseInOut(controlRef, Color(rgb=(0.05,0.05,0.05)), ColorBrightness.LOW, 1, 4.0, Color(rgb=(0.0, 0.0, 0.0))))
behaviorList.append(MoveBehaviorStraight(controlRef, 50, MovementDirection.FORWARD, 2, 1.5))
socialBehavior2 = ComposedBehavior(controlRef, behaviorList)


socialBehaviorList = []
socialBehaviorList.append(socialBehavior1)
socialBehaviorList.append(socialBehavior2)

bugsBunnysocialProfile = SocialProfile("BugsBunnysocial", attentionCallBehavior, 10.0, socialBehaviorList)

behaviorList = []
behaviorList.append(BlinkBehaviorInstant(controlRef, Color(rgb=(1.0,0.4,0.0)), ColorBrightness.HIGH, 2, 2.0, Color(rgb=(0.0, 0.0, 0.0))))
behaviorList.append(MoveBehaviorCircle(controlRef, 50, MovementDirection.FORWARD, 2, 2.0))
risingCreativeBehavior = ComposedBehavior(controlRef, behaviorList)

behaviorList = []
behaviorList.append(BlinkBehaviorInstant(controlRef, Color(rgb=(1.0,0.4,0.0)), ColorBrightness.HIGH, 2, 2.0, Color(rgb=(0.0, 0.0, 0.0))))
behaviorList.append(MoveBehaviorSpikes(controlRef, 80, MovementDirection.FORWARD, 3, 2.0))
climaxCreativeBehavior = ComposedBehavior(controlRef, behaviorList)

behaviorList = []
behaviorList.append(BlinkBehaviorInstant(controlRef, Color(rgb=(1.0,0.4,0.0)), ColorBrightness.HIGH, 2, 2.0, Color(rgb=(0.0, 0.0, 0.0))))
behaviorList.append(MoveBehaviorCircle(controlRef, 30, MovementDirection.FORWARD, 2, 2.0))
fallingCreativeBehavior = ComposedBehavior(controlRef, behaviorList)

allShapes = list(map(int, ShapeType))
creativityRisingDict ={e:risingCreativeBehavior for e in allShapes}
creativityClimaxDict ={e:climaxCreativeBehavior for e in allShapes}
creativityFallingDict ={e:fallingCreativeBehavior for e in allShapes}


bugsBunnyCreativityProfile = CreativityProfile("BugsBunnyCreative", 
	3.1, creativityRisingDict, StoryArcBehaviorType.MIRROR, 
	5.1, creativityClimaxDict, StoryArcBehaviorType.CONTRAST, 
	3.1, creativityFallingDict, StoryArcBehaviorType.MIRROR)


agent.interact(generalProfile = bugsBunnyGeneralProfile, socialProfile=bugsBunnysocialProfile, creativityProfile = bugsBunnyCreativityProfile)