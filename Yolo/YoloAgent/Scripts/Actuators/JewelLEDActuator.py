import RPi.GPIO as GPIO
import os
import time
from neopixel import *
from Libs.Constants import *


# LED strip configuration:
LED_COUNT = 15  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (Between 1 and 14)
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_CHANNEL = 0  # PWM 0 or 1
LED_TYPE = ws.WS2811_STRIP_GRB  # This type is for WS2811 GRB, must be matched with strip but it works. Check the Neopixel library for codes


# NOTE: Two LED devices must have different DMA and PWM channels to work!!!!
# Another NOTE: Sometimes LEDs behave weirdly with the correct LED count but when more LEDs than those present on the strip are
# provided it starts behaving as expected (eg. strip had 12 I gave it 15 it behaved normally -- still don't know why this happens)
class JewelLEDActuator:
    def __init__(self):
        # Create NeoPixel object with appropriate configuration.
        # Note: the jewel has a configuration of GRB
        self.leds = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_TYPE)
        # Initialize the library (must be called once before other functions).
        self.leds.begin()

        for i in range(0, self.leds.numPixels(), 1):
            self.leds.setPixelColor(i, Color(0, 0, 0))

        self.leds.show()

        print "OK! -- Jewel LEDs set up!"

    def __del__(self):

        for i in range(0, self.leds.numPixels(), 1):
            self.leds.setPixelColor(i, Color(0, 0, 0))
        self.leds.show()

        print "Turning off the Jewel's LEDs"

    # Note: Don't change the setColor functions just the RGB specs for each strip
    def setColor(self, red, green, blue):

        # Note: the jewel has a configuration of GRB
        for i in range(0, self.leds.numPixels(), 1):
            self.leds.setPixelColor(i, Color(int(red), int(green), int(blue)))
        self.leds.show()

        #self.printColor(self.leds.getPixelColor(0))

    def setBrightness(self, brightness):

        self.leds.setBrightness(int(brightness))
        self.leds.show()

    def performColorDisplay(self):
        for i in range(0, self.leds.numPixels(), 1):
            self.leds.setPixelColor(i, Color(255, 0, 0))
        self.leds.show()
        self.printColor(self.leds.getPixelColor(0))
        time.sleep(1)

        for i in range(0, self.leds.numPixels(), 1):
            self.leds.setPixelColor(i, Color(0, 255, 0))
        self.leds.show()
        self.printColor(self.leds.getPixelColor(0))
        time.sleep(1)

        for i in range(0, self.leds.numPixels(), 1):
            self.leds.setPixelColor(i, Color(0, 0, 255))
        self.leds.show()
        self.printColor(self.leds.getPixelColor(0))
        time.sleep(1)

    def printColor(self, ledColorData):
        blue = 255 & ledColorData
        green = ((255 << 8) & ledColorData) >> 8
        red = ((255 << 16) & ledColorData) >> 16

        print "Jewel LEDs color: " + str(red) + ", " + str(green) + ", " + str(blue)
