import sys
sys.path.append('../..')

from Core.Agent import *


agent = Agent("YOLO")
controlRef = agent.getControlRef()

agent.interact(generalProfile = "EXUBERANT", socialProfile="EXUBERANT", creativityProfile="EXUBERANT")