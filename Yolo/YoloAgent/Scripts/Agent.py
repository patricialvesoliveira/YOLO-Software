from Mind import Mind
from Body import Body
import sys

from colour import Color
from Libs.Constants import *


class Agent:
    def __init__(self, name, personalityType):
        self.name = name
        self.body = Body(self.generateBodyStimulusColor(personalityType))
        self.mind = Mind(personalityType, self.body)

    def __del__(self):
        self.body = None
        self.mind = None

    def generateBodyStimulusColor(self, personalityType):
    	switcher = {
    		PersonalityType.AFFECTIVE: Color(rgb=(1.0,0.55,0.0)),
    		PersonalityType.ALOOF: Color(rgb=(0.0,1.0,0.0)),
    		PersonalityType.PUNK: Color(rgb=(0.5,0.0,0.5))
    	}
    	return switcher.get(personalityType, "Invalid Personality Type")

    def update(self):
        self.mind.update()
