from machine import Pin
from utime import sleep
from neopixel import NeoPixel
from pimoroni import RGBLED
from plasma import plasma2040

off = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 50, 0)
green = (0, 255, 0)
teal = (0, 139, 139)
blue = (0, 0, 255)
purple = (100, 0, 127)
white = (255, 255, 255)
sleep_duration = 1.0
num_led = 21
#they are tuples which cannot be changed

switch_a = Pin(12, Pin.IN, Pin.PULL_UP)
led_pin = Pin(15,Pin.OUT)
neo_out = NeoPixel(led_pin, num_led, 3)


def snek_forward():
    for i in range(num_led): 
        neo_out[i] = purple
        neo_out.write()
        sleep(sleep_duration)
        neo_out[i] = off
        neo_out.write()
        
def snek_backward():
    for i in range(num_led -1, -1, -1):
        neo_out[i] = blue
        neo_out.write()
        sleep(sleep_duration)
        neo_out[i] = off
        neo_out.write()

def blinking_forward():
    for i in range(num_led): #Blinking
        neo_out[i] = teal
        neo_out.write()
        sleep(sleep_duration)
        neo_out.write()
        neo_out[i] = off
        neo_out.write()
        sleep(sleep_duration)
        
def rainbow_forward():
    for i in range(num_led):
        neo_out[i] = red
        sleep(sleep_duration)
        neo_out.write()
            
    for i in range(num_led):
        neo_out[i] = orange
        sleep(sleep_duration)
        neo_out.write()
            
    for i in range(num_led):
        neo_out[i] = green
        sleep(sleep_duration)
        neo_out.write()
            
    for i in range(num_led):
        neo_out[i] = blue
        sleep(sleep_duration)
        neo_out.write()
            
    for i in range(num_led):
        neo_out[i] = purple
        sleep(sleep_duration)
        neo_out.write()
            
    for i in range(num_led):
        neo_out[i] = white
        sleep(sleep_duration)
        neo_out.write()

def rainbow_blinking_forward():
     for i in range(num_led):
        neo_out[i] = red
        neo_out.write()
        neo_out[i] = off
        sleep(sleep_duration)
        neo_out.write()
            
        neo_out[i] = orange
        neo_out.write()
        neo_out[i] = off
        sleep(sleep_duration)
        neo_out.write()
            
        neo_out[i] = green
        neo_out.write()
        neo_out[i] = off
        sleep(sleep_duration)
        neo_out.write()
            
        neo_out[i] = blue
        neo_out.write()
        neo_out[i] = off
        sleep(sleep_duration)
        neo_out.write()
            
        neo_out[i] = purple
        neo_out.write()
        neo_out[i] = off
        sleep(sleep_duration)
        neo_out.write()

patterns = {
    0: snek_forward,
    1: snek_backward,
    2: blinking_forward,
    3: rainbow_forward,
    4: rainbow_blinking_forward
}

try:

    counter = 0
    while True:        
        
        if switch_a.value() == 0:
            counter += 1
            if counter >= len(patterns):
               counter = 0
        
        patterns[counter]()
        
finally:
    neo_out.fill(off)
    neo_out.write()




    # Setup the RGB Led
# led = RGBLED(16, 17, 18)
# 
# sleep_duration = 1
# 
# try:
#     # Cycle through RGB (Red, Green, Blue)
#     while True:
#         led.set_rgb(255, 0, 20)
#         sleep(sleep_duration)
#         
#         led.set_rgb(0, 205, 66)
#         sleep(sleep_duration)
#         
#         led.set_rgb(33, 44, 0)
#         sleep(sleep_duration)
#         
#         led.set_rgb(255, 50, 0)
#         sleep(sleep_duration)
#         
#         led.set_rgb(255, 0, 255)
#         sleep(sleep_duration)
#         
#         
# except:
#     # do
#     pass
# 
# finally:
#     led.set_rgb(0, 0, 0)