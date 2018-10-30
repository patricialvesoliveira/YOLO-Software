"""
Script to record mouse movements to obtain Training data.
This uses pygame to record the x,y co-ordinates relative to screen based on mouse movements.
This assumes the figure drwan are closed figures and considers two events
with the difference of mouse up and down as independant.
"""
import argparse
import pygame, random
import lib.util
from scripts.OpticalSensor import *
from scripts.TouchSensor import *
from lib.constants import *


def roundline(srf, color, start, end, radius=1):
    dx = end[0]-start[0]
    dy = end[1]-start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance): 
        x = int( start[0]+float(i)/distance*dx)
        y = int( start[1]+float(i)/distance*dy)
        pygame.draw.circle(srf, color, (x, y), radius)

def trainModelComputer(shape):
    screen = pygame.display.set_mode((800,600))
    draw_on = False
    last_pos = (0, 0)
    color = (255, 128, 0)
    radius = 10
    f = open(NEW_TRAINING_LOCATION, 'a+')
    arr = []

    try:
        while True:
            e = pygame.event.wait()
            if e.type == pygame.QUIT:
                raise StopIteration
            if e.type == pygame.MOUSEBUTTONDOWN:
                # color = (random.randrange(256), random.randrange(256), random.randrange(256))
                color = (255,255,255)
                pygame.draw.circle(screen, color, e.pos, radius)
                draw_on = True
            if e.type == pygame.MOUSEBUTTONUP:
                draw_on = False
                arr.append(shape)
                f.write(str(arr)+'\n')
                arr[:] = []
                break
            if e.type == pygame.MOUSEMOTION:
                if draw_on:
                    pygame.draw.circle(screen, color, e.pos, radius)
                    roundline(screen, color, e.pos, last_pos,  radius)
                    arr.append(e.pos)
                last_pos = e.pos
            pygame.display.flip()

    except StopIteration:
        pass

    pygame.quit()

def trainModelRobot(shape):

    # to detect start and stop of shape
    touchSensor = TouchSensor()
    opticalSensor = OpticalSensor()

    startedRecordingShape = False
    oldSensorPosition = [-1, -1]
    currentSensorPosition = [0, 0]
    finalShape = []

    trainingLocationFile = open(NEW_TRAINING_LOCATION, 'a+')

    while True:

        if not startedRecordingShape and touchSensor.isBeingTouched():
            startedRecordingShape = True
            print "Started recording the shape!"

        if startedRecordingShape and touchSensor.isBeingTouched():

            resultList = []
            for eventList in opticalSensor.getEvents():
                if eventList is not None:
                    resultList = eventList

            for event in resultList:
                if event[0] == "xCoordinate":
                    currentSensorPosition[0] = currentSensorPosition[0] + int(event[1])
                elif event[0] == "yCoordinate":
                    currentSensorPosition[1] = currentSensorPosition[1] + int(event[1])

            if currentSensorPosition != oldSensorPosition: 
                #print "Adding point " + str(currentSensorPosition)
                finalShape.append((int(currentSensorPosition[0]), int(currentSensorPosition[1])))
                oldSensorPosition[0] = currentSensorPosition[0]
                oldSensorPosition[1] = currentSensorPosition[1]


        if startedRecordingShape and not touchSensor.isBeingTouched():
            
            finalShape.append(shape)
            trainingLocationFile.write(str(finalShape)+"\n")

            print "Finished recognizing the \"" + shape + "\" shape!"
            print "- " + str(len(finalShape)) + " datapoints recorded for \"rect\""
            #print "- " + str(len(finalShape)) + " datapoints recorded for \"rect\": " + str(finalShape)

            return


def main(version):
    
    print ""
    behaviorChoice = str(raw_input("What do you want to do? \n To compute and cache features (Data should be at: " + TRAINING_LOCATION + ") : 1 \n To store new data to train model (Storing data at: " + NEW_TRAINING_LOCATION + "): 2 \n -- "))

    if behaviorChoice == "1":
        print ""
        lib.util.cacheFeatures()
        print "Features successfully cached to location \"" + CACHE_LOCATION + "\" from data in \"" + TRAINING_LOCATION + "\"."
        exit()
    elif behaviorChoice == "2":
        print ""
        shape = str(raw_input("Enter shape (should match the ones expected by the Yolo Agent code -- spikes, curved, straight, rect, loops):\n"))
        if version == "pc":
            trainModelComputer(shape)
        elif version == "robot":
            trainModelRobot(shape)
        else:
            print "Error: unsupported version introduced!"
            return
        print ""
        print "New data item recorded to location \"" + NEW_TRAINING_LOCATION + "\". Move to \"" + TRAINING_LOCATION + "\" to cache features before running algorithm."
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Agent startup')
    parser.add_argument('--version', metavar='string', default="pc", help='The mode of execution (pc or robot). Dev requires a display either directly connected or using  X11 through SSH. Default is Dev)')
    args = parser.parse_args()
    main(version=args.version)
