from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior import *
from Scripts.Behaviors.SimpleBehaviors.FeelerBehavior import *
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from Libs.Constants import *
import time


class AffectiveIdleBehavior(ComposedBehavior):
    def __init__(self):
        # standard behaviors
        ComposedBehavior.__init__(self)

        # generic variables
        self.behaviorType = ComposedBehaviors.AFFECTIVE_IDLE
        return

    def prepareBehavior(self, body):

        for behavior in self.behaviorList:

                if behavior.behaviorType == Behaviors.BLINK:
                    # Blink yellow -- rgb=(0.933333, 0.866667, 0.509804))
                    behavior.prepareBehavior(body, [Color(rgb=(1.0, 1.0, 0))], ColorBrightness.HIGH,
                                             Transitions.EASEINOUT, 1, 9, Color(rgb=(0, 0, 0)), False)
                    pass
                elif behavior.behaviorType == Behaviors.FEELER:
                    pass
                elif behavior.behaviorType == Behaviors.MOVE:
                    pass

                else:
                    raise IndexError("Prepare behavior: This standard behavior type doesn't exist")

        return
