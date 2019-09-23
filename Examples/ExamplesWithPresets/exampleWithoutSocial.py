import sys
sys.path.append('../..')

from Core.Agent import *


agent = Agent("YOLO")
controlRef = agent.getControlRef()

agent.interact(creativityProfile="NEUTRAL")
