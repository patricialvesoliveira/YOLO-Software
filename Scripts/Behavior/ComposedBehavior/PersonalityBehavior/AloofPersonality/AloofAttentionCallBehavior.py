from colour import Color
from Libs.Constants import *
from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior


class AloofAttentionCallBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # Aloof does nothing on attention call
        ComposedBehavior.__init__(self, bodyRef)
        self.behaviorType = ComposedBehaviorType.ALOOF_ATTENTION_CALL