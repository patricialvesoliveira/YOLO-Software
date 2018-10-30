import calendar
import logging
import time
import numpy

from Libs.Constants import *
from Libs.MachineLearning.lib.constants import SHAPE_ARRAY
from Libs.MachineLearning.lib.util import extract_features, predict
from Scripts.Behaviors.ComposedBehaviors.CreativeTechniques.CurvedFastBehavior import CurvedFastBehavior
from Scripts.Behaviors.ComposedBehaviors.CreativeTechniques.CurvedSlowBehavior import CurvedSlowBehavior
from Scripts.Behaviors.ComposedBehaviors.CreativeTechniques.LoopsFastBehavior import LoopsFastBehavior
from Scripts.Behaviors.ComposedBehaviors.CreativeTechniques.LoopsSlowBehavior import LoopsSlowBehavior
from Scripts.Behaviors.ComposedBehaviors.CreativeTechniques.RectFastBehavior import RectFastBehavior
from Scripts.Behaviors.ComposedBehaviors.CreativeTechniques.RectSlowBehavior import RectSlowBehavior
from Scripts.Behaviors.ComposedBehaviors.CreativeTechniques.SpikesFastBehavior import SpikesFastBehavior
from Scripts.Behaviors.ComposedBehaviors.CreativeTechniques.SpikesSlowBehavior import SpikesSlowBehavior
from Scripts.Behaviors.ComposedBehaviors.GenericBehaviors.PuppeteerBehavior import PuppeteerBehavior

from Scripts.Behaviors.ComposedBehaviors.PersonalityBehaviors.AffectivePersonality.AffectiveAttentionCallBehavior import \
    AffectiveAttentionCallBehavior
from Scripts.Behaviors.ComposedBehaviors.PersonalityBehaviors.AffectivePersonality.AffectiveBehavior1 import AffectiveBehavior1
from Scripts.Behaviors.ComposedBehaviors.PersonalityBehaviors.AffectivePersonality.AffectiveBehavior2 import AffectiveBehavior2
from Scripts.Behaviors.ComposedBehaviors.PersonalityBehaviors.AffectivePersonality.AffectiveHelloBehavior import AffectiveHelloBehavior
from Scripts.Behaviors.ComposedBehaviors.PersonalityBehaviors.AffectivePersonality.AffectiveIdleBehavior import AffectiveIdleBehavior
from Scripts.Behaviors.ComposedBehaviors.PersonalityBehaviors.AffectivePersonality.AffectiveBehavior3 import \
    AffectiveBehavior3

from Scripts.Behaviors.ComposedBehaviors.PersonalityBehaviors.AloofPersonality.AloofAttentionCallBehavior import \
    AloofAttentionCallBehavior
from Scripts.Behaviors.ComposedBehaviors.PersonalityBehaviors.AloofPersonality.AloofBehavior1 import AloofBehavior1
from Scripts.Behaviors.ComposedBehaviors.PersonalityBehaviors.AloofPersonality.AloofBehavior2 import AloofBehavior2
from Scripts.Behaviors.ComposedBehaviors.PersonalityBehaviors.AloofPersonality.AloofBehavior3 import AloofBehavior3
from Scripts.Behaviors.ComposedBehaviors.PersonalityBehaviors.AloofPersonality.AloofHelloBehavior import \
    AloofHelloBehavior
from Scripts.Behaviors.ComposedBehaviors.PersonalityBehaviors.AloofPersonality.AloofIdleBehavior import \
    AloofIdleBehavior

from Scripts.Behaviors.ComposedBehaviors.PersonalityBehaviors.PunkPersonality.PunkAttentionCallBehavior import \
    PunkAttentionCallBehavior
from Scripts.Behaviors.ComposedBehaviors.PersonalityBehaviors.PunkPersonality.PunkBehavior1 import PunkBehavior1
from Scripts.Behaviors.ComposedBehaviors.PersonalityBehaviors.PunkPersonality.PunkBehavior2 import PunkBehavior2
from Scripts.Behaviors.ComposedBehaviors.PersonalityBehaviors.PunkPersonality.PunkBehavior3 import PunkBehavior3
from Scripts.Behaviors.ComposedBehaviors.PersonalityBehaviors.PunkPersonality.PunkHelloBehavior import PunkHelloBehavior
from Scripts.Behaviors.ComposedBehaviors.PersonalityBehaviors.PunkPersonality.PunkIdleBehavior import PunkIdleBehavior


class Mind:
    """docstring for Mind"""

    def __init__(self, personality, body):

        # agent's variables
        self.personality = personality
        self.activeBehavior = AffectiveHelloBehavior()
        self.body = body

        # this will allow to cycle through the different story arcs
        self.currentStoryArcIndex = 1
        self.storyArcDuration = StoryArcTime[StoryArc(self.currentStoryArcIndex).name] * 60  # in seconds
        self.storyStartTime = time.time()

        # sensor variables
        self.touchStatus = Touch.NOT_TOUCHING
        self.opticalStatus = Optical.NOT_RECEIVING
        self.recognizedShape = None
        self.accelerationStatus = Acceleration.SLOW

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
        self.puppeteerBehavior = PuppeteerBehavior()

        # to check if the agent already introduced himself (happens only after first being touched)
        self.performedIntroduction = False


        return

    def update(self):

        self.parseSensorData(self.body.getSensorData())

        if time.time() - self.storyStartTime > self.storyArcDuration and self.currentStoryArcIndex < len(StoryArc) and self.performedIntroduction:
            # NOTE: if it has to be cumulative it's just adding the duration of the arcs to the previous one
            self.currentStoryArcIndex += 1
            self.storyArcDuration = StoryArcTime[StoryArc(self.currentStoryArcIndex).name] * 60  # in seconds
            self.storyStartTime = time.time()

        #print("Status: " + StoryArc(self.storyArcCurrent).name + " - elapsed: " + str(
        #    (time.time() - self.storyStartTime) / 60) + " - max: " + str(
        #    StoryArcTime[StoryArc(self.storyArcCurrent).name]))

        # Note : checks if there is a behavior being carried out and applies it, otherwise selects a new behavior on touch
        if self.activeBehavior is not None and not self.activeBehavior.isOver and self.touchStatus == Touch.NOT_TOUCHING:
            self.activeBehavior.applyBehavior(self.body)
            return
        elif self.touchStatus == Touch.TOUCHING and not self.wasTouched:
            #Note : if it's touched all behaviors should stop, so stopping them
            if self.idleBehavior is not None:
                self.idleBehavior.isOver = True

            #NOTE: this check only exists because during testing the decideBehavior() function could sometimes have missing behaviors
            # and return None, in the final version the behavior should always be defined at this point
            if self.activeBehavior is not None:
                self.activeBehavior.haltAndFinishBehavior(self.body)

            #Note: starts the puppeteer behavior that should change the robot's lights to white to indicate a puppeteer mode
            self.puppeteerBehavior.prepareBehavior(self.body)
            self.puppeteerBehavior.startBehavior()

            self.wasTouched = True
            self.touchStartTime = time.gmtime()
            return
        elif self.touchStatus == Touch.NOT_TOUCHING and self.wasTouched:
            self.decideBehavior()
            self.wasTouched = False
            self.startedIdle = False

            timestamp = calendar.timegm(self.touchStartTime)
            logging.info(StoryArc(self.currentStoryArcIndex).name + ' arc --- Touch recorded starting at ' + time.strftime("%H:%M:%S", self.touchStartTime) + ', with a duration of ' + "%.2f" % (time.time() - timestamp) + ' seconds. ')
            print(StoryArc(self.currentStoryArcIndex).name + ' arc --- Touch recorded starting at ' + time.strftime("%H:%M:%S", self.touchStartTime) + ', with a duration of ' + "%.2f" % (time.time() - timestamp) + ' seconds. ')

            return
        elif self.touchStatus == Touch.TOUCHING and not self.puppeteerBehavior.isOver:
            self.puppeteerBehavior.applyBehavior(self.body)
            return
        elif self.touchStatus == Touch.TOUCHING:
            #Note: this clause avoids having to test in all following ifs if the robot is still being touched
            return

        # There are two types of idle behaviors - a breathe behavior which played over and over and an attention call which happens once in a while
        if ((self.activeBehavior is not None and self.activeBehavior.isOver) or self.activeBehavior is None) and not self.startedIdle and self.performedIntroduction:
            self.startedIdle = True
            self.idleStartTime = time.time()
            self.startIdleBehavior()
            return
        elif self.startedIdle and time.time() - self.idleStartTime > self.idleAttentionCallInterval:
            self.startedIdle = False
            self.startAttentionCall()
            return
        elif self.startedIdle and self.idleBehavior is not None and not self.idleBehavior.isOver:
            self.idleBehavior.applyBehavior(self.body)
        elif self.startedIdle:
            self.startIdleBehavior()

        return


    def decideBehavior(self):

        # run the agent's personality behavior in first place
        if not self.performedIntroduction:
            self.startIntroduction()

            self.performedIntroduction = True
            # Note: only starts counting the story after children see a behavior
            self.storyStartTime = time.time()
            return

        randomValue = numpy.random.random() * StoryBehaviorTotalProbability

        # The probabilities change with each story arc
        personalityBehaviorProbability = StoryPersonalityBehaviorProbability[StoryArc(self.currentStoryArcIndex).name]
        creativeBehaviorProbability = StoryCreativeBehaviorProbability[StoryArc(self.currentStoryArcIndex).name]
        creativeBehaviorProbability += personalityBehaviorProbability  # to get the maximum value for the range
        #print("The value of " + str(randomValue) + " was chosen!")

        # Note: in some story arcs only personality behaviors are performed and creative techniques probability should be 0
        if randomValue <= personalityBehaviorProbability:
            print("Carrying out a new personality behavior.")
            self.activeBehavior = self.selectPersonalityBehavior()
        elif personalityBehaviorProbability < randomValue <= creativeBehaviorProbability:
            print("Carrying out a new creative technique.")
            self.activeBehavior = self.selectCreativeTechnique()

            #Note: if no suitable creative technique is found do a personality behavior
            if self.activeBehavior is None:
                print("Carrying out a new personality behavior instead.")
                self.activeBehavior = self.selectPersonalityBehavior()

        else:
            print("The value of " + str(randomValue) + " shouldn't be reachable!")
            logging.info('Error: Random values generated by the mind for decision making are over the threshold!')

        # Note: after executing a response behavior the path drawn should be cleared
        self.recognizedShape = None

        return

    def selectPersonalityBehavior(self):

        # to select between two possible outputs randomly
        randomValue = numpy.random.random_integers(3)

        if self.personality is Personality.AFFECTIVE:
            if randomValue == 1:
                selectedBehavior = AffectiveBehavior1()
            elif randomValue == 2:
                selectedBehavior = AffectiveBehavior2()
            elif randomValue == 3:
                selectedBehavior = AffectiveBehavior3()

        elif self.personality is Personality.ALOOF:
            if randomValue == 1:
                selectedBehavior = AloofBehavior1()
            elif randomValue == 2:
                selectedBehavior = AloofBehavior2()
            elif randomValue == 3:
                selectedBehavior = AloofBehavior3()

        elif self.personality is Personality.PUNK:
            if randomValue == 1:
                selectedBehavior = PunkBehavior1()
            elif randomValue == 2:
                selectedBehavior = PunkBehavior2()
            elif randomValue == 3:
                selectedBehavior = PunkBehavior3()

        else:
            print "This shouldn't happen, the mind didn't find this personality to match with a personality behavior"
            logging.info("Error: The mind didn't find this personality to match with a personality behavior")
            raise Exception("Error: The mind didn't find this personality to match with a personality behavior")

        selectedBehavior.prepareBehavior(self.body)
        selectedBehavior.startBehavior()

        logging.info(StoryArc(self.currentStoryArcIndex).name + ' arc --- Performing personality behavior: ' + selectedBehavior.behaviorType.name + ". ")

        return selectedBehavior

    def selectCreativeTechnique(self):

        selectedBehavior = None
        currentStoryArc = StoryArc(self.currentStoryArcIndex)

        # Note: guard is in place to prevent interactions (touch) with no discernable input patterns to trigger creative techniques
        # Additionally, for now the Straight shape has no response
        if self.recognizedShape is None or self.recognizedShape is Shapes.STRAIGHT:
            print "No suitable technique found. Staying idle"
            print StoryArc(self.currentStoryArcIndex).name + ' arc --- Corresponding input, recognized shape: ' + str(self.recognizedShape) + ', and acceleration: ' + self.accelerationStatus.name + '.'

            logging.info('Attempted to perform creative technique but no suitable technique was found')
            logging.info(StoryArc(self.currentStoryArcIndex).name + ' arc --- Corresponding input, recognized shape: ' + str(self.recognizedShape) + ', and acceleration: ' + self.accelerationStatus.name + '.')
            return None

        # to select between two possible outputs randomly
        randomValue = numpy.random.random_integers(2)

        # First 3 options should only use the social aspect & no creative techniques
        if currentStoryArc == StoryArc.EXPOSITION or currentStoryArc == StoryArc.CLIMAX or currentStoryArc == StoryArc.DENOUEMENT:
            print "Error: This clause should never be reached while selecting a creative technique, probabilities for these phases should not allow it"
            logging.info("Error: This clause should never be reached while selecting a creative technique, probabilities for these phases should not allow it")
            return None

        elif currentStoryArc == StoryArc.CONFLICT_INTRODUCED:

            if self.recognizedShape == Shapes.LOOPS.name and self.accelerationStatus == Acceleration.FAST:
                selectedBehavior = LoopsFastBehavior()
            elif self.recognizedShape == Shapes.LOOPS.name and self.accelerationStatus == Acceleration.SLOW:
                selectedBehavior = LoopsSlowBehavior()
            elif self.recognizedShape == Shapes.CURVED.name and self.accelerationStatus == Acceleration.FAST:
                selectedBehavior = CurvedFastBehavior()
            elif self.recognizedShape == Shapes.CURVED.name and self.accelerationStatus == Acceleration.SLOW:
                selectedBehavior = CurvedSlowBehavior()
            elif self.recognizedShape == Shapes.SPIKES.name and self.accelerationStatus == Acceleration.FAST:
                selectedBehavior = SpikesFastBehavior()
            elif self.recognizedShape == Shapes.SPIKES.name and self.accelerationStatus == Acceleration.SLOW:
                selectedBehavior = SpikesSlowBehavior()
            elif self.recognizedShape == Shapes.RECT.name and self.accelerationStatus == Acceleration.FAST:
                selectedBehavior = RectFastBehavior()
            elif self.recognizedShape == Shapes.RECT.name and self.accelerationStatus == Acceleration.SLOW:
                selectedBehavior = RectSlowBehavior()

        elif currentStoryArc == StoryArc.RISING_ACTION_PT1:

            if self.recognizedShape == Shapes.LOOPS.name and self.accelerationStatus == Acceleration.FAST:
                selectedBehavior = LoopsSlowBehavior()
            elif self.recognizedShape == Shapes.LOOPS.name and self.accelerationStatus == Acceleration.SLOW:
                selectedBehavior = LoopsFastBehavior()
            elif self.recognizedShape == Shapes.CURVED.name and self.accelerationStatus == Acceleration.FAST:
                selectedBehavior = CurvedSlowBehavior()
            elif self.recognizedShape == Shapes.CURVED.name and self.accelerationStatus == Acceleration.SLOW:
                selectedBehavior = CurvedFastBehavior()
            elif self.recognizedShape == Shapes.SPIKES.name and self.accelerationStatus == Acceleration.FAST:
                selectedBehavior = SpikesSlowBehavior()
            elif self.recognizedShape == Shapes.SPIKES.name and self.accelerationStatus == Acceleration.SLOW:
                selectedBehavior = SpikesFastBehavior()
            elif self.recognizedShape == Shapes.RECT.name and self.accelerationStatus == Acceleration.FAST:
                selectedBehavior = RectSlowBehavior()
            elif self.recognizedShape == Shapes.RECT.name and self.accelerationStatus == Acceleration.SLOW:
                selectedBehavior = RectFastBehavior()

        elif currentStoryArc == StoryArc.RISING_ACTION_PT2:

            if self.recognizedShape == Shapes.LOOPS.name and self.accelerationStatus == Acceleration.FAST:
                if randomValue == 1:
                    selectedBehavior = SpikesFastBehavior()
                else:
                    selectedBehavior = RectFastBehavior()
            elif self.recognizedShape == Shapes.LOOPS.name and self.accelerationStatus == Acceleration.SLOW:
                if randomValue == 1:
                    selectedBehavior = SpikesSlowBehavior()
                else:
                    selectedBehavior = RectSlowBehavior()
            elif self.recognizedShape == Shapes.CURVED.name and self.accelerationStatus == Acceleration.FAST:
                if randomValue == 1:
                    selectedBehavior = SpikesFastBehavior()
                else:
                    selectedBehavior = RectFastBehavior()
            elif self.recognizedShape == Shapes.CURVED.name and self.accelerationStatus == Acceleration.SLOW:
                if randomValue == 1:
                    selectedBehavior = SpikesSlowBehavior()
                else:
                    selectedBehavior = RectSlowBehavior()
            elif self.recognizedShape == Shapes.SPIKES.name and self.accelerationStatus == Acceleration.FAST:
                if randomValue == 1:
                    selectedBehavior = LoopsFastBehavior()
                else:
                    selectedBehavior = CurvedFastBehavior()
            elif self.recognizedShape == Shapes.SPIKES.name and self.accelerationStatus == Acceleration.SLOW:
                if randomValue == 1:
                    selectedBehavior = LoopsSlowBehavior()
                else:
                    selectedBehavior = CurvedSlowBehavior()
            elif self.recognizedShape == Shapes.RECT.name and self.accelerationStatus == Acceleration.FAST:
                if randomValue == 1:
                    selectedBehavior = LoopsFastBehavior()
                else:
                    selectedBehavior = CurvedFastBehavior()
            elif self.recognizedShape == Shapes.RECT.name and self.accelerationStatus == Acceleration.SLOW:
                if randomValue == 1:
                    selectedBehavior = LoopsSlowBehavior()
                else:
                    selectedBehavior = CurvedSlowBehavior()

        elif currentStoryArc == StoryArc.FALLING_ACTION_PT1:

            if self.recognizedShape == Shapes.LOOPS.name and self.accelerationStatus == Acceleration.FAST:
                if randomValue == 1:
                    selectedBehavior = SpikesSlowBehavior()
                else:
                    selectedBehavior = RectSlowBehavior()
            elif self.recognizedShape == Shapes.LOOPS.name and self.accelerationStatus == Acceleration.SLOW:
                if randomValue == 1:
                    selectedBehavior = SpikesFastBehavior()
                else:
                    selectedBehavior = RectFastBehavior()
            elif self.recognizedShape == Shapes.CURVED.name and self.accelerationStatus == Acceleration.FAST:
                if randomValue == 1:
                    selectedBehavior = SpikesSlowBehavior()
                else:
                    selectedBehavior = RectSlowBehavior()
            elif self.recognizedShape == Shapes.CURVED.name and self.accelerationStatus == Acceleration.SLOW:
                if randomValue == 1:
                    selectedBehavior = SpikesFastBehavior()
                else:
                    selectedBehavior = RectFastBehavior()
            elif self.recognizedShape == Shapes.SPIKES.name and self.accelerationStatus == Acceleration.FAST:
                if randomValue == 1:
                    selectedBehavior = LoopsSlowBehavior()
                else:
                    selectedBehavior = CurvedSlowBehavior()
            elif self.recognizedShape == Shapes.SPIKES.name and self.accelerationStatus == Acceleration.SLOW:
                if randomValue == 1:
                    selectedBehavior = LoopsFastBehavior()
                else:
                    selectedBehavior = CurvedFastBehavior()
            elif self.recognizedShape == Shapes.RECT.name and self.accelerationStatus == Acceleration.FAST:
                if randomValue == 1:
                    selectedBehavior = LoopsSlowBehavior()
                else:
                    selectedBehavior = CurvedSlowBehavior()
            elif self.recognizedShape == Shapes.RECT.name and self.accelerationStatus == Acceleration.SLOW:
                if randomValue == 1:
                    selectedBehavior = LoopsFastBehavior()
                else:
                    selectedBehavior = CurvedFastBehavior()

        elif currentStoryArc == StoryArc.FALLING_ACTION_PT2:

            if self.recognizedShape == Shapes.LOOPS.name and self.accelerationStatus == Acceleration.FAST:
                selectedBehavior = CurvedFastBehavior()
            elif self.recognizedShape == Shapes.LOOPS.name and self.accelerationStatus == Acceleration.SLOW:
                selectedBehavior = CurvedSlowBehavior()
            elif self.recognizedShape == Shapes.CURVED.name and self.accelerationStatus == Acceleration.FAST:
                selectedBehavior = LoopsFastBehavior()
            elif self.recognizedShape == Shapes.CURVED.name and self.accelerationStatus == Acceleration.SLOW:
                selectedBehavior = LoopsSlowBehavior()
            elif self.recognizedShape == Shapes.SPIKES.name and self.accelerationStatus == Acceleration.FAST:
                selectedBehavior = RectFastBehavior()
            elif self.recognizedShape == Shapes.SPIKES.name and self.accelerationStatus == Acceleration.SLOW:
                selectedBehavior = RectSlowBehavior()
            elif self.recognizedShape == Shapes.RECT.name and self.accelerationStatus == Acceleration.FAST:
                selectedBehavior = SpikesFastBehavior()
            elif self.recognizedShape == Shapes.RECT.name and self.accelerationStatus == Acceleration.SLOW:
                selectedBehavior = SpikesSlowBehavior()

        elif currentStoryArc == StoryArc.RESOLUTION:

            if self.recognizedShape == Shapes.LOOPS.name and self.accelerationStatus == Acceleration.FAST:
                selectedBehavior = LoopsFastBehavior()
            elif self.recognizedShape == Shapes.LOOPS.name and self.accelerationStatus == Acceleration.SLOW:
                selectedBehavior = LoopsSlowBehavior()
            elif self.recognizedShape == Shapes.CURVED.name and self.accelerationStatus == Acceleration.FAST:
                selectedBehavior = CurvedFastBehavior()
            elif self.recognizedShape == Shapes.CURVED.name and self.accelerationStatus == Acceleration.SLOW:
                selectedBehavior = CurvedSlowBehavior()
            elif self.recognizedShape == Shapes.SPIKES.name and self.accelerationStatus == Acceleration.FAST:
                selectedBehavior = SpikesFastBehavior()
            elif self.recognizedShape == Shapes.SPIKES.name and self.accelerationStatus == Acceleration.SLOW:
                selectedBehavior = SpikesSlowBehavior()
            elif self.recognizedShape == Shapes.RECT.name and self.accelerationStatus == Acceleration.FAST:
                selectedBehavior = RectFastBehavior()
            elif self.recognizedShape == Shapes.RECT.name and self.accelerationStatus == Acceleration.SLOW:
                selectedBehavior = RectSlowBehavior()


        print("Selected a creative technique")

        if selectedBehavior is not None:
            selectedBehavior.prepareBehavior(self.body)
            selectedBehavior.startBehavior()
            logging.info(' ' + StoryArc(self.currentStoryArcIndex).name + ' arc --- Performing creative technique: ' + selectedBehavior.behaviorType.name)
        else:
            print("No suitable technique found. Staying idle")
            print StoryArc(self.currentStoryArcIndex).name + ' arc --- Corresponding input, recognized shape: ' + str(
                self.recognizedShape) + ', and acceleration: ' + self.accelerationStatus.name + '.'
            logging.info('Attempted to perform creative technique but no suitable technique was found')
            logging.info(StoryArc(self.currentStoryArcIndex).name + ' arc --- Corresponding input, recognized shape: ' + str(self.recognizedShape) + ', and acceleration: ' + self.accelerationStatus.name + '.')
            return None

        return selectedBehavior

    def parseSensorData(self, sensorData):

        for sensor in sensorData:

            if sensor[0] == Sensor.TOUCH:
                self.touchStatus = sensor[1]

            elif sensor[0] == Sensor.ACCEL:
                self.accelerationStatus = sensor[1]

            elif sensor[0] == Sensor.OPTICAL:
                # NOTE: optical sensor also carries the data for the shape in a tuple
                self.opticalStatus = sensor[1][0]

                if self.opticalStatus == Optical.FINISHED:
                    self.recognizedShape = self.predictShape(sensor[1][1])

        #print("Sensor input parsed!")
        return

    def startIdleBehavior(self):

        if self.personality == Personality.AFFECTIVE:
            if self.idleBehavior is None:
                self.idleBehavior = AffectiveIdleBehavior()

        elif self.personality == Personality.ALOOF:
            if self.idleBehavior is None:
                self.idleBehavior = AloofIdleBehavior()

        elif self.personality == Personality.PUNK:
            if self.idleBehavior is None:
                self.idleBehavior = PunkIdleBehavior()
        else:
            print 'Error: Personality not found for idle behavior'
            raise Exception("Error: Personality not found for idle behavior")

        self.idleBehavior.prepareBehavior(self.body)
        self.idleBehavior.startBehavior()

        print StoryArc(self.currentStoryArcIndex).name + ' arc --- Performing idle behavior: ' + self.idleBehavior.behaviorType.name
        logging.info(StoryArc(self.currentStoryArcIndex).name + ' arc --- Performing idle behavior: ' + self.idleBehavior.behaviorType.name)

    def startAttentionCall(self):

        if self.personality == Personality.AFFECTIVE:
            self.activeBehavior = AffectiveAttentionCallBehavior()

        elif self.personality == Personality.ALOOF:
            self.activeBehavior = AloofAttentionCallBehavior()

        elif self.personality == Personality.PUNK:
            self.activeBehavior = PunkAttentionCallBehavior()
        else:
            print 'Error: Personality not found for attention call behavior'
            raise Exception("Error: Personality not found for attention call behavior")

        self.activeBehavior.prepareBehavior(self.body)
        self.activeBehavior.startBehavior()

        print StoryArc(self.currentStoryArcIndex).name + ' arc --- Performing attention call behavior: ' + self.activeBehavior.behaviorType.name
        logging.info(StoryArc(self.currentStoryArcIndex).name + ' arc --- Performing attention call behavior: ' + self.activeBehavior.behaviorType.name)


    def startIntroduction(self):

        if self.personality == Personality.AFFECTIVE:
            self.activeBehavior = AffectiveHelloBehavior()

        elif self.personality == Personality.ALOOF:
            self.activeBehavior = AloofHelloBehavior()

        elif self.personality == Personality.PUNK:
            self.activeBehavior = PunkHelloBehavior()
        else:
            print 'Error: Personality not found for introduction behavior'
            raise Exception("Error: Personality not found for introduction behavior")

        self.activeBehavior.prepareBehavior(self.body)
        self.activeBehavior.startBehavior()

        print StoryArc(self.currentStoryArcIndex).name + ' arc --- Performing introduction behavior: ' + self.activeBehavior.behaviorType.name
        logging.info(StoryArc(self.currentStoryArcIndex).name + ' arc --- Performing introduction behavior: ' + self.activeBehavior.behaviorType.name)

    def predictShape(self, pointDataArray):
        #print "shape recognized (length " + str(len(pointDataArray)) + "): " + str(pointDataArray)

        #print "Time feature extract start: " + time.strftime("%H:%M:%S", time.gmtime())
        features = extract_features(pointDataArray)
        prediction = predict(features)[0]
        #print "Time predict end: " + time.strftime("%H:%M:%S", time.gmtime())

        print StoryArc(self.currentStoryArcIndex).name + ' arc --- Recognized a shape: ' + SHAPE_ARRAY[int(prediction)]
        logging.info(StoryArc(self.currentStoryArcIndex).name + ' arc --- Recognized a shape: ' + SHAPE_ARRAY[int(prediction)])

        return SHAPE_ARRAY[int(prediction)]

