from machine import Pin, Signal 
from time import sleep
from neopixel import NeoPixel

ledpin = Pin(16, Pin.OUT)

neo = NeoPixel(ledpin, 1)

red = (128,0,0)
green = (0,128,0)
blue = (0,0,128)
off = (0,0,0)

def buttn_handler(pina):
    print("button pressed, YIPPEE")

try:
    neo[0] = (red)
    neo.write()

    while True:
    #no not

        # At this point, num is some value
        # between 0..7
            
            
        if num == 0:
            neo[0] = (off)
            neo.write()
        elif num == 1:
            neo[0] = (blue)
            neo.write()



finally:
    neo [0] = (off)
    neo.write()


