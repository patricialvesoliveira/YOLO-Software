import enum

class ApplicationMode(enum.Enum):
    AUTONOMOUS = 1
    DEMO = 2

# BODY

class SensorType(enum.Enum):
    OPTICAL = 1
    TOUCH = 2


class OpticalState(enum.Enum):
    RECEIVING = 1
    NOT_RECEIVING = 2
    FINISHED = 3



class TouchState(enum.Enum):
    TOUCHING = 1
    NOT_TOUCHING = 2



# MIND

class PersonalityType(enum.Enum):
    NONE = 0
    PUNK = 1
    AFFECTIVE = 2
    ALOOF = 3


class ShapeType(enum.Enum):
    NONE = 0
    SPIKES = 1
    CURVED = 2
    LOOPS = 3
    STRAIGHT = 4
    RECT = 5
    CIRCLE = 6
    FORWARD_AND_BACK = 7


class MovementDirection(enum.Enum):
    NONE = 0
    FORWARD = 1
    REVERSE = 2
    ALTERNATING = 3


# order is relevant here, the story progresses through its arcs sequentially
class StoryArc(enum.Enum):
    NONE = 0
    RISING_ACTION = 1
    CLIMAX = 2
    FALLING_ACTION = 3



class BehaviorType(enum.Enum):
    NONE = 0
    BLINK = 1
    MOVE = 2


class ComposedBehaviorType(enum.Enum):
    NONE = 0
    LOOPS_FAST = 1
    LOOPS_SLOW = 2
    CURVED_FAST = 3
    CURVED_SLOW = 4
    SPIKES_FAST = 5
    SPIKES_SLOW = 6
    STRAIGHT_FAST = 7
    STRAIGHT_SLOW = 8
    RECT_FAST = 9
    RECT_SLOW = 10
    PUPPETEER = 11
    AFFECTIVE_IDLE = 12
    AFFECTIVE_ATTENTION_CALL = 13
    AFFECTIVE_EXPRESSION_1 = 14
    AFFECTIVE_EXPRESSION_2 = 15
    AFFECTIVE_EXPRESSION_3 = 16
    PUNK_IDLE = 17
    PUNK_ATTENTION_CALL = 18
    PUNK_EXPRESSION_1 = 19
    PUNK_EXPRESSION_2 = 20
    PUNK_EXPRESSION_3 = 21
    ALOOF_IDLE = 22
    ALOOF_ATTENTION_CALL = 23
    ALOOF_EXPRESSION_1 = 24
    ALOOF_EXPRESSION_2 = 25
    ALOOF_EXPRESSION_3 = 26
    HELLO = 27
    BASE = 28


class BlinkingSpeed(enum.Enum):
    NONE = 0
    STOPPED = 1
    VERY_SLOW = 2
    SLOW = 3
    NORMAL = 4
    FAST = 5
    VERY_FAST = 6


class ColorType(enum.Enum):
    NONE = 0
    WHITE = 1
    GRAY = 2
    BLACK = 3
    YELLOW = 4
    DARKYELLOW = 5
    ORANGE = 6
    RED = 7
    DARKRED = 8
    PURPLE = 9
    DARKPURPLE = 10
    BLUE = 11
    DARKBLUE = 12
    CYAN = 13
    GREEN = 14
    DARKGREEN = 15
    BROWN = 16


class ColorBrightness(enum.Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3


ColorBrightnessValues = {'LOW': 120, 'MEDIUM': 180, 'HIGH': 255}
