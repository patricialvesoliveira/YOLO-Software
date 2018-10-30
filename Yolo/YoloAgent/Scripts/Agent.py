from Mind import Mind
from Body import Body
import sys


class Agent:
    def __init__(self, name, personality):
        self.name = name
        self.body = Body()
        self.mind = Mind(personality, self.body)

    def __del__(self):
        self.body = None
        self.mind = None

    def update(self):

        self.mind.update()
