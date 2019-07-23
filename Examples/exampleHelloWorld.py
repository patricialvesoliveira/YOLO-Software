import sys
sys.path.append('..')

from Core.Agent import *


agent = Agent("YOLO")
bodyRef = agent.getBodyRef()


helloBehavior = ComposedBehavior(bodyRef, [BlinkBehaviorEaseInOut(bodyRef, Color(rgb=(1.0, 1.0, 1.0)), ColorBrightness.LOW, 2, 2.0, Color(rgb=(0.0, 0.0, 1.0)))])
goodbyeBehavior = ComposedBehavior(bodyRef, [])
puppeteerBehavior = ComposedBehavior(bodyRef,[])
idleBehavior = ComposedBehavior(bodyRef, [])

helloWorldGeneralProfile = GeneralProfile("helloWorldGeneral", helloBehavior, goodbyeBehavior, puppeteerBehavior, idleBehavior, 1.0)

agent.interact(generalProfile = helloWorldGeneralProfile)