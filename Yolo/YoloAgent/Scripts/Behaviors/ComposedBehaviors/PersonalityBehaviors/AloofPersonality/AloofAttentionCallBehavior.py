from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Libs.Constants import *
import time


class AloofAttentionCallBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviors.ALOOF_ATTENTION_CALL