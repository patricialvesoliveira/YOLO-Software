from Mind import Mind
from Body import Body
import sys


class Agent:
    def __init__(self, name, personalityType):
        self.name = name
        self.body = Body()
        self.mind = Mind(personalityType, self.body)

    def __del__(self):
        self.body = None
        self.mind = None

    def update(self):
        self.mind.update()
