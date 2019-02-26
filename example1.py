from Scripts.YOLOSoftware import *

bodyColor = Color(rgb=(0.5,0.0,0.5))
agent = Agent("YOLO")
bodyRef = agent.getBodyRef()

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

personalityProfile = PersonalityProfile("Punk", attentionCallBehavior, idleBehavior, personalityBehaviorList)


creativityBehaviorList = []
curvedFastBehavior = ComposedBehavior(bodyRef)
curvedFastBehavior.behaviorList.append(MoveBehaviorCurved(bodyRef, 95, MovementDirection.FORWARD, 2, 1.5, True))
curvedFastBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativityBehaviorList.append(curvedFastBehavior)

curvedSlowBehavior = ComposedBehavior(bodyRef)
curvedSlowBehavior.behaviorList.append(MoveBehaviorCurved(bodyRef, 30, MovementDirection.FORWARD, 2, 3.5, True))
curvedSlowBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 7.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativityBehaviorList.append(curvedSlowBehavior)

loopsFastBehavior = ComposedBehavior(bodyRef)
loopsFastBehavior.behaviorList.append(MoveBehaviorLoops(bodyRef, 95, MovementDirection.FORWARD, 2, 1.5, True))
loopsFastBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativityBehaviorList.append(loopsFastBehavior)

loopsSlowBehavior = ComposedBehavior(bodyRef)
loopsSlowBehavior.behaviorList.append(MoveBehaviorLoops(bodyRef, 30, MovementDirection.FORWARD, 2, 3.5, True))
loopsSlowBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 7.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativityBehaviorList.append(loopsSlowBehavior)

rectFastBehavior = ComposedBehavior(bodyRef)
rectFastBehavior.behaviorList.append(MoveBehaviorRect(bodyRef, 95, MovementDirection.FORWARD, 2, 1.5, True))
rectFastBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativityBehaviorList.append(rectFastBehavior)

rectSlowBehavior = ComposedBehavior(bodyRef)
rectSlowBehavior.behaviorList.append(MoveBehaviorRect(bodyRef, 30, MovementDirection.FORWARD, 2, 3.5, True))
rectSlowBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 7.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativityBehaviorList.append(rectSlowBehavior)

spikesFastBehavior = ComposedBehavior(bodyRef)
spikesFastBehavior.behaviorList.append(MoveBehaviorSpikes(bodyRef, 95, MovementDirection.FORWARD, 2, 1.5, True))
spikesFastBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativityBehaviorList.append(spikesFastBehavior)

spikesSlowBehavior = ComposedBehavior(bodyRef)
spikesSlowBehavior.behaviorList.append(MoveBehaviorSpikes(bodyRef, 30, MovementDirection.FORWARD, 2, 3.5, True))
spikesSlowBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 7.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativityBehaviorList.append(spikesSlowBehavior)

straightFastBehavior = ComposedBehavior(bodyRef)
straightFastBehavior.behaviorList.append(MoveBehaviorStraight(bodyRef, 95, MovementDirection.FORWARD, 2, 1.5, True))
straightFastBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativityBehaviorList.append(straightFastBehavior)

straightSlowBehavior = ComposedBehavior(bodyRef)
straightSlowBehavior.behaviorList.append(MoveBehaviorStraight(bodyRef, 30, MovementDirection.FORWARD, 2, 1.5, True))
straightSlowBehavior.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyColor], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
creativityBehaviorList.append(straightSlowBehavior)

creativityProfile = CreativityProfile("Creative", 
	5, creativityBehaviorList, StoryArcBehaviorType.MIRROR, 
	3, creativityBehaviorList, StoryArcBehaviorType.CONTRAST, 
	5, creativityBehaviorList, StoryArcBehaviorType.MIRROR)

agent.interact(bodyColor, personalityProfile, creativityProfile)
