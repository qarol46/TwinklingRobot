from neopixel import NeoPixel
from machine import Pin

NUM_OF_LED = 3
np = NeoPixel(Pin(25), NUM_OF_LED)

while(1):
    np[0]=(0,0,255)
    np.write()