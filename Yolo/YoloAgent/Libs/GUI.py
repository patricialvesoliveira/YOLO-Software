from ttk import Progressbar

from Libs.Constants import *
from Scripts.Agent import Agent
from Tkinter import *
import tkMessageBox
import logging
import os
import platform
import traceback
import sys


class GUI:
    def __init__(self, agent):
        try:
            self.agent = agent
            self.b1 = "up"
            self.xold, self.yold = None, None

            self.applicationGUI = Tk()
            # Code to add widgets will go here...
            self.applicationGUI.title("YOLO agent demonstration GUI")
            self.applicationGUI.geometry("800x600")

            # NOTE: screen is split in 2 frames: on the left drawing input and console; on the right buttons to simulate different inputs
            fullscreen = PanedWindow(self.applicationGUI)
            fullscreen.pack(fill=BOTH, expand=1)

            # NOTE: Left side of screen
            leftScreen = PanedWindow(fullscreen, orient=VERTICAL)
            leftScreen.pack(expand=1)
            fullscreen.add(leftScreen)

            shapeInputCanvas = Canvas(self.applicationGUI, height=250, borderwidth=5, background="white")
            shapeInputCanvas.pack()
            leftScreen.add(shapeInputCanvas)

            shapeInputCanvas.bind("<Motion>", self.motion)
            shapeInputCanvas.bind("<ButtonPress-1>", self.b1down)
            shapeInputCanvas.bind("<ButtonRelease-1>", self.b1up)

            console = Text(self.applicationGUI, width=50, height=50)
            console.pack()
            leftScreen.add(console)

            # NOTE: Right side of screen
            rightScreen = PanedWindow(fullscreen, orient=VERTICAL)
            rightScreen.pack(expand=1)
            fullscreen.add(rightScreen)

            # agent input controls
            inputControlslabelframe = LabelFrame(rightScreen, text="Agent input controls")
            inputControlslabelframe.pack()
            rightScreen.add(inputControlslabelframe)
            # Application mode & switch
            applicationModeFrame = Frame(inputControlslabelframe)
            applicationModeFrame.pack(expand=1)

            applicationModeState = Label(applicationModeFrame,
                                         text="Current application mode: " + self.agent.body.applicationMode.name)
            applicationModeState.pack()

            switchApplicationModeButton = Button(applicationModeFrame, text="Switch application mode",
                                                 command=lambda: self.switchApplicationMode(console, applicationModeState))
            switchApplicationModeButton.pack()

            # Acceleration input & state
            accelerationOptions = ["Slow", "Fast"]

            accelerationInputFrame = Frame(inputControlslabelframe)
            accelerationInputFrame.pack(expand=1)

            self.accelerationInputState = Label(accelerationInputFrame,
                                           text="Current acceleration state: " + self.agent.body.getAccelerationSensorData()[
                                               1].name)
            self.accelerationInputState.pack()

            selectedAccelerationOption = StringVar(accelerationInputFrame)
            selectedAccelerationOption.set(accelerationOptions[0])  # initial value

            option = OptionMenu(accelerationInputFrame, selectedAccelerationOption, *accelerationOptions,
                                command=self.updateAccelerationInput(console, self.accelerationInputState))
            option.pack()

            # Touch input & state
            touchOptions = ["Touching", "Not Touching"]

            touchInputFrame = Frame(inputControlslabelframe)
            touchInputFrame.pack(expand=1)

            self.touchInputState = Label(touchInputFrame, text="Current touch state: " + self.agent.body.getTouchSensorData()[1].name)
            self.touchInputState.pack()

            selectedTouchOption = StringVar(touchInputFrame)
            selectedTouchOption.set(touchOptions[0])  # initial value

            option = OptionMenu(touchInputFrame, selectedTouchOption, *touchOptions,
                                command=self.updateTouchInput(console, self.touchInputState))
            option.pack()

            # agent current state
            agentStatuslabelframe = LabelFrame(rightScreen, text="Agent current status")
            agentStatuslabelframe.pack()
            rightScreen.add(agentStatuslabelframe)

            # head's LEDs state
            self.agentColorName = Label(agentStatuslabelframe, text="Current agent's color: " + str(self.agent.body.getColor()))
            self.agentColorName.pack()

            self.agentColorCanvas = Canvas(agentStatuslabelframe, width=50, height=50, borderwidth=5, background="black")
            self.agentColorCanvas.pack()

            # head's extension state
            self.agentHeadMovementName = Label(agentStatuslabelframe,
                                               text="Current head height (%): " + str(self.agent.body.getFeelerPosition()))
            self.agentHeadMovementName.pack()

            self.headProgressValue = DoubleVar()
            self.headProgressValue.set(self.agent.body.getFeelerPosition())
            agentHeadMovementStatus = Progressbar(agentStatuslabelframe, variable=self.headProgressValue, orient=VERTICAL,
                                                  length=80, mode='determinate')
            agentHeadMovementStatus.pack()

            # Recognized shape
            recognizedShapeFrame = Frame(agentStatuslabelframe)
            recognizedShapeFrame.pack(expand=1)

            self.recognizedShapeName = Label(recognizedShapeFrame,
                                             text="Current shape recognized: " + str(self.agent.mind.recognizedShape))
            self.recognizedShapeName.pack()

            # Behavior underway
            activeBehaviorFrame = Frame(agentStatuslabelframe)
            activeBehaviorFrame.pack(expand=1)

            self.activeBehaviorName = Label(activeBehaviorFrame,
                                            text="Active behavior: " + str(self.agent.mind.activeBehavior.behaviorType))
            self.activeBehaviorName.pack()

            # Current story arc
            storyArcFrame = Frame(agentStatuslabelframe)
            storyArcFrame.pack(expand=1)

            self.storyArcName = Label(storyArcFrame, text="Current story arc: " + StoryArc(
                self.agent.mind.currentStoryArcIndex).name)
            self.storyArcName.pack()

            self.applicationGUI.after(10, self.applicationMainLoop)
            self.applicationGUI.protocol("WM_DELETE_WINDOW", self.on_closing)
            logging.info('GUI setup finished')

        except Exception, e:
            print('Error: Problem with GUI setup. ' + str(e))
            return

    def startMainApplicationLoop(self):
        self.applicationGUI.mainloop()

    def applicationMainLoop(self):

        try:
            self.agent.update()
        except Exception, e:
            print str(traceback.print_exc())
            print('Error: ' + str(e))
            self.agent = None
            return

        self.recognizedShapeName.config(text="Current shape recognized: " + str(self.agent.mind.recognizedShape))

        if self.agent.mind.activeBehavior is not None and not self.agent.mind.activeBehavior.isOver:
            self.activeBehaviorName.config(text="Active behavior: " + str(self.agent.mind.activeBehavior.behaviorType))
        elif self.agent.mind.idleBehavior is not None and not self.agent.mind.idleBehavior.isOver:
            self.activeBehaviorName.config(text="Idle behavior active: " + str(
                self.agent.mind.idleBehavior.behaviorType))

        mycolor = self.agent.body.getColor().rgb
        color = (self.translate(mycolor[0], 0.0, 1.0, 0, 254), self.translate(mycolor[1], 0.0, 1.0, 0, 254), self.translate(mycolor[2], 0.0, 1.0, 0, 254))
        colorval = "#%02x%02x%02x" % color
        self.agentColorName.config(
            text="Current agent's color: (" + "%.1f" % color[0] + ", " + "%.1f" % color[1] + ", " + "%.1f" % color[
                2] + ")")
        self.agentColorCanvas.config(bg=colorval)

        self.touchInputState.config(text="Current touch state: " + self.agent.body.getTouchSensorData()[1].name)
        self.accelerationInputState.config(
            text="Current acceleration state: " + self.agent.body.getAccelerationSensorData()[1].name)

        self.agentHeadMovementName.config(text="Current head height (%): " + str(self.agent.body.getFeelerPosition()))
        self.headProgressValue.set(self.agent.body.getFeelerPosition())

        self.storyArcName.config(text="Current story arc: " + StoryArc(self.agent.mind.currentStoryArcIndex).name)

        self.applicationGUI.update_idletasks()
        self.applicationGUI.after(10, self.applicationMainLoop)  # reschedule event

    @staticmethod
    def translate(value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)

    def on_closing(self):
        if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
            self.agent = None  # allows the cleanup of GPIO pins
            self.applicationGUI.destroy()

    def switchApplicationMode(self,console, applicationModeState):

        self.agent.body.toggleApplicationMode()
        applicationModeState.configure(text="Current application mode: " + self.agent.body.applicationMode.name)

        console.insert('1.0', "Switched application mode to: " + self.agent.body.applicationMode.name + "\n")

        return

    # NOTE: for testing purposes only - wrapper function
    def updateAccelerationInput(self, console, accelerationInputState):

        def executeBehavior(value):

            if self.agent.body.applicationMode == ApplicationMode.AUTONOMOUS:
                console.insert('1.0', "Application in autonomous mode - input locked \n")
                return

            if value == "Fast":
                newAccelerationState = Acceleration.FAST
            else:
                newAccelerationState = Acceleration.SLOW

            self.agent.body.accelerationState = newAccelerationState
            accelerationInputState.configure(text="Current acceleration state: " + self.agent.body.getAccelerationSensorData()[1].name)

            console.insert('1.0', "Switched acceleration mode to: " + self.agent.body.getAccelerationSensorData()[
                1].name + "\n")

        return executeBehavior

    # NOTE: for testing purposes only - wrapper function
    def updateTouchInput(self, console, touchInputState):

        def executeBehavior(value):

            if self.agent.body.applicationMode == ApplicationMode.AUTONOMOUS:
                console.insert('1.0', "Application in autonomous mode - input locked \n")
                return

            if value == "Touching":
                newTouchState = Touch.TOUCHING
            else:
                newTouchState = Touch.NOT_TOUCHING

            self.agent.body.touchState = newTouchState
            touchInputState.configure(text="Current touch state: " + self.agent.body.getTouchSensorData()[1].name)

            console.insert('1.0', "Switched touch mode to: " + self.agent.body.getTouchSensorData()[1].name + "\n")

        return executeBehavior

    # NOTE: to draw the shapes on the canvas

    def b1down(self, event):
        self.b1 = "down"  # you only want to draw when the button is down
        # because "Motion" events happen -all the time-

    def b1up(self, event):
        self.b1 = "up"
        self.xold = None  # reset the line when you let go of the button
        self.yold = None

        self.agent.body.opticalState = Optical.FINISHED
        event.widget.delete("all")

    def motion(self, event):

        if self.b1 == "down":
            if self.xold is not None and self.yold is not None and event.x is not None and event.y is not None:
                event.widget.create_line(self.xold, self.yold, event.x, event.y, smooth=TRUE)
                # here's where you draw it. smooth. neat.
                self.agent.body.newOpticalInfo = (event.x, event.y)
                self.agent.body.opticalState = Optical.RECEIVING
                #print("info sent: " + str(self.agent.body.newOpticalInfo))

            self.xold = event.x
            self.yold = event.y
