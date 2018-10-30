from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior import *
from Scripts.Behaviors.SimpleBehaviors.FeelerBehavior import *
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from Libs.Constants import *
import time


class AloofBehavior2(ComposedBehavior):
    def __init__(self):
        # standard behaviors
        ComposedBehavior.__init__(self)

        # generic variables
        self.behaviorType = ComposedBehaviors.ALOOF_EXPRESSION_2

        return

    def prepareBehavior(self, body):

        for behavior in self.behaviorList:

                if behavior.behaviorType == Behaviors.BLINK:
                    behavior.prepareBehavior(body, [Color(rgb=(0.0, 1.0, 0.0)), Color(rgb=(0.0, 0.0, 1.0))], ColorBrightness.HIGH, Transitions.EASEINOUT, 3, 12, Color(rgb=(0.0, 0.0, 0.0)), True)
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
