import numpy
import RPi.GPIO as GPIO
from neopixel import *
from Core.Enumerations import *

# LED strip configuration:
LED_COUNT      = 15      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_TYPE       = ws.SK6812_STRIP_RGBW   # Strip type and colour ordering

# NOTE: Two LED devices must have different DMA and PWM channels to work!!!!
# Another NOTE: Sometimes LEDs behave weirdly with the correct LED count but when more LEDs than those present on the strip are
# provided it starts behaving as expected (eg. strip had 12 I gave it 15 it behaved normally -- still don't know why this happens)
class LEDActuator:
    def __init__(self):
        # Create NeoPixel object with appropriate configuration.
        # Note: the jewel has a configuration of GRB
        self.leds = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_TYPE)
        self.leds.begin()
        self.setColor( 0, 0, 0)
        self.leds.setBrightness(0)
        print "OK! -- Jewel LEDs set up!"

    def __del__(self):
        print "LED Actuator cleanup successful!"

    # Don't change the setColor functions just the RGB specs for each strip
    def setColor(self, green, red, blue):
        red = self.changeColorScale(red, 0, 1, 0, 255)
        green = self.changeColorScale(green, 0, 1, 0, 255)
        blue = self.changeColorScale(blue, 0, 1, 0, 255)

        # cleaning up any imprecision
        red = numpy.clip(red, 0, 255)
        green = numpy.clip(green, 0, 255)
        blue = numpy.clip(blue, 0, 255)

        color = Color(int(red), int(green), int(blue));

        # Note: the jewel has a configuration of GRB
        for i in range(0, self.leds.numPixels(), 1):
            self.leds.setPixelColor(i, color)
        self.leds.show()

    def setBrightness(self, brightness):
        self.leds.setBrightness(int(brightness))
        self.leds.show()


    def changeColorScale(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)

    def printColor(self, ledColorData):
        blue = 255 & ledColorData
        green = ((255 << 8) & ledColorData) >> 8
        red = ((255 << 16) & ledColorData) >> 16
        print "Jewel LEDs color: " + str(red) + ", " + str(green) + ", " + str(blue)