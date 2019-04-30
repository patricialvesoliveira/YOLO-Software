from enum import IntEnum

# Related to BODY
class SensorType(IntEnum):
    OPTICAL = 1
    TOUCH = 2

class OpticalState(IntEnum):
    RECEIVING = 1
    NOT_RECEIVING = 2
    FINISHED = 3

class TouchState(IntEnum):
    TOUCHING = 1
    NOT_TOUCHING = 2

class ColorBrightness(IntEnum):
    NONE = 0
    LOW = 120
    MEDIUM = 180
    HIGH = 255

#Related to BEHAVIOR
class ShapeType(IntEnum):
    NONE = 0
    SPIKES = 1
    CURVED = 2
    LOOPS = 3
    STRAIGHT = 4
    RECT = 5
    CIRCLE = 6
    FORWARD_AND_BACK = 7

class MovementDirection(IntEnum):
    NONE = 0
    FORWARD = 1
    REVERSE = 2
    ALTERNATING = 3



#Related to  MIND

# order is relevant here, the story progresses through its arcs sequentially
class StoryArc(IntEnum):
    NONE = 0
    RISING_ACTION = 1
    CLIMAX = 2
    FALLING_ACTION = 3

class StoryArcBehaviorType(IntEnum):
    NONE = 0
    MIRROR = 1
    CONTRAST = 2

