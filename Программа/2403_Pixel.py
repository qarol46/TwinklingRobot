from neopixel import NeoPixel

NUM_OF_LED = 3
np = NeoPixel(Pin(13), NUM_OF_LED)

for i in range(32):
    np[i] = (i * 8, 0, 0)