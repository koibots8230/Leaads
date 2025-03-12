from machine import Pin, UART
from time import sleep
from machine import Pin
from neopixel import NeoPixel
from pimoroni import RGBLED
from plasma import plasma2040

off: tuple[int, int, int] = (0, 0, 0)
red: tuple[int, int, int] = (255, 0, 0)
orange: tuple[int, int, int] = (255, 50, 0)
green = (0, 255, 0)
teal = (0, 139, 139)
blue = (0, 0, 255)
purple: tuple[int, int, int] = (100, 0, 127)
white = (255, 255, 255)
num_leds: int = 40
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
                
                
def all_off():
    result = []
    frame: list[list[tupl[int, int, int]]] = [off]*num_leds
    result.append(frame)
    
    return result

def snek_forward_backward() -> list[list[tuple[int, int, int]]]:
    result: list[list[tuple[int, int, int]]] = []
    
    for i in range(0, num_leds):
        frame: list[tuple[int, int, int]] = [off]*num_leds
        frame[i] = purple
        result.append(frame)
    
    for i in range(num_leds - 1, -1, -1):
        frame: list[tuple[int, int, int]] = [off]*num_leds
        frame[i] = orange
        result.append(frame)
    
    return result

def all_teal() -> list[list[tuple[int, int, int]]]:
    result = []
    frame: list[tuple[int, int, int]] = [teal]*num_leds
    result.append(frame)
    
    return result

def all_red() -> list[list[tuple[int, int, int]]]:
    result = []
    frame: list[tuple[int, int, int]] = [red]*num_leds
    result.append(frame)
    
    return result

def all_orange() -> list[list[tuple[int, int, int]]]:
    result = []
    frame: list[tuple[int, int, int]] = [orange]*num_leds
    result.append(frame)
    
    return result

def all_green() -> list[list[tuple[int, int, int]]]:
    result = []
    frame: list[tuple[int, int, int]] = [green]*num_leds
    result.append(frame)
    
    return result

def all_blue() -> list[list[tuple[int, int, int]]]:
    result = []
    frame: list[tuple[int, int, int]] = [blue]*num_leds
    result.append(frame)
    
    return result

def all_purple() -> list[list[tuple[int, int, int]]]:
    result = []
    frame: list[tuple[int, int, int]] = [purple]*num_leds
    result.append(frame)
    
    return result

def all_white() -> list[list[tuple[int, int, int]]]:
    result = []
    frame: list[tuple[int, int, int]] = [white]*num_leds
    result.append(frame)
    
    return result

def rainbow_forward() -> list[list[tuple[int, int, int]]]:
    result = []
    for i in range(num_leds):
        frame: list[tuple[int, int, int]] = [off]*num_leds
        frame[i] = red
        result.append(frame)
            
    for i in range(num_leds):
        frame: list[tuple[int, int, int]] = [off]*num_leds
        frame[i] = orange
        result.append(frame)
            
    for i in range(num_leds):
        frame: list[tuple[int, int, int]] = [off]*num_leds
        frame[i] = green
        result.append(frame)
            
    for i in range(num_leds):
        frame: list[tuple[int, int, int]] = [off]*num_leds
        frame[i] = teal
        result.append(frame)
        
    for i in range(num_leds):
        frame: list[tuple[int, int, int]] = [off]*num_leds
        frame[i] = blue
        result.append(frame)
            
    for i in range(num_leds):
        frame: list[tuple[int, int, int]] = [off]*num_leds
        frame[i] = purple
        result.append(frame)
        
    for i in range(num_leds):
        frame: list[tuple[int, int, int]] = [off]*num_leds
        frame[i] = white
        result.append(frame)
    
    return result 

def rainbow_blinking_forward() -> list[list[tuple[int, int, int]]]:
    result = []
    
    frame: list[tuple[int, int, int]] = [red]*num_leds
    result.append(frame)
    result.append([off]*num_leds)
        
    frame: list[tuple[int, int, int]] = [orange]*num_leds
    result.append(frame)
    result.append([off]*num_leds)
            
    frame: list[tuple[int, int, int]] = [green]*num_leds
    result.append(frame)
    result.append([off]*num_leds)
            
    frame: list[tuple[int, int, int]] = [teal]*num_leds
    result.append(frame)
    result.append([off]*num_leds)

    frame: list[tuple[int, int, int]] = [blue]*num_leds
    result.append(frame)
    result.append([off]*num_leds)

    frame: list[tuple[int, int, int]] = [purple]*num_leds
    result.append(frame)
    result.append([off]*num_leds)

    frame: list[tuple[int, int, int]] = [white]*num_leds
    result.append(frame)
    result.append([off]*num_leds)

    return result

def all_rainbow_gradient() -> list[list[tuple[int, int, int]]]:
    result = []
    frame: list[tuple[int, int, int]] = [red]*num_leds
    result.append(frame)
    
    red_to_orange = interpolate(red, orange, interpolation_factor)  
    for color in red_to_orange:
        result.append([color]*num_leds)

    frame: list[tuple[int, int, int]] = [orange]*num_leds
    result.append(frame)
    
    orange_to_green = interpolate(orange, green, interpolation_factor*2)  
    for color in orange_to_green:
        result.append([color]*num_leds)
    
    frame: list[tuple[int, int, int]] = [green]*num_leds
    result.append(frame)
    
    green_to_teal = interpolate(green, teal, interpolation_factor)  
    for color in green_to_teal:
        result.append([color]*num_leds)
    
    frame: list[tuple[int, int, int]] = [teal]*num_leds
    result.append(frame)
    
    teal_to_blue = interpolate(teal, blue, interpolation_factor)  
    for color in teal_to_blue:
        result.append([color]*num_leds)
    
    frame: list[tuple[int, int, int]] = [blue]*num_leds
    result.append(frame)
    
    blue_to_purple = interpolate(blue, purple, interpolation_factor)  
    for color in blue_to_purple:
        result.append([color]*num_leds)
    
    frame: list[tuple[int, int, int]] = [purple]*num_leds
    result.append(frame)
    
    purple_to_white = interpolate(purple, white, interpolation_factor)  
    for color in purple_to_white:
        result.append([color]*num_leds)
    
    frame: list[tuple[int, int, int]] = [white]*num_leds
    result.append(frame)
    
    return result

def rainbow_gradient_long():
    halfway = int(num_leds/2)
    result = [off] * num_leds
    result[0] = green
    result[-1] = teal
    result[halfway] = red
    first_half = interpolate(result[0], result[-1], result[halfway])
    
    for led_color in (first_half):
        enumerate(first_half)
        result[led_color] = led_color
        
    for i in led_color:
        result[i, first_half] = led_color

patterns = {
    b"0": (snek_forward_backward, 0.5),
    b"1": (rainbow_blinking_forward, 0.8),
    b"2": (all_rainbow_gradient, 0.10),
    b"3": (all_purple, 1.0),
    b"4": (all_teal, 1.0),
    b"5": (all_orange, 0.10),
    b"6": (all_off, 1.0),
    b"7": (rainbow_gradient_long, 1.0)
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
    