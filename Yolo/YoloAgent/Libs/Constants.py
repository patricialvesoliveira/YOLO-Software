import enum

class ApplicationMode(enum.Enum):
    AUTONOMOUS = 1
    DEMO = 2

# BODY

class Sensor(enum.Enum):
    OPTICAL = 1
    ACCEL = 2
    TOUCH = 3
    TILT = 4
    BATTERY = 5


class Optical(enum.Enum):
    RECEIVING = 1
    NOT_RECEIVING = 2
    FINISHED = 3


class Acceleration(enum.Enum):
    FAST = 1
    SLOW = 2


class Touch(enum.Enum):
    TOUCHING = 1
    NOT_TOUCHING = 2


class Tilt(enum.Enum):
    VERTICAL = 1
    HORIZONTAL = 2


class Battery(enum.Enum):
    LOW = 1
    OK = 2


# MIND

class Personality(enum.Enum):
    PUNK = 1
    AFFECTIVE = 2
    ALOOF = 3


class Shapes(enum.Enum):
    SPIKES = 1
    CURVED = 2
    LOOPS = 3
    STRAIGHT = 4
    RECT = 5
    CIRCLE = 6
    FORWARD_AND_BACK = 7


class MovementDirection(enum.Enum):
    STANDARD = 1
    REVERSE = 2
    ALTERNATING = 3


# order is relevant here, the story progresses through its arcs sequentially
class StoryArc(enum.Enum):
    EXPOSITION = 1
    CONFLICT_INTRODUCED = 2
    RISING_ACTION_PT1 = 3
    RISING_ACTION_PT2 = 4
    CLIMAX = 5
    FALLING_ACTION_PT1 = 6
    FALLING_ACTION_PT2 = 7
    RESOLUTION = 8
    DENOUEMENT = 9


# Time in minutes for each stage in the story arc
StoryArcTime = {'EXPOSITION': 3, 'CONFLICT_INTRODUCED': 2, 'RISING_ACTION_PT1': 5, 'RISING_ACTION_PT2': 5, 'CLIMAX': 1,
                'FALLING_ACTION_PT1': 5, 'FALLING_ACTION_PT2': 5, 'RESOLUTION': 2, 'DENOUEMENT': 2}

# Total probability for the
StoryBehaviorTotalProbability = 100

# Probabilities for the occurrence of either a creative technique or personality behavior at different points of the story
# Their sum should equal to the total probability
StoryPersonalityBehaviorProbability = {'EXPOSITION': 100, 'CONFLICT_INTRODUCED': 40, 'RISING_ACTION_PT1': 40, 'RISING_ACTION_PT2': 40, 'CLIMAX': 100,
                'FALLING_ACTION_PT1': 40, 'FALLING_ACTION_PT2': 40, 'RESOLUTION': 40, 'DENOUEMENT': 100}

StoryCreativeBehaviorProbability = {'EXPOSITION': 0, 'CONFLICT_INTRODUCED': 60, 'RISING_ACTION_PT1': 60, 'RISING_ACTION_PT2': 60, 'CLIMAX': 0,
                'FALLING_ACTION_PT1': 60, 'FALLING_ACTION_PT2': 60, 'RESOLUTION': 60, 'DENOUEMENT': 0}

# BEHAVIORS


class Behaviors(enum.Enum):
    BLINK = 1
    FEELER = 2
    MOVE = 3
    ROTATE = 4
    BASE = 5


class ComposedBehaviors(enum.Enum):
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
    AFFECTIVE_HELLO = 13
    AFFECTIVE_ATTENTION_CALL = 14
    AFFECTIVE_EXPRESSION_1 = 15
    AFFECTIVE_EXPRESSION_2 = 16
    AFFECTIVE_EXPRESSION_3 = 17
    PUNK_IDLE = 18
    PUNK_HELLO = 19
    PUNK_ATTENTION_CALL = 20
    PUNK_EXPRESSION_1 = 21
    PUNK_EXPRESSION_2 = 22
    PUNK_EXPRESSION_3 = 23
    ALOOF_IDLE = 24
    ALOOF_HELLO = 25
    ALOOF_ATTENTION_CALL = 26
    ALOOF_EXPRESSION_1 = 27
    ALOOF_EXPRESSION_2 = 28
    ALOOF_EXPRESSION_3 = 29
    BASE = 30


class BlinkingSpeed(enum.Enum):
    STOPPED = 1
    VERY_SLOW = 2
    SLOW = 3
    NORMAL = 4
    FAST = 5
    VERY_FAST = 6


class Colors(enum.Enum):
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
    LOW = 1
    MEDIUM = 2
    HIGH = 3


ColorBrightnessValues = {'LOW': 120, 'MEDIUM': 180, 'HIGH': 255}


class Transitions(enum.Enum):
    LINEAR = 1
    EASEIN = 2
    EASEOUT = 3
    INSTANT = 4
    EASEINOUT = 5
