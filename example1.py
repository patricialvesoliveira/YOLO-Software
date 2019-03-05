from Scripts.YOLOSoftware import *

bodyColor = Color(rgb=(0.2,1.0,0.5))
agent = Agent("YOLO")
bodyRef = agent.getBodyRef()


behaviorList = []
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, Color(rgb=(0.0,0.1,0.5)), ColorBrightness.HIGH, 2, 2.0, Color(rgb=(0.0, 0.0, 0.0))))
helloBehavior = ComposedBehavior(bodyRef, behaviorList)

behaviorList = []
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, Color(rgb=(0.2,0.5,0.0)), ColorBrightness.HIGH, 1, 2.0, Color(rgb=(0.0, 0.0, 0.0))))
goodbyeBehavior = ComposedBehavior(bodyRef, behaviorList)

behaviorList = []
behaviorList.append(BlinkBehaviorInstant(bodyRef, Color(rgb=(1.0,0.0,1.0)), ColorBrightness.HIGH, 0, 2.0, Color(rgb=(0.0, 0.0, 0.0))))
puppeteerBehavior = ComposedBehavior(bodyRef, behaviorList)


behaviorList = []
behaviorList.append(BlinkBehaviorEaseIn(bodyRef, bodyColor, ColorBrightness.HIGH, 1, 2.0, Color(rgb=(0.0, 0.0, 0.0))))
idleBehavior = ComposedBehavior(bodyRef, behaviorList)

generalProfile = GeneralProfile("Jerk", helloBehavior, goodbyeBehavior, puppeteerBehavior, idleBehavior)


behaviorList = []
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, Color(rgb=(1.0, 1.0, 0.0)), ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
behaviorList.append(MoveBehaviorSpikes(bodyRef, 90, MovementDirection.ALTERNATING, 2, 1.5))
attentionCallBehavior = ComposedBehavior(bodyRef, behaviorList)


behaviorList = []
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, Color(rgb=(0.9, 0.0, 1.0)), ColorBrightness.HIGH, 1, 4.5, Color(rgb=(0.0, 0.0, 0.0))))
behaviorList.append(MoveBehaviorSpikes(bodyRef, 40, MovementDirection.FORWARD, 20, 1.5))
personalityBehavior1 = ComposedBehavior(bodyRef, behaviorList)

behaviorList = []
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, Color(rgb=(1.0, 0.0, 0.0)), ColorBrightness.HIGH, 1, 4.5, Color(rgb=(0.0, 0.0, 0.0))))
behaviorList.append(MoveBehaviorLoops(bodyRef, 50, MovementDirection.FORWARD, 20, 1.5))
personalityBehavior2 = ComposedBehavior(bodyRef, behaviorList)

personalityBehaviorList = []
personalityBehaviorList.append(personalityBehavior1)
personalityBehaviorList.append(personalityBehavior2)

personalityProfile = PersonalityProfile("Jerk", 1.0, attentionCallBehavior, 30.0, personalityBehaviorList)


creativitySlowBehaviorDict = {}
creativityFastBehaviorDict = {}

behaviorList = []
behaviorList.append(MoveBehaviorLoops(bodyRef, 95, MovementDirection.FORWARD, 2, 1.5))
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, bodyColor, ColorBrightness.HIGH, 20, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
curvedFastBehavior = ComposedBehavior(bodyRef, behaviorList)
creativityFastBehaviorDict[ShapeType.CURVED] = curvedFastBehavior

behaviorList = []
behaviorList.append(MoveBehaviorLoops(bodyRef, 30, MovementDirection.FORWARD, 2, 3.5))
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, bodyColor, ColorBrightness.HIGH, 20, 7.0, Color(rgb=(0.0, 0.0, 0.0))))
curvedSlowBehavior = ComposedBehavior(bodyRef, behaviorList)
creativitySlowBehaviorDict[ShapeType.CURVED] = curvedSlowBehavior

behaviorList = []
behaviorList.append(MoveBehaviorLoops(bodyRef, 95, MovementDirection.FORWARD, 2, 1.5))
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, bodyColor, ColorBrightness.HIGH, 20, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
loopsFastBehavior = ComposedBehavior(bodyRef, behaviorList)
creativityFastBehaviorDict[ShapeType.LOOPS] = loopsFastBehavior

behaviorList = []
behaviorList.append(MoveBehaviorLoops(bodyRef, 30, MovementDirection.FORWARD, 2, 3.5))
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, bodyColor, ColorBrightness.HIGH, 20, 7.0, Color(rgb=(0.0, 0.0, 0.0))))
loopsSlowBehavior = ComposedBehavior(bodyRef, behaviorList)
creativitySlowBehaviorDict[ShapeType.LOOPS] = loopsSlowBehavior

behaviorList = []
behaviorList.append(MoveBehaviorLoops(bodyRef, 95, MovementDirection.FORWARD, 2, 1.5))
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, bodyColor, ColorBrightness.HIGH, 20, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
rectFastBehavior = ComposedBehavior(bodyRef, behaviorList)
creativityFastBehaviorDict[ShapeType.RECT] = rectFastBehavior

behaviorList = []
behaviorList.append(MoveBehaviorLoops(bodyRef, 30, MovementDirection.FORWARD, 2, 3.5))
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, bodyColor, ColorBrightness.HIGH, 20, 7.0, Color(rgb=(0.0, 0.0, 0.0))))
rectSlowBehavior = ComposedBehavior(bodyRef, behaviorList)
creativitySlowBehaviorDict[ShapeType.RECT] = rectSlowBehavior

behaviorList = []
behaviorList.append(MoveBehaviorLoops(bodyRef, 95, MovementDirection.FORWARD, 2, 1.5))
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, bodyColor, ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
spikesFastBehavior = ComposedBehavior(bodyRef, behaviorList)
creativityFastBehaviorDict[ShapeType.SPIKES] = spikesFastBehavior

behaviorList = []
behaviorList.append(MoveBehaviorLoops(bodyRef, 30, MovementDirection.FORWARD, 2, 3.5))
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, bodyColor, ColorBrightness.HIGH, 20, 7.0, Color(rgb=(0.0, 0.0, 0.0))))
spikesSlowBehavior = ComposedBehavior(bodyRef, behaviorList)
creativitySlowBehaviorDict[ShapeType.SPIKES] = spikesSlowBehavior

behaviorList = []
behaviorList.append(MoveBehaviorLoops(bodyRef, 95, MovementDirection.FORWARD, 2, 1.5))
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, bodyColor, ColorBrightness.HIGH, 20, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
straightFastBehavior = ComposedBehavior(bodyRef, behaviorList)
creativityFastBehaviorDict[ShapeType.STRAIGHT] = straightFastBehavior

behaviorList = []
behaviorList.append(MoveBehaviorLoops(bodyRef, 30, MovementDirection.FORWARD, 2, 1.5))
behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, bodyColor, ColorBrightness.HIGH, 20, 3.0, Color(rgb=(0.0, 0.0, 0.0))))
straightSlowBehavior = ComposedBehavior(bodyRef, behaviorList)
creativitySlowBehaviorDict[ShapeType.STRAIGHT] = straightSlowBehavior


creativityProfile = CreativityProfile("Creative", 
	3.1, creativitySlowBehaviorDict, StoryArcBehaviorType.CONTRAST, 
	5.1, creativityFastBehaviorDict, StoryArcBehaviorType.CONTRAST, 
	3.1, creativitySlowBehaviorDict, StoryArcBehaviorType.MIRROR)

agent.interact(creativityProfile = creativityProfile)

agent.interact(personalityProfile = "AFFECTIVE", creativityProfile = "AFFECTIVE")

agent.interact(personalityProfile = "ALOOF", creativityProfile = "ALOOF")