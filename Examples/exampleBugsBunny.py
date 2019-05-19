import sys
sys.path.append('..')

from Core.Agent import *


bodyColor = Color(rgb=(1.0,0.0,0.0))
agent = Agent("YOLO")
bodyRef = agent.getBodyRef()


helloBehavior = ComposedBehavior(bodyRef, [BlinkBehaviorEaseInOut(bodyRef, Color(rgb=(0.0,1.0,0.0)), ColorBrightness.LOW, 2, 3.0, Color(rgb=(0.0, 0.0, 0.0)))])
goodbyeBehavior = ComposedBehavior(bodyRef, [BlinkBehaviorEaseInOut(bodyRef, Color(rgb=(0.0,1.0,0.0)), ColorBrightness.LOW, 2, 3.0, Color(rgb=(0.0, 0.0, 0.0)))])
puppeteerBehavior = ComposedBehavior(bodyRef,[BlinkBehaviorEaseInOut(bodyRef, Color(rgb=(0.05,0.05,0.05)), ColorBrightness.LOW, 0, 1.0, Color(rgb=(0.0, 0.0, 0.0)))])

idleBehavior = ComposedBehavior(bodyRef, [BlinkBehaviorEaseInOut(bodyRef,  Color(rgb=(0.05,0.05,0.05)), ColorBrightness.LOW, 1, 2.0, Color(rgb=(1.0, 0.4, 0.0)))])

bugsBunnyGeneralProfile = GeneralProfile("BugsBunnyGeneral", helloBehavior, goodbyeBehavior, puppeteerBehavior, idleBehavior, 1.0)


attentionCallBehavior = ComposedBehavior(bodyRef, [BlinkBehaviorInstant(bodyRef, Color(rgb=(0.05,0.05,0.05)), ColorBrightness.HIGH, 4, 2.0, Color(rgb=(0.0, 0.0, 0.0)))])


behaviorList = []
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, Color(rgb=(0.05,0.05,0.05)), ColorBrightness.LOW, 1, 4.0, Color(rgb=(0.0, 0.0, 0.0))))
behaviorList.append(MoveBehaviorStraight(bodyRef, 30, MovementDirection.FORWARD, 2, 1.5))
personalityBehavior1 = ComposedBehavior(bodyRef, behaviorList)

behaviorList = []
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, Color(rgb=(0.05,0.05,0.05)), ColorBrightness.LOW, 1, 4.0, Color(rgb=(0.0, 0.0, 0.0))))
behaviorList.append(MoveBehaviorStraight(bodyRef, 50, MovementDirection.FORWARD, 2, 1.5))
personalityBehavior2 = ComposedBehavior(bodyRef, behaviorList)


personalityBehaviorList = []
personalityBehaviorList.append(personalityBehavior1)
personalityBehaviorList.append(personalityBehavior2)

bugsBunnyPersonalityProfile = PersonalityProfile("BugsBunnyPersonality", attentionCallBehavior, 10.0, personalityBehaviorList)

behaviorList = []
behaviorList.append(BlinkBehaviorInstant(bodyRef, Color(rgb=(1.0,0.4,0.0)), ColorBrightness.HIGH, 2, 2.0, Color(rgb=(0.0, 0.0, 0.0))))
behaviorList.append(MoveBehaviorCircle(bodyRef, 50, MovementDirection.FORWARD, 2, 2.0))
risingCreativeBehavior = ComposedBehavior(bodyRef, behaviorList)

behaviorList = []
behaviorList.append(BlinkBehaviorInstant(bodyRef, Color(rgb=(1.0,0.4,0.0)), ColorBrightness.HIGH, 2, 2.0, Color(rgb=(0.0, 0.0, 0.0))))
behaviorList.append(MoveBehaviorSpikes(bodyRef, 80, MovementDirection.FORWARD, 3, 2.0))
climaxCreativeBehavior = ComposedBehavior(bodyRef, behaviorList)

behaviorList = []
behaviorList.append(BlinkBehaviorInstant(bodyRef, Color(rgb=(1.0,0.4,0.0)), ColorBrightness.HIGH, 2, 2.0, Color(rgb=(0.0, 0.0, 0.0))))
behaviorList.append(MoveBehaviorCircle(bodyRef, 30, MovementDirection.FORWARD, 2, 2.0))
fallingCreativeBehavior = ComposedBehavior(bodyRef, behaviorList)

allShapes = list(map(int, ShapeType))
creativityRisingDict ={e:risingCreativeBehavior for e in allShapes}
creativityClimaxDict ={e:climaxCreativeBehavior for e in allShapes}
creativityFallingDict ={e:fallingCreativeBehavior for e in allShapes}


bugsBunnyCreativityProfile = CreativityProfile("BugsBunnyCreative", 
	3.1, creativityRisingDict, StoryArcBehaviorType.MIRROR, 
	5.1, creativityClimaxDict, StoryArcBehaviorType.CONTRAST, 
	3.1, creativityFallingDict, StoryArcBehaviorType.MIRROR)


agent.interact(generalProfile = bugsBunnyGeneralProfile, personalityProfile=bugsBunnyPersonalityProfile, creativityProfile = bugsBunnyCreativityProfile)