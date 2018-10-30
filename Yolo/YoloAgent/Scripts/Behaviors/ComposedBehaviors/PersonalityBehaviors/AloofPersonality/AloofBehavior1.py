from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior import *
from Scripts.Behaviors.SimpleBehaviors.FeelerBehavior import *
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from Libs.Constants import *
import time


class AloofBehavior1(ComposedBehavior):
    def __init__(self):
        # standard behaviors
        ComposedBehavior.__init__(self)

        # generic variables
        self.behaviorType = ComposedBehaviors.ALOOF_EXPRESSION_1

        return

    def prepareBehavior(self, body):

        for behavior in self.behaviorList:

                if behavior.behaviorType == Behaviors.BLINK:
                    behavior.prepareBehavior(body, [Color(rgb=(0.0, 1.0, 0.0))], ColorBrightness.MEDIUM, Transitions.EASEIN, 1, 10, Color(rgb=(0.0, 0.0, 0.0)), True)
                    pass
                elif behavior.behaviorType == Behaviors.FEELER:
                    #behavior.PrepareBehavior(body, 0.86)
                    pass
                elif behavior.behaviorType == Behaviors.MOVE:
                    #behavior.prepareBehavior(body, Shapes.SPIKES, Transitions.LINEAR, 1, 5, True)
                    pass

                else:
                    raise IndexError("Prepare behavior: This standard behavior type doesn't exist")

        return
