from machine import Pin, UART
from time import sleep
from machine import Pin
from neopixel import NeoPixel
from pimoroni import RGBLED
from plasma import plasma2040

off: tuple[int, int, int] = (0, 0, 0)
purple: tuple[int, int, int] = (100, 0, 127)
orange: tuple[int, int, int] = (255, 50, 0)


num_leds: int = 21
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
def all_color(color: tuple[int, int, int]) -> list[list[tuple[int, int, int]]]:
    result = []
    frame: list[tuple[int, int, int]] = [color]*num_leds
    result.append(frame)
    
    return result               
                
def all_off():
    return all_color(off)

def all_orange():
    return all_color(orange)

def all_purple():
    return all_color(purple)

def orange_purple_gradient_long() -> list[list[tuple[int, int, int]]]:

    frame: list[tuple[int, int, int]] = interpolate(scarlet, purple, num_leds)
        
    return [frame]

def rainbow_gradient_long() -> list[list[tuple[int, int, int]]]:
    frame = [off] * num_leds
    frame[0] = green
    frame[halfway] = red
    frame[-1] = teal
    
    first_half: list[tuple[int, int, int]] = interpolate(frame[0], frame[halfway], halfway)
    second_half = interpolate(frame[halfway], frame[-1], halfway)
    
    for idx, led_color in enumerate(first_half):
        frame[idx] = led_color
        
    for idx, led_color in enumerate(second_half):
        frame[idx + halfway] = led_color
        


patterns = {
    b"0": (all_off, 0.10),
    b"1": (all_orange, 0.10),
    b"2": (all_purple, 0.10),
    b"3": (orange_purple_gradient_long, 0.01),
    b"4": (rainbow_gradient_long, 0.01),
    b"5": (, 0.3),
    b"6": (, 0.01),
    b"7": (, 0.01),
    b"8": (, 0.05),
    b"9": (, 0.4)
}

switch_a = Pin(12, Pin.IN, Pin.PULL_UP)
led_pin = Pin(15,Pin.OUT)
neo_out = NeoPixel(led_pin, num_leds, 3)

uart = UART(1, 9600, tx=Pin(10), rx=Pin(9), timeout = 1)

animator = Animator(neo_out)

try:

    while True:
        selection = uart.read(1)
        
        if selection in patterns:
            frames_function, sleep_duration = patterns[selection]
            animator.set_animation(frames_function(), sleep_duration)
        
                
        animator.advance()
        
finally:
    neo_out.fill(off)
    neo_out.write()
    

