from machine import Pin, SPI
from time import sleep
from neopixel import NeoPixel 
#https://docs.micropython.org/en/latest/library/neopixel.html

ledpin = Pin(5, Pin.OUT)

lilad = Pin(16, Pin.OUT)

numleds = 80

red = (128,0,0)
green = (0,128,0)
blue = (0,0,128)
off = (0,0,0)
orange = (255,50,0)
purple = (100,0,127)


pina = Pin(29, Pin.IN, Pin.PULL_DOWN)
pinb = Pin(28, Pin.IN, Pin.PULL_DOWN)
pinc = Pin(27, Pin.IN, Pin.PULL_DOWN)
pind = Pin(26, Pin.IN, Pin.PULL_DOWN)

def read_pins():
    num = 0
    if pina.value():
        num += 1
    if pinb.value():
        num += 2
    if pinc.value():
        num += 4
    if pind.value():
        num += 8
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
    1: showoff_cmd,
    2: summon_cmd,
    4: snek_cmd,
}

try:
    haha[0] = red
    haha.write()
    cur_cmd = -1
    while True:
    
        cmd = read_pins()
        if cmd > 0 and cmd not in ALL_CMDS:
            print("you been off'd, command"+str(cmd))
            cur_cmd = -1
            off_cmd.execute()
        elif cmd in ALL_CMDS:
            print("you been got, command"+str(cmd))
            cur_cmd = cmd
            ALL_CMDS[cmd].execute()
        elif cur_cmd > 0:
            ALL_CMDS[cur_cmd].execute()
        else:
            off_cmd.execute()
           
        sleep(.125)
        
finally:
    neo.fill(off)
    neo.write()
    haha[0]= (off)
    haha.write()
    
    