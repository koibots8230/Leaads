from machine import Pin, SPI
from time import sleep
from neopixel import NeoPixel 
#https://docs.micropython.org/en/latest/library/neopixel.html

ledpin = Pin(5, Pin.OUT)

lilad = Pin(16, Pin.OUT)

numleds = 30

red = (128,0,0)
green = (0,128,0)
blue = (0,0,128)
off = (0,0,0)
orange = (255,50,0)
purple = (100,0,127)


pina = Pin(8, Pin.IN, Pin.PULL_UP)
pinb = Pin(7, Pin.IN, Pin.PULL_UP)
pinc = Pin(6, Pin.IN, Pin.PULL_UP)

def read_pins():
    num = 0
    if not pina.value():
        num += 1
    if not pinb.value():
        num += 2
    if not pinc.value():
        num += 4
    return num    

#you need an even number of leds to work
class Snek:
    def __init__(self,neo):
        self.neo = neo
    
    def execute(self):
        self.neo.fill(purple)
        self.neo.write()
        hlfway = int(numleds/2)
        for i in range(0,hlfway):
            self.neo[i+hlfway] = green
            self.neo[hlfway-(i+1)] = green
            self.neo.write()
            sleep(.05)
        for i in range(0,hlfway):
            self.neo[i] = purple
            self.neo[numleds-(i+1)]= purple
            self.neo.write()
            sleep(.05)
            

class ShowOff:
   
   def __init__(self,neo):
        self.neo = neo
        
   def execute(self):
       self.neo.fill(orange)
       self.neo.write()
       for i in range(numleds):
            sleep(.05)
            if i > 0:
                self.neo[i-1] = orange
            self.neo[i] = purple
            self.neo.write()
        
class SummonThePlayers:
    
    def __init__(self,neo):
        self.neo = neo
     
    @staticmethod
    def scale(num):
        return int(num**3/256**2)
    
    def execute(self):
        for i in range(0,256,4):
            self.neo.fill((0,self.scale(i),self.scale(i)))
            self.neo.write()
            sleep(0.01)
        for i in range(255,-1,-4):
            self.neo.fill((0,self.scale(i),self.scale(i)))
            self.neo.write()
            sleep(0.002)
   
    def stop(self):
        self.neo.fill(off)
        self.neo.write()


class OffCommand:
    def __init__(self,neo):
        self.neo = neo
    
    def execute(self):
        self.neo.fill(off)
        self.neo.write()

neo = NeoPixel(ledpin, numleds)
haha = NeoPixel(lilad, 1)
showoff_cmd = ShowOff(neo)
summon_cmd = SummonThePlayers(neo)
snek_cmd = Snek(neo)
off_cmd = OffCommand(neo)


ALL_CMDS = {
    0: off_cmd,
    1: showoff_cmd,
    2: summon_cmd,
    3: snek_cmd,
}

try:
    while True:
        cmd = read_pins()
        print("you been got, command"+str(cmd))
        if cmd in ALL_CMDS:
            ALL_CMDS[cmd].execute()
        sleep(.125)
        
finally:
    neo.fill(off)
    neo.write()
    haha[0]= (off)
    haha.write()
    
    