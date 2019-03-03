from Scripts.YOLOSoftware import *

bodyColor = Color(rgb=(0.2,1.0,0.5))
agent = Agent("YOLO")
bodyRef = agent.getBodyRef()

attentionCallBehavior = ComposedBehavior(bodyRef)
attentionCallBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [Color(rgb=(1.0, 1.0, 0.0))], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
attentionCallBehavior.behaviorList.append(MoveBehaviorSpikes(bodyRef, 90, MovementDirection.ALTERNATING, 2, 1.5, False))

idleBehavior = ComposedBehavior(bodyRef)
idleBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 2.0, Color(rgb=(0.0, 0.0, 0.0)), False))

helloBehavior = ComposedBehavior(bodyRef)
helloBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 2.0, Color(rgb=(0.0, 0.0, 0.0)), False))

puppeteerBehavior = ComposedBehavior(bodyRef)
puppeteerBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 2.0, Color(rgb=(0.0, 0.0, 0.0)), False))


personalityBehavior1 = ComposedBehavior(bodyRef)
personalityBehavior1.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [Color(rgb=(0.9, 0.0, 1.0))], ColorBrightness.HIGH, 1, 4.5, Color(rgb=(0.0, 0.0, 0.0)), False))
personalityBehavior1.behaviorList.append(MoveBehaviorSpikes(bodyRef, 40, MovementDirection.FORWARD, 3, 1.5, False))

personalityBehavior2 = ComposedBehavior(bodyRef)
personalityBehavior2.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 4.5, Color(rgb=(0.0, 0.0, 0.0)), False))
personalityBehavior2.behaviorList.append(MoveBehaviorLoops(bodyRef, 50, MovementDirection.FORWARD, 3, 1.5, False))

personalityBehaviorList = []
personalityBehaviorList.append(personalityBehavior1)
personalityBehaviorList.append(personalityBehavior2)

personalityProfile = PersonalityProfile("Jerk", 1.0, attentionCallBehavior, 30.0, helloBehavior, puppeteerBehavior, idleBehavior, personalityBehaviorList)


creativitySlowBehaviorDict = {}
creativityFastBehaviorDict = {}

curvedFastBehavior = ComposedBehavior(bodyRef)
curvedFastBehavior.behaviorList.append(MoveBehaviorLoops(bodyRef, 95, MovementDirection.FORWARD, 2, 1.5, True))
curvedFastBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativityFastBehaviorDict[ShapeType.CURVED] = curvedFastBehavior

curvedSlowBehavior = ComposedBehavior(bodyRef)
curvedSlowBehavior.behaviorList.append(MoveBehaviorLoops(bodyRef, 30, MovementDirection.FORWARD, 2, 3.5, True))
curvedSlowBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 7.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativitySlowBehaviorDict[ShapeType.CURVED] = curvedSlowBehavior

loopsFastBehavior = ComposedBehavior(bodyRef)
loopsFastBehavior.behaviorList.append(MoveBehaviorLoops(bodyRef, 95, MovementDirection.FORWARD, 2, 1.5, True))
loopsFastBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativityFastBehaviorDict[ShapeType.LOOPS] = loopsFastBehavior

loopsSlowBehavior = ComposedBehavior(bodyRef)
loopsSlowBehavior.behaviorList.append(MoveBehaviorLoops(bodyRef, 30, MovementDirection.FORWARD, 2, 3.5, True))
loopsSlowBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 7.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativitySlowBehaviorDict[ShapeType.LOOPS] = loopsSlowBehavior

rectFastBehavior = ComposedBehavior(bodyRef)
rectFastBehavior.behaviorList.append(MoveBehaviorLoops(bodyRef, 95, MovementDirection.FORWARD, 2, 1.5, True))
rectFastBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativityFastBehaviorDict[ShapeType.RECT] = rectFastBehavior

rectSlowBehavior = ComposedBehavior(bodyRef)
rectSlowBehavior.behaviorList.append(MoveBehaviorLoops(bodyRef, 30, MovementDirection.FORWARD, 2, 3.5, True))
rectSlowBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 7.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativitySlowBehaviorDict[ShapeType.RECT] = rectSlowBehavior

spikesFastBehavior = ComposedBehavior(bodyRef)
spikesFastBehavior.behaviorList.append(MoveBehaviorLoops(bodyRef, 95, MovementDirection.FORWARD, 2, 1.5, True))
spikesFastBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativityFastBehaviorDict[ShapeType.SPIKES] = spikesFastBehavior

spikesSlowBehavior = ComposedBehavior(bodyRef)
spikesSlowBehavior.behaviorList.append(MoveBehaviorLoops(bodyRef, 30, MovementDirection.FORWARD, 2, 3.5, True))
spikesSlowBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 7.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativitySlowBehaviorDict[ShapeType.SPIKES] = spikesSlowBehavior

straightFastBehavior = ComposedBehavior(bodyRef)
straightFastBehavior.behaviorList.append(MoveBehaviorLoops(bodyRef, 95, MovementDirection.FORWARD, 2, 1.5, True))
straightFastBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativityFastBehaviorDict[ShapeType.STRAIGHT] = straightFastBehavior

straightSlowBehavior = ComposedBehavior(bodyRef)
straightSlowBehavior.behaviorList.append(MoveBehaviorLoops(bodyRef, 30, MovementDirection.FORWARD, 2, 1.5, True))
straightSlowBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativitySlowBehaviorDict[ShapeType.STRAIGHT] = straightSlowBehavior


creativityProfile = CreativityProfile("Creative", 
	0.1, creativitySlowBehaviorDict, StoryArcBehaviorType.CONTRAST, 
	0.1, creativityFastBehaviorDict, StoryArcBehaviorType.CONTRAST, 
	0.1, creativitySlowBehaviorDict, StoryArcBehaviorType.MIRROR)

agent.interact(personalityProfile = "PUNK", creativityProfile = creativityProfile)

agent.interact(personalityProfile = "AFFECTIVE")