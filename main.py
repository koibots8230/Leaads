from machine import Pin, SPI
from utime import sleep
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


def off_handler(off_cmd, all_cmds):
   
    print('Turning active=False')
    for mycmd in all_cmds.values():
        mycmd.active = False
       
    sleep(1)
    off_cmd.execute()
   

#you need an even number of leds to work
class Snek:
    def __init__(self,neo):
        self.neo = neo
        self.active = False
   
    def execute(self):
       
        self.active = True

        self.neo.fill(purple)
        self.neo.write()
        hlfway = int(numleds/2)
        for i in range(0,hlfway):
            if self.active is False:
                break
            self.neo[i+hlfway] = green
            self.neo[hlfway-(i+1)] = green
            self.neo.write()
            sleep(.05)
           
        for i in range(0,hlfway):
            if self.active is False:
                break
            self.neo[i] = purple
            self.neo[numleds-(i+1)]= purple
            self.neo.write()
            sleep(.05)
           

class ShowOff:
   
   def __init__(self,neo):
        self.neo = neo
        self.active = False
       
   def execute(self):

        self.active = True
       
        self.neo.fill(orange)
        self.neo.write()
        for i in range(numleds):
            if self.active is False:
                break
            if i > 0:
                self.neo[i-1] = orange
            self.neo[i] = purple
            self.neo.write()
            sleep(.05)
       
class SummonThePlayers:
   
    def __init__(self,neo):
        self.neo = neo
        self.active = False
     
    @staticmethod
    def scale(num):
        return int(num**3/256**2)
   
    def execute(self):

        self.active = True
       
        for i in range(0,256,4):
            if self.active is False:
                break
            self.neo.fill((0,self.scale(i),self.scale(i)))
            self.neo.write()
            sleep(0.01)
           
        for i in range(255,-1,-4):
            if self.active is False:
                break
            self.neo.fill((0,self.scale(i),self.scale(i)))
            self.neo.write()
            sleep(0.002)


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
    4: snek_cmd
}


pind.irq(trigger=Pin.IRQ_RISING, handler=lambda p: off_handler(off_cmd, ALL_CMDS))

try:
    haha[0] = (red)
    haha.write()

    while True:
     
        cmd = read_pins()
        if cmd in ALL_CMDS:
            print("you been got, command", cmd)
            haha[0] = (green)
            haha.write()
            off_handler(off_cmd, ALL_CMDS)
            ALL_CMDS[cmd].execute()
        elif cmd == 0:
            for mycmd in ALL_CMDS.values():
                if mycmd.active is True:
                    mycmd.execute()
                    break
           
        haha[0] = (red)
        haha.write()
       
        sleep(.125)
       
finally:
    neo.fill(off)
    neo.write()
    haha[0]= (off)
    haha.write()
