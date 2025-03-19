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
scarlet = (237,33,0)
sunset = (250, 95, 85)
fuchsia = (255,0,255)
deep_blue = (0, 83, 219)
dark_pink = (218, 0, 150)
light_blue = (0, 150, 218)
neon_green = (15, 255, 80)
jungle_green = (42, 170, 138)
crimson = (220, 20, 60)
gold = (255, 215, 0)
amaranth = (159, 43, 104)
steel_gray = (113, 121, 126)

num_leds: int = 40
halfway = int(num_leds/2)
interpolation_factor = 5
#they are tuples which cannot be changed

def all_color(color: tuple[int, int, int]) -> list[list[tuple[int, int, int]]]:
    result = []
    frame: list[tuple[int, int, int]] = [color]*num_leds
    result.append(frame)
    
    return result

def breathe_color(color: tuple[int, int, int]) -> list[list[tuple[int, int, int]]]:
    result = []
    
    almost_off_color = (int(color[0]/20), int(color[1]/20), int(color[2]/20))


    breathe_colors: list[tuple[int, int, int]] = interpolate(almost_off_color, color, num_leds)
    
    for my_color in breathe_colors:
        result.append([my_color]*num_leds)
    
    breathe_colors.reverse()
    
    for my_color in breathe_colors:
        result.append([my_color]*num_leds)
    
    return result

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
    return all_color(off)

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

def all_red() -> list[list[tuple[int, int, int]]]:
    return all_color(red)

def all_orange() -> list[list[tuple[int, int, int]]]:
    return all_color(orange)

def all_blue() -> list[list[tuple[int, int, int]]]:
    return all_color(blue)

def all_purple() -> list[list[tuple[int, int, int]]]:
    return all_color(purple)


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

def rainbow_blinking() -> list[list[tuple[int, int, int]]]:
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
        
    
    return [frame]

def rainbow_gradient_long_run() -> list[list[tuple[int, int, int]]]:
    result = []
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
        
    result.append(frame)
    
    cur_frame = frame.copy()    
    for _ in range(num_leds - 1):
        cur_frame.insert(0, cur_frame.pop(-1))
        result.append(cur_frame)
        cur_frame = cur_frame.copy()
        
    
    return result

def orange_purple_gradient_long() -> list[list[tuple[int, int, int]]]:

    frame: list[tuple[int, int, int]] = interpolate(scarlet, purple, num_leds)
        
    return [frame]

def breathe_blue():
    return breathe_color(blue)

def breathe_orange_purple():
    result = []
    
    almost_off_orange = (int(orange[0]/20), int(orange[1]/20), int(orange[2]/20))
    almost_off_purple = (int(purple[0]/20), int(purple[1]/20), int(purple[2]/20))

    breathe_orange: list[tuple[int, int, int]] = interpolate(almost_off_orange, orange, num_leds)
    breathe_purple: list[tuple[int, int, int]] = interpolate(almost_off_purple, purple, num_leds)
    
    for my_color in breathe_orange:
        result.append([my_color]*num_leds)
    
    breathe_orange.reverse()
    
    for my_color in breathe_orange:
        result.append([my_color]*num_leds)
        
    for my_color in breathe_purple:
        result.append([my_color]*num_leds)
    
    breathe_purple.reverse()
    
    for my_color in breathe_purple:
        result.append([my_color]*num_leds)
    
    return result

def blue_fuchsia():
    
    frame: list[tuple[int, int, int]] = interpolate(deep_blue, fuchsia, num_leds)
        
    return [frame]

def breathe_deep_blue():
    return breathe_color(deep_blue)

def orange_flash():
    return breathe_color(orange)

def xander_mode():
    result = []
    
    frame: list[tuple[int, int, int]] = [red]*num_leds
    result.append(frame)
    result.append([off]*num_leds)
    
    
    return result

def purple_green_blue():
    frame = [off] * num_leds
    frame[0] = dark_pink
    frame[halfway] = neon_green
    frame[-1] = light_blue
    
    first_half: list[tuple[int, int, int]] = interpolate(frame[0], frame[halfway], halfway)
    second_half = interpolate(frame[halfway], frame[-1], halfway)
    
    for idx, led_color in enumerate(first_half):
        frame[idx] = led_color
        
    for idx, led_color in enumerate(second_half):
        frame[idx + halfway] = led_color
        
    
    return [frame]

def tada():
    
    result =[]

    
    
    my_colors: list[tuple[int, int, int]] = [
        sunset, red, crimson, blue, orange, purple, gold, teal,
        green, purple, fuchsia, scarlet, amaranth, neon_green,
        jungle_green, deep_blue, dark_pink, steel_gray, orange, deep_blue
]
    
    first_explosion = my_colors.copy()
    
    second_explosion = my_colors.copy()    
    second_explosion.reverse()
    
    for i in range(0, halfway):
        
        frame = [off]*num_leds
        
        for j in range(0, i):
            frame[j] = purple
            frame[-1 - j] = orange
            
        result.append(frame)
    
    explosion = first_explosion + second_explosion
    
    for _ in range(5):
        result.append(explosion[0:num_leds])
        result.append([off]*num_leds)

    first_explosion = my_colors.copy()
    first_explosion.reverse()
    second_explosion = my_colors.copy()
    explosion = first_explosion + second_explosion
    
    for _ in range(5):
        result.append(explosion[0:num_leds])
        result.append([off]*num_leds)

    
    return result
    
patterns = {
    b"0": (all_off, 0.10),
    b"1": (orange_purple_gradient_long, 0.10),
    b"2": (blue_fuchsia, 0.10),
    b"3": (breathe_orange_purple, 0.01),
    b"4": (breathe_blue, 0.01),
    b"5": (all_blue, 0.3),
    b"6": (orange_flash, 0.01),
    b"7": (all_orange, 0.01),
    b"8": (rainbow_gradient_long_run, 0.05),
    b"9": (xander_mode, 0.4),
    b"a": (tada, 0.1)
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
    