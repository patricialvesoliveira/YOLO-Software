import numpy

import RPi.GPIO as GPIO
import os
import time

from Scripts.Utilities import Utilities

from neopixel import *
from Libs.Constants import *

# # LED strip configuration:
# LED_COUNT = 15  # Number of LED pixels.
# LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
# LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
# LED_DMA = 10  # DMA channel to use for generating signal (Between 1 and 14)
# LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
# LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
# LED_CHANNEL = 0  # PWM 0 or 1
# LED_TYPE = ws.WS2811_STRIP_GRB  # This type is for WS2811 GRB, must be matched with strip but it works. Check the Neopixel library for codes


# LED strip configuration:
LED_COUNT      = 15      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_TYPE      = ws.WS2811_STRIP_RGB   # Strip type and colour ordering


# NOTE: Two LED devices must have different DMA and PWM channels to work!!!!
# Another NOTE: Sometimes LEDs behave weirdly with the correct LED count but when more LEDs than those present on the strip are
# provided it starts behaving as expected (eg. strip had 12 I gave it 15 it behaved normally -- still don't know why this happens)
class LEDActuator:
    def __init__(self):
        # Create NeoPixel object with appropriate configuration.
        # Note: the jewel has a configuration of GRB
        self.leds = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_TYPE)
        # Initialize the library (must be called once before other functions).
        self.leds.begin()

        # init leds with a white color
        # for i in range(0, self.leds.numPixels(), 1):
        #     self.setColor(1,1,1);

        # self.leds.show()

        print "OK! -- Jewel LEDs set up!"

    def __del__(self):

        for i in range(0, self.leds.numPixels(), 1):
            self.leds.setPixelColor(i, Color(0, 0, 0))
        self.leds.show()

        print "Turning off the Jewel's LEDs"

    # Note: Don't change the setColor functions just the RGB specs for each strip
    def setColor(self, red, green, blue):

        #Note: I separate the color into its channel to avoid confusing between the Color module I was using and the one defined by NeoPixel
        red = Utilities.changeScale(red, 0, 1, 0, 255)
        green = Utilities.changeScale(green, 0, 1, 0, 255)
        blue = Utilities.changeScale(blue, 0, 1, 0, 255)

        # cleaning up any imprecision
        red = numpy.clip(red, 0, 255)
        green = numpy.clip(green, 0, 255)
        blue = numpy.clip(blue, 0, 255)

        color = Color(int(red), int(green), int(blue));

        # self.printColor(color)

        # Note: the jewel has a configuration of GRB
        for i in range(0, self.leds.numPixels(), 1):
            self.leds.setPixelColor(i, color)
        self.leds.show()

    def setBrightness(self, brightness):
        self.leds.setBrightness(int(brightness))
        self.leds.show()

    def printColor(self, ledColorData):
        blue = 255 & ledColorData
        green = ((255 << 8) & ledColorData) >> 8
        red = ((255 << 16) & ledColorData) >> 16

        print "Jewel LEDs color: " + str(red) + ", " + str(green) + ", " + str(blue)
