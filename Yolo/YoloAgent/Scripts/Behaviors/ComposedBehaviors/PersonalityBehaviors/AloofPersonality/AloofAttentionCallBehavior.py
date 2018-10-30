from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior import *
from Scripts.Behaviors.SimpleBehaviors.FeelerBehavior import *
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from Libs.Constants import *
import time


class AloofAttentionCallBehavior(ComposedBehavior):
    def __init__(self):
        # standard behaviors
        ComposedBehavior.__init__(self)

        # generic variables
        self.behaviorType = ComposedBehaviors.ALOOF_ATTENTION_CALL

        return

    def prepareBehavior(self, body):

        for behavior in self.behaviorList:

                if behavior.behaviorType == Behaviors.BLINK:
                    pass
                elif behavior.behaviorType == Behaviors.FEELER:
                    pass
                elif behavior.behaviorType == Behaviors.MOVE:
                    pass

                else:
                    raise IndexError("Prepare behavior: This standard behavior type doesn't exist")

        return
