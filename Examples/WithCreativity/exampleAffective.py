import sys
sys.path.append('../..')

from Core.Agent import *


agent = Agent("YOLO")
bodyRef = agent.getBodyRef()

agent.interact(generalProfile = "AFFECTIVE", personalityProfile="AFFECTIVE", creativityProfile="AFFECTIVE")
