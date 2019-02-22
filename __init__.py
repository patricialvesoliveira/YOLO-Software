import logging
import os
import platform
import argparse
import time

from Libs.Constants import *
from Scripts.Agent import Agent

agent = None

def main(personality):
    if platform.system() == "Windows":
        directory = os.path.dirname(os.path.abspath(__file__)) + '\Logging\\'
    else:
        directory = os.path.dirname(os.path.abspath(__file__)) + '/Logging/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    print("Logging directory: " + directory)

    logging.basicConfig(filename= directory + 'AgentYOLO(' + time.strftime("%Y-%m-%d-%H.%M.%S") + ').log', format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info('Agent YOLO startup')

    if personality == "Affective":
        selectedPersonality = PersonalityType.AFFECTIVE
    elif personality == "Aloof":
        selectedPersonality = PersonalityType.ALOOF
    elif personality == "Punk":
        selectedPersonality = PersonalityType.PUNK
    else:
        raise Exception("Error: Chosen personality not found.")

    global agent
    try:
        agent = Agent("YOLO", selectedPersonality)
    except Exception as e:
        print "Error: " + str(e)
        return

    try:
        while True:
            agent.update()
    except KeyboardInterrupt:
        print "Application closed due to user input!"
    except Exception as e:
        print "Error: " + str(e)
    finally:
        agent = None

    # After getting out of the main loop cleanup agent
    agent = None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Agent startup')
    parser.add_argument('--personality', metavar='string', default="Affective", help='The personality the agent will have (Punk, Affective, Aloof). Default is Affective (for testing).')
    # parser.add_argument('--version', metavar='string', default="Dev", help='The mode of execution (Dev or Release). Dev requires a display either directly connected or using  X11 through SSH. Default is Dev)')
    args = parser.parse_args()
    main(personality=args.personality)