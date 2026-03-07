from machine import Pin, UART
from time import sleep
from machine import Pin
from neopixel import NeoPixel
#from pimoroni import RGBLED
from plasma import plasma2040
#import plasma

off: tuple[int, int, int] = (0, 0, 0)
scarlet: tuple[int, int, int] = (237, 33, 0)
purple: tuple[int, int, int] = (100, 0, 127)
white: tuple[int, int, int] = (255, 255, 355)

num_leds: int = 40
halfway = int(num_leds/2)
interpolation_factor = 5
#they are tuples which cannot be changed


def interpolate(start_color: tuple[int, int, int], end_color: tuple[int, int, int], steps: int) -> list[tuple[int, int, int]]:
    result = [white]*steps
    result[0] = start_color
    result[-1] = end_color
    red_slope = (end_color[0] - start_color[0])/steps
    green_slope = (end_color[1] - start_color[1])/steps
    blue_slope = (end_color[2] - start_color[2])/steps
    
    for indx in range(steps - 2):
        result_indx = indx + 1
        result_red = red_slope * result_indx + start_color[0]
        result_green = green_slope * result_indx + start_color[1]
        result_blue = blue_slope * result_indx + start_color[2]
        result[result_indx] = (int(result_red), int(result_green), int(result_blue))  
    
    return result


class Animator:
    pixels: NeoPixel
    frames: list[list[tuple[int,int,int]]]
    current_frame_idx: int

    sleep_duration: int

    def __init__(self, pixels: NeoPixel):
        self.pixels = pixels
        self.current_frame_idx = 0
        self.frames = []
        self.sleep_duration = 1.0

    def set_animation(self, frames: list[list[tuple[int,int,int]]], sleep_duration: float):
        
        if self.frames != frames:
            self.current_frame_idx = 0
            self.frames = frames
        self.sleep_duration = sleep_duration
        
    def get_current_frame(self):
        return self.frames[self.current_frame_idx]

    def advance(self):
        """
        Update the LEDs to the next frame
        """
        if len(self.frames) > 0:
        
            for idx, led in enumerate(self.get_current_frame()):
                self.pixels[idx] = led

            self.pixels.write()
            
            if len(self.frames) > 1:
                sleep(self.sleep_duration)
                self.current_frame_idx += 1

                # Check for current frame getting larger than our array
                if self.current_frame_idx >= len(self.frames):
                    self.current_frame_idx = 0
                

def orange_purple_gradiant_run() -> list[list[tuple[int, int, int]]]:
    result = []
    frame = [off] * num_leds
    frame[0] = scarlet
    frame[-1] = purple
    
    first_half: list[tuple[int, int, int]] = interpolate(frame[0], frame[-1], num_leds)
    
    for idx, led_color in enumerate(first_half):
        frame[idx] = led_color
        
    result.append(frame)
    
    cur_frame = frame.copy()    
    for _ in range(num_leds - 1):
        cur_frame.insert(0, cur_frame.pop(-1))
        result.append(cur_frame)
        cur_frame = cur_frame.copy()
        
    
    return result


#switch_a = Pin(12, Pin.IN, Pin.PULL_UP)
led_pin1 = Pin(15,Pin.OUT)
led_pin2 = Pin(26, Pin.OUT)
led_strip1 = NeoPixel(led_pin1, num_leds, bpp = 3)
led_strip2 = NeoPixel(led_pin2, num_leds, bpp =  3)
## bpp is for rgb LEDs because its three and rgb has three in its name ;)

animator1 = Animator(led_strip1)
animator2 = Animator(led_strip2)


try:
    
    frames = orange_purple_gradiant_run()
    sleep_duration = .07
    
    while True:
               
        animator1.set_animation(frames, sleep_duration)
        animator2.set_animation(frames, sleep_duration)

                
        animator1.advance()
        animator2.advance()
      
finally:
    led_strip1.fill(off)
    led_strip2.fill(off)
    led_strip1.write()
    led_strip2.write()

    