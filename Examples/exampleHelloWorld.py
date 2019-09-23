import sys
sys.path.append('..')

from Core.Agent import *


agent = Agent("YOLO")
controlRef = agent.getControlRef()


helloBehavior = ComposedBehavior(controlRef, [BlinkBehaviorEaseInOut(controlRef, Color(rgb=(1.0, 1.0, 1.0)), ColorBrightness.LOW, 2, 2.0, Color(rgb=(0.0, 0.0, 1.0)))])
goodbyeBehavior = ComposedBehavior(controlRef, [])
puppeteerBehavior = ComposedBehavior(controlRef,[])
idleBehavior = ComposedBehavior(controlRef, [])

helloWorldGeneralProfile = GeneralProfile("helloWorldGeneral", helloBehavior, goodbyeBehavior, puppeteerBehavior, idleBehavior, 1.0)

agent.interact(generalProfile = helloWorldGeneralProfile)