import sys
sys.path.append('../..')

from Core.Agent import *


agent = Agent("YOLO")
bodyRef = agent.getBodyRef()

agent.interact(generalProfile = "ALOOF", personalityProfile="ALOOF", creativityProfile="ALOOF")
