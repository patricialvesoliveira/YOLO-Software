import sys
import calendar
import logging
import time
import numpy

import traceback

from Libs.Constants import *
from Libs.MachineLearning.lib.constants import SHAPE_ARRAY
from Libs.MachineLearning.lib.util import extract_features, predict

from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseOut import BlinkBehaviorEaseOut
from colour import Color



from Scripts.Behavior.ComposedBehavior.CreativeTechnique.CurvedFastBehavior import CurvedFastBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.CurvedSlowBehavior import CurvedSlowBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.LoopsFastBehavior import LoopsFastBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.LoopsSlowBehavior import LoopsSlowBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.RectFastBehavior import RectFastBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.RectSlowBehavior import RectSlowBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.SpikesFastBehavior import SpikesFastBehavior
from Scripts.Behavior.ComposedBehavior.CreativeTechnique.SpikesSlowBehavior import SpikesSlowBehavior
from Behavior.ComposedBehavior.GenericBehavior.PuppeteerBehavior import PuppeteerBehavior

from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AffectivePersonality.AffectiveAttentionCallBehavior import AffectiveAttentionCallBehavior
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AffectivePersonality.AffectiveBehavior1 import AffectiveBehavior1
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AffectivePersonality.AffectiveBehavior2 import AffectiveBehavior2
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AffectivePersonality.AffectiveBehavior3 import AffectiveBehavior3
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AffectivePersonality.AffectiveHelloBehavior import AffectiveHelloBehavior
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AffectivePersonality.AffectiveIdleBehavior import AffectiveIdleBehavior

from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AloofPersonality.AloofAttentionCallBehavior import AloofAttentionCallBehavior
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AloofPersonality.AloofBehavior1 import AloofBehavior1
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AloofPersonality.AloofBehavior2 import AloofBehavior2
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AloofPersonality.AloofBehavior3 import AloofBehavior3
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AloofPersonality.AloofHelloBehavior import AloofHelloBehavior
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.AloofPersonality.AloofIdleBehavior import AloofIdleBehavior

from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.PunkPersonality.PunkAttentionCallBehavior import PunkAttentionCallBehavior
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.PunkPersonality.PunkBehavior1 import PunkBehavior1
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.PunkPersonality.PunkBehavior2 import PunkBehavior2
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.PunkPersonality.PunkBehavior3 import PunkBehavior3
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.PunkPersonality.PunkHelloBehavior import PunkHelloBehavior
from Scripts.Behavior.ComposedBehavior.PersonalityBehavior.PunkPersonality.PunkIdleBehavior import PunkIdleBehavior


class Mind:
    """docstring for Mind"""

    def __init__(self, personality, body):
        # agent's variables
        self.personality = personality
        self.body = body


        self.activeBehavior = PuppeteerBehavior(body)

        # this will allow to cycle through the different story arcs
        self.currentStoryArcIndex = 1
        self.storyArcDuration = StoryArcTime[StoryArc(self.currentStoryArcIndex).name] * 60  # in seconds
        self.storyStartTime = time.time()

        # sensor variables
        self.touchStatus = TouchState.NOT_TOUCHING
        self.opticalStatus = OpticalState.NOT_RECEIVING
        self.recognizedShape = None

        # behaviors are halted by touching the agent and new behaviors are performed after touch
        self.wasTouched = False
        # to document in logs the duration of an interaction children had
        self.touchStartTime = 0.0

        # idle checking variables
        self.startedIdle = False
        self.idleStartTime = time.time()
        self.idleAttentionCallInterval = 30
        self.idleBehavior = None

        # puppeteer behavior for when children grab the agent
        self.puppeteerBehavior = PuppeteerBehavior(body)

        # to check if the agent already introduced himself (happens only after first being touched)
        self.performedIntroduction = False

        self.testBehavior = BlinkBehaviorEaseOut(self.body, [Color(rgb=(1.0, 0.25, 0.0)),Color(rgb=(1.0, 1.0, 1.0))], ColorBrightness.MEDIUM, 1, 10, self.body.getColor(), True);

        return

    def update(self):

        self.testBehavior.applyBehavior()

        # self.parseSensorData(self.body.getSensorData())

        # if time.time() - self.storyStartTime > self.storyArcDuration and self.currentStoryArcIndex < len(StoryArc) and self.performedIntroduction:
        #     # NOTE: if it has to be cumulative it's just adding the duration of the arcs to the previous one
        #     self.currentStoryArcIndex += 1
        #     self.storyArcDuration = StoryArcTime[StoryArc(self.currentStoryArcIndex).name] * 60  # in seconds
        #     self.storyStartTime = time.time()

        # #print("Status: " + StoryArc(self.storyArcCurrent).name + " - elapsed: " + str(
        # #    (time.time() - self.storyStartTime) / 60) + " - max: " + str(
        # #    StoryArcTime[StoryArc(self.storyArcCurrent).name]))


        # # Note : checks if there is a behavior being carried out and applies it, otherwise selects a new behavior on touch
        # if self.activeBehavior is not None and not self.activeBehavior.isOver and self.touchStatus == TouchState.NOT_TOUCHING:
        #     self.activeBehavior.applyBehavior()
        #     return
        # elif self.touchStatus == TouchState.TOUCHING and not self.wasTouched:
        #     #Note : if it's touched all behaviors should stop, so stopping them
        #     if self.idleBehavior is not None:
        #         self.idleBehavior.isOver = True

        #     #NOTE: this check only exists because during testing the decideBehavior() function could sometimes have missing behaviors
        #     # and return None, in the final version the behavior should always be defined at this point
        #     if self.activeBehavior is not None:
        #         self.activeBehavior.haltAndFinishBehavior()

        #     #Note: starts the puppeteer behavior that should change the robot's lights to white to indicate a puppeteer mode
        #     # self.puppeteerBehavior.prepareBehavior()
        #     self.puppeteerBehavior.startBehavior()

        #     self.wasTouched = True
        #     self.touchStartTime = time.gmtime()
        #     return
        # elif self.touchStatus == TouchState.NOT_TOUCHING and self.wasTouched:
        #     self.puppeteerBehavior.haltAndFinishBehavior()
        #     self.decideBehavior()
        #     self.wasTouched = False
        #     self.startedIdle = False

        #     timestamp = calendar.timegm(self.touchStartTime)
        #     logging.info(StoryArc(self.currentStoryArcIndex).name + ' arc --- Touch recorded starting at ' + time.strftime("%H:%M:%S", self.touchStartTime) + ', with a duration of ' + "%.2f" % (time.time() - timestamp) + ' seconds. ')
        #     print(StoryArc(self.currentStoryArcIndex).name + ' arc --- Touch recorded starting at ' + time.strftime("%H:%M:%S", self.touchStartTime) + ', with a duration of ' + "%.2f" % (time.time() - timestamp) + ' seconds. ')

        #     return
        # elif self.touchStatus == TouchState.TOUCHING and not self.puppeteerBehavior.isOver:
        #     self.puppeteerBehavior.applyBehavior()
        #     return
        # elif self.touchStatus == TouchState.TOUCHING:
        #     #Note: this clause avoids having to test in all following ifs if the robot is still being touched
        #     return

        # # There are two types of idle behaviors - a breathe behavior which played over and over and an attention call which happens once in a while
        # if ((self.activeBehavior is not None and self.activeBehavior.isOver) or self.activeBehavior is None) and not self.startedIdle and self.performedIntroduction:
        #     self.startedIdle = True
        #     self.idleStartTime = time.time()
        #     self.startIdleBehavior()
        #     return
        # elif self.startedIdle and time.time() - self.idleStartTime > self.idleAttentionCallInterval:
        #     self.startedIdle = False
        #     self.startAttentionCall()
        #     return
        # elif self.startedIdle and self.idleBehavior is not None and not self.idleBehavior.isOver:
        #     self.idleBehavior.applyBehavior()
        # elif self.startedIdle:
        #     self.startIdleBehavior()

        return


    # def decideBehavior(self):

    #     # run the agent's personality behavior in first place
    #     if not self.performedIntroduction:
    #         self.startIntroduction()

    #         self.performedIntroduction = True
    #         # Note: only starts counting the story after children see a behavior
    #         self.storyStartTime = time.time()
    #         return

    #     randomValue = numpy.random.random() * StoryBehaviorTotalProbability

    #     # The probabilities change with each story arc
    #     personalityBehaviorProbability = StoryPersonalityBehaviorProbability[StoryArc(self.currentStoryArcIndex).name]
    #     creativeBehaviorProbability = StoryCreativeBehaviorProbability[StoryArc(self.currentStoryArcIndex).name]
    #     creativeBehaviorProbability += personalityBehaviorProbability  # to get the maximum value for the range
    #     #print("The value of " + str(randomValue) + " was chosen!")

    #     # Note: in some story arcs only personality behaviors are performed and creative techniques probability should be 0
    #     if randomValue <= personalityBehaviorProbability:
    #         print("Carrying out a new personality behavior.")
    #         self.activeBehavior = self.selectPersonalityBehavior()
    #     elif personalityBehaviorProbability < randomValue <= creativeBehaviorProbability:
    #         print("Carrying out a new creative technique.")
    #         self.activeBehavior = self.selectCreativeTechnique()

    #         #Note: if no suitable creative technique is found do a personality behavior
    #         if self.activeBehavior is None:
    #             print("Carrying out a new personality behavior instead.")
    #             self.activeBehavior = self.selectPersonalityBehavior()

    #     else:
    #         print("The value of " + str(randomValue) + " shouldn't be reachable!")
    #         logging.info('Error: Random values generated by the mind for decision making are over the threshold!')

    #     # Note: after executing a response behavior the path drawn should be cleared
    #     self.recognizedShape = None

    #     return

    # def selectPersonalityBehavior(self):

    #     # to select between two possible outputs randomly
    #     randomValue = numpy.random.random_integers(3)

    #     if self.personality is Personality.AFFECTIVE:
    #         if randomValue == 1:
    #             selectedBehavior = AffectiveBehavior1(self.body)
    #         elif randomValue == 2:
    #             selectedBehavior = AffectiveBehavior2(self.body)
    #         elif randomValue == 3:
    #             selectedBehavior = AffectiveBehavior3(self.body)

    #     elif self.personality is Personality.ALOOF:
    #         if randomValue == 1:
    #             selectedBehavior = AloofBehavior1(self.body)
    #         elif randomValue == 2:
    #             selectedBehavior = AloofBehavior2(self.body)
    #         elif randomValue == 3:
    #             selectedBehavior = AloofBehavior3(self.body)

    #     elif self.personality is Personality.PUNK:
    #         if randomValue == 1:
    #             selectedBehavior = PunkBehavior1(self.body)
    #         elif randomValue == 2:
    #             selectedBehavior = PunkBehavior2(self.body)
    #         elif randomValue == 3:
    #             selectedBehavior = PunkBehavior3(self.body)

    #     else:
    #         print "This shouldn't happen, the mind didn't find this personality to match with a personality behavior"
    #         logging.info("Error: The mind didn't find this personality to match with a personality behavior")
    #         raise Exception("Error: The mind didn't find this personality to match with a personality behavior")

    #     # selectedBehavior.prepareBehavior()
    #     selectedBehavior.startBehavior()

    #     logging.info(StoryArc(self.currentStoryArcIndex).name + ' arc --- Performing personality behavior: ' + selectedBehavior.behaviorType.name + ". ")

    #     return selectedBehavior

    # def selectCreativeTechnique(self):

    #     selectedBehavior = None
    #     currentStoryArc = StoryArc(self.currentStoryArcIndex)

    #     # Note: guard is in place to prevent interactions (touch) with no discernable input patterns to trigger creative techniques
    #     # Additionally, for now the Straight shape has no response
    #     if self.recognizedShape is None or self.recognizedShape is Shapes.STRAIGHT:
    #         print "No suitable technique found. Staying idle"
    #         print StoryArc(self.currentStoryArcIndex).name + ' arc --- Corresponding input, recognized shape: ' + str(self.recognizedShape) + '.'

    #         logging.info('Attempted to perform creative technique but no suitable technique was found')
    #         logging.info(StoryArc(self.currentStoryArcIndex).name + ' arc --- Corresponding input, recognized shape: ' + str(self.recognizedShape) + '.')
    #         return None

    #     # to select between two possible outputs randomly
    #     randomValue = numpy.random.random_integers(2)

    #     # First 3 options should only use the social aspect & no creative techniques
    #     if currentStoryArc == StoryArc.EXPOSITION or currentStoryArc == StoryArc.CLIMAX or currentStoryArc == StoryArc.DENOUEMENT:
    #         print "Error: This clause should never be reached while selecting a creative technique, probabilities for these phases should not allow it"
    #         logging.info("Error: This clause should never be reached while selecting a creative technique, probabilities for these phases should not allow it")
    #         return None

    #     elif currentStoryArc == StoryArc.CONFLICT_INTRODUCED:

    #         if self.recognizedShape == Shapes.LOOPS.name:
    #             selectedBehavior = LoopsFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.LOOPS.name:
    #             selectedBehavior = LoopsSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.CURVED.name:
    #             selectedBehavior = CurvedFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.CURVED.name:
    #             selectedBehavior = CurvedSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.SPIKES.name:
    #             selectedBehavior = SpikesFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.SPIKES.name:
    #             selectedBehavior = SpikesSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.RECT.name:
    #             selectedBehavior = RectFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.RECT.name:
    #             selectedBehavior = RectSlowBehavior(self.body)

    #     elif currentStoryArc == StoryArc.RISING_ACTION_PT1:

    #         if self.recognizedShape == Shapes.LOOPS.name:
    #             selectedBehavior = LoopsSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.LOOPS.name:
    #             selectedBehavior = LoopsFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.CURVED.name:
    #             selectedBehavior = CurvedSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.CURVED.name:
    #             selectedBehavior = CurvedFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.SPIKES.name:
    #             selectedBehavior = SpikesSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.SPIKES.name:
    #             selectedBehavior = SpikesFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.RECT.name:
    #             selectedBehavior = RectSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.RECT.name:
    #             selectedBehavior = RectFastBehavior(self.body)

    #     elif currentStoryArc == StoryArc.RISING_ACTION_PT2:

    #         if self.recognizedShape == Shapes.LOOPS.name:
    #             if randomValue == 1:
    #                 selectedBehavior = SpikesFastBehavior(self.body)
    #             else:
    #                 selectedBehavior = RectFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.LOOPS.name:
    #             if randomValue == 1:
    #                 selectedBehavior = SpikesSlowBehavior(self.body)
    #             else:
    #                 selectedBehavior = RectSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.CURVED.name:
    #             if randomValue == 1:
    #                 selectedBehavior = SpikesFastBehavior(self.body)
    #             else:
    #                 selectedBehavior = RectFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.CURVED.name:
    #             if randomValue == 1:
    #                 selectedBehavior = SpikesSlowBehavior(self.body)
    #             else:
    #                 selectedBehavior = RectSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.SPIKES.name:
    #             if randomValue == 1:
    #                 selectedBehavior = LoopsFastBehavior(self.body)
    #             else:
    #                 selectedBehavior = CurvedFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.SPIKES.name:
    #             if randomValue == 1:
    #                 selectedBehavior = LoopsSlowBehavior(self.body)
    #             else:
    #                 selectedBehavior = CurvedSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.RECT.name:
    #             if randomValue == 1:
    #                 selectedBehavior = LoopsFastBehavior(self.body)
    #             else:
    #                 selectedBehavior = CurvedFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.RECT.name:
    #             if randomValue == 1:
    #                 selectedBehavior = LoopsSlowBehavior(self.body)
    #             else:
    #                 selectedBehavior = CurvedSlowBehavior(self.body)

    #     elif currentStoryArc == StoryArc.FALLING_ACTION_PT1:

    #         if self.recognizedShape == Shapes.LOOPS.name:
    #             if randomValue == 1:
    #                 selectedBehavior = SpikesSlowBehavior(self.body)
    #             else:
    #                 selectedBehavior = RectSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.LOOPS.name:
    #             if randomValue == 1:
    #                 selectedBehavior = SpikesFastBehavior(self.body)
    #             else:
    #                 selectedBehavior = RectFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.CURVED.name:
    #             if randomValue == 1:
    #                 selectedBehavior = SpikesSlowBehavior(self.body)
    #             else:
    #                 selectedBehavior = RectSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.CURVED.name:
    #             if randomValue == 1:
    #                 selectedBehavior = SpikesFastBehavior(self.body)
    #             else:
    #                 selectedBehavior = RectFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.SPIKES.name:
    #             if randomValue == 1:
    #                 selectedBehavior = LoopsSlowBehavior(self.body)
    #             else:
    #                 selectedBehavior = CurvedSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.SPIKES.name:
    #             if randomValue == 1:
    #                 selectedBehavior = LoopsFastBehavior(self.body)
    #             else:
    #                 selectedBehavior = CurvedFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.RECT.name:
    #             if randomValue == 1:
    #                 selectedBehavior = LoopsSlowBehavior(self.body)
    #             else:
    #                 selectedBehavior = CurvedSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.RECT.name:
    #             if randomValue == 1:
    #                 selectedBehavior = LoopsFastBehavior(self.body)
    #             else:
    #                 selectedBehavior = CurvedFastBehavior(self.body)

    #     elif currentStoryArc == StoryArc.FALLING_ACTION_PT2:

    #         if self.recognizedShape == Shapes.LOOPS.name:
    #             selectedBehavior = CurvedFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.LOOPS.name:
    #             selectedBehavior = CurvedSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.CURVED.name:
    #             selectedBehavior = LoopsFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.CURVED.name:
    #             selectedBehavior = LoopsSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.SPIKES.name:
    #             selectedBehavior = RectFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.SPIKES.name:
    #             selectedBehavior = RectSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.RECT.name:
    #             selectedBehavior = SpikesFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.RECT.name:
    #             selectedBehavior = SpikesSlowBehavior(self.body)

    #     elif currentStoryArc == StoryArc.RESOLUTION:

    #         if self.recognizedShape == Shapes.LOOPS.name:
    #             selectedBehavior = LoopsFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.LOOPS.name:
    #             selectedBehavior = LoopsSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.CURVED.name:
    #             selectedBehavior = CurvedFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.CURVED.name:
    #             selectedBehavior = CurvedSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.SPIKES.name:
    #             selectedBehavior = SpikesFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.SPIKES.name:
    #             selectedBehavior = SpikesSlowBehavior(self.body)
    #         elif self.recognizedShape == Shapes.RECT.name:
    #             selectedBehavior = RectFastBehavior(self.body)
    #         elif self.recognizedShape == Shapes.RECT.name:
    #             selectedBehavior = RectSlowBehavior(self.body)


    #     print("Selected a creative technique")

    #     if selectedBehavior is not None:
    #         # selectedBehavior.prepareBehavior()
    #         selectedBehavior.startBehavior()
    #         logging.info(' ' + StoryArc(self.currentStoryArcIndex).name + ' arc --- Performing creative technique: ' + selectedBehavior.behaviorType.name)
    #     else:
    #         print("No suitable technique found. Staying idle")
    #         print StoryArc(self.currentStoryArcIndex).name + ' arc --- Corresponding input, recognized shape: ' + str(
    #             self.recognizedShape) + '.'
    #         logging.info('Attempted to perform creative technique but no suitable technique was found')
    #         logging.info(StoryArc(self.currentStoryArcIndex).name + ' arc --- Corresponding input, recognized shape: ' + str(self.recognizedShape) + ', and acceleration: ' + '.')
    #         return None

    #     return selectedBehavior

    # def parseSensorData(self, sensorData):

    #     for sensor in sensorData:

    #         if sensor[0] == SensorType.TOUCH:
    #             self.touchStatus = sensor[1]

    #         # elif sensor[0] == Sensor.ACCEL:
    #         #     self.accelerationStatus = sensor[1]

    #         elif sensor[0] == SensorType.OPTICAL:
    #             # NOTE: optical sensor also carries the data for the shape in a tuple
    #             self.opticalStatus = sensor[1][0]

    #             if self.opticalStatus == OpticalState.FINISHED:
    #                 self.recognizedShape = self.predictShape(sensor[1][1])

    #     #print("Sensor input parsed!")
    #     return

    # def startIdleBehavior(self):

    #     if self.personality == PersonalityType.AFFECTIVE:
    #         if self.idleBehavior is None:
    #             self.idleBehavior = AffectiveIdleBehavior(self.body)

    #     elif self.personality == PersonalityType.ALOOF:
    #         if self.idleBehavior is None:
    #             self.idleBehavior = AloofIdleBehavior(self.body)

    #     elif self.personality == PersonalityType.PUNK:
    #         if self.idleBehavior is None:
    #             self.idleBehavior = PunkIdleBehavior(self.body)
    #     else:
    #         print 'Error: Personality not found for idle behavior'
    #         raise Exception("Error: Personality not found for idle behavior")

    #     # self.idleBehavior.prepareBehavior(self.body)
    #     self.idleBehavior.startBehavior()

    #     print StoryArc(self.currentStoryArcIndex).name + ' arc --- Performing idle behavior: ' + self.idleBehavior.behaviorType.name
    #     logging.info(StoryArc(self.currentStoryArcIndex).name + ' arc --- Performing idle behavior: ' + self.idleBehavior.behaviorType.name)

    # def startAttentionCall(self):

    #     if self.personality == PersonalityType.AFFECTIVE:
    #         self.activeBehavior = AffectiveAttentionCallBehavior(self.body)

    #     elif self.personality == PersonalityType.ALOOF:
    #         self.activeBehavior = AloofAttentionCallBehavior(self.body)

    #     elif self.personality == PersonalityType.PUNK:
    #         self.activeBehavior = PunkAttentionCallBehavior(self.body)
    #     else:
    #         print 'Error: Personality not found for attention call behavior'
    #         raise Exception("Error: Personality not found for attention call behavior")

    #     # self.activeBehavior.prepareBehavior(self.body)
    #     self.activeBehavior.startBehavior()

    #     print StoryArc(self.currentStoryArcIndex).name + ' arc --- Performing attention call behavior: ' + self.activeBehavior.behaviorType.name
    #     logging.info(StoryArc(self.currentStoryArcIndex).name + ' arc --- Performing attention call behavior: ' + self.activeBehavior.behaviorType.name)


    # def startIntroduction(self):

    #     if self.personality == PersonalityType.AFFECTIVE:
    #         self.activeBehavior = AffectiveHelloBehavior(self.body)

    #     elif self.personality == PersonalityType.ALOOF:
    #         self.activeBehavior = AloofHelloBehavior(self.body)

    #     elif self.personality == PersonalityType.PUNK:
    #         self.activeBehavior = PunkHelloBehavior(self.body)
    #     else:
    #         print 'Error: Personality not found for introduction behavior'
    #         raise Exception("Error: Personality not found for introduction behavior")

    #     # self.activeBehavior.prepareBehavior()
    #     self.activeBehavior.startBehavior()

    #     print StoryArc(self.currentStoryArcIndex).name + ' arc --- Performing introduction behavior: ' + self.activeBehavior.behaviorType.name
    #     logging.info(StoryArc(self.currentStoryArcIndex).name + ' arc --- Performing introduction behavior: ' + self.activeBehavior.behaviorType.name)

    # def predictShape(self, pointDataArray):
    #     #print "shape recognized (length " + str(len(pointDataArray)) + "): " + str(pointDataArray)

    #     #print "Time feature extract start: " + time.strftime("%H:%M:%S", time.gmtime())
    #     features = extract_features(pointDataArray)
    #     prediction = predict(features)[0]
    #     #print "Time predict end: " + time.strftime("%H:%M:%S", time.gmtime())

    #     print StoryArc(self.currentStoryArcIndex).name + ' arc --- Recognized a shape: ' + SHAPE_ARRAY[int(prediction)]
    #     logging.info(StoryArc(self.currentStoryArcIndex).name + ' arc --- Recognized a shape: ' + SHAPE_ARRAY[int(prediction)])

    #     return SHAPE_ARRAY[int(prediction)]

