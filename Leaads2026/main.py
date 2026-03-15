from machine import Pin, UART
from time import sleep, ticks_ms, ticks_diff
from machine import Pin
from neopixel import NeoPixel
from pimoroni import RGBLED
#from plasma import plasma2040
import plasma

LED_DATA_PIN = 15
SER_TX_PIN=10
SER_RX_PIN=9
debug_print = False
debug_single_step = False

off: tuple[int, int, int] = (0, 0, 0)

red: tuple[int, int, int] = (255, 0, 0)

orange: tuple[int, int, int] = (255, 50, 0)

yellow = (255, 255, 0)
yelreen = (255, 215, 0)

green = (0, 255, 0)
light_green = (155, 203, 60)
sea_foam = (15, 255, 80)
teal = (0, 139, 139)

blue = (0, 0, 255)
light_blue = (0, 83, 219)

purple: tuple[int, int, int] = (100, 0, 127)
light_purple = (159, 43, 104)
fuchsia = (255,0,255)

pink = (226, 50, 96)
neon_pink = (220, 20, 60)
peach = (250, 95, 85)
char_pink = (214,2,112)

white = (255, 255, 255)

steel_gray = (113, 121, 126)

num_leds: int = 84
halfway = int(num_leds/2)
interpolation_factor = 5

#they are tuples which cannot be changed

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
        frame_count = len(self.frames)
        if frame_count > 0:
            if self.current_frame_idx == 0 or self.current_frame_idx < frame_count:
                for idx, led in enumerate(self.get_current_frame()):
                    self.pixels[idx] = led
                if debug_print:
                    print("Writing frame " + str(self.current_frame_idx) + " / " + str(frame_count))
                self.pixels.write()
		self.current_frame_idx += 1

            if frame_count > 1:
                if self.sleep_duration > 0:
                    if debug_print:
                        print("Sleeping for " + str(self.sleep_duration))
                    sleep(self.sleep_duration)

                # Check for current frame getting larger than our array
                if self.current_frame_idx >= frame_count:
                    self.current_frame_idx = 0

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

def all_color(color: tuple[int, int, int]) -> list[list[tuple[int, int, int]]]:
    result = []
    frame: list[tuple[int, int, int]] = [color]*num_leds
    result.append(frame)

    return result

def all_off():
    return all_color(off)

def dueling_serpents():
    result =[]
    mid_state = []

    for i in range(0, halfway + 1):

        frame = [off]*num_leds

        for j in range(0, i):
            frame[j] = blue
            frame[-1 - j] = red

        result.append(frame)

        mid_state = frame

    for i in range(halfway, -1, -1):
        frame = mid_state.copy()

        for j in range(halfway, i - 1, -1):
            frame[-1 - j] = blue
            frame[j] = red

        result.append(frame)

    return result

def teal_orange_purple():
    result = []
    frame = [off] * num_leds
    frame[0] = teal
    frame[halfway] = orange
    frame[-1] = purple

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

    frame: list[tuple[int, int, int]] = interpolate(orange, purple, num_leds)

    return [frame]

def breathe_orange_purple():
    result = []

    almost_off_orange = (int(orange[0]/20), int(orange[1]/20), int(orange[2]/20))
    almost_off_purple = (int(purple[0]/20), int(purple[1]/20), int(purple[2]/20))

    breathe_orange: list[tuple[int, int, int]] = interpolate(almost_off_orange, orange, 15)
    breathe_purple: list[tuple[int, int, int]] = interpolate(almost_off_purple, purple, 15)

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

def tada():
    result =[]

    my_colors: list[tuple[int, int, int]] = [
        red, sea_foam, blue, orange, purple, yelreen, teal,
        green, pink, fuchsia, yellow, white, light_blue,
        neon_pink, light_purple, orange, steel_gray, red, sea_foam
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


def cylon(base_color: tuple[int, int, int] = red,
          start_idx: int = 0,
          end_idx: int = num_leds,
          tail_length: int = 6,
          initial_pause_frames: int = 10,
          halfway_pause_frames: int = 3) -> list[list[tuple[int, int, int]]]:

    # ---- argument checks ----
    if end_idx > num_leds - 1:
        end_idx = num_leds - 1
    if start_idx < 0:
        start_idx = 0
    if start_idx > end_idx:
        start_idx = end_idx
    if tail_length < 0:
        tail_length = 0
    if tail_length > (end_idx - start_idx):
        tail_length = end_idx - start_idx

    print(f"building cylon animation start={start_idx}, end={end_idx}, tail_length={tail_length}")

    result: list[list[tuple[int, int, int]]] = []

    def scale_color(color, factor):
        r, g, b = color
        return int(r*factor), int(g*factor), int(b*factor)

    def make_frame(head_pos, direction):
        frame = [off] * num_leds

        # head
        frame[head_pos] = base_color

        # tail
        for t in range(1, tail_length + 1):
            tail_pos = head_pos - (direction * t)

            if start_idx <= tail_pos <= end_idx:
                # Linear fade
                #fade = (tail_length - t + 1) / (tail_length + 1)
                # Quadratic fade
                fade = ((tail_length - t + 1) / (tail_length + 1)) ** 2
                frame[tail_pos] = scale_color(base_color, fade)

        return frame

    # ---- initial pause ----
    if initial_pause_frames > 0:
        frame = make_frame(start_idx, 1)
        for _ in range(initial_pause_frames):
            result.append(frame)

    head = start_idx
    direction = 1

    while True:
        # move until endpoint
        while start_idx <= head + direction <= end_idx:
            head += direction
            result.append(make_frame(head, direction))

        # endpoint reached
        endpoint = head

        # tail catch-up
        for remaining in range(tail_length, 0, -1):
            frame = [off]*num_leds
            frame = list(frame)

            # keep head fully lit
            frame[endpoint] = base_color

            # draw remaining tail approaching the head
            for t in range(1, remaining + 1):
                tail_pos = endpoint - (direction * t)

                if start_idx <= tail_pos <= end_idx:
                    fade = (remaining - t + 1) / (tail_length + 1)
                    frame[tail_pos] = scale_color(base_color, fade)

            result.append(frame)

        # pause at endpoint
        if initial_pause_frames > 0:
            frame = [off] * num_leds
            frame[endpoint] = base_color
            for _ in range(halfway_pause_frames):
                result.append(frame)

        # reverse direction
        direction *= -1

        # stop once we have completed a full cycle
        if endpoint == start_idx and direction == 1:
            break

    return result

## Lambda which selects a single frame from an animation, for debugging
## Use like this: frame_func = lambda: one_frame(base_animataion, frame_idx)()
one_frame = lambda frames, idx: (lambda: [frames[idx]])

## Lambda which composes any number of functions
compose = lambda *funcs: [item for func in funcs for item in func()]

## Creates an animation of a fade between two frames using
## linear interpolation.
def fade(
    start_frame: list[tuple[int,int,int]],
    end_frame: list[tuple[int,int,int]],
    steps: int = 5
) -> list[list[tuple[int,int,int]]]:
    result = []

    # Calculate the delta for each pixel
    delta_frame = [
        (
            (end_r - start_r) / steps,
            (end_g - start_g) / steps,
            (end_b - start_b) / steps
        )
        for (start_r, start_g, start_b), (end_r, end_g, end_b) in zip(start_frame, end_frame)
    ]

    # Build frames by applying the delta step by step
    for step in range(1, steps + 1):
        frame = [
            (
                int(start_r + delta_r * step),
                int(start_g + delta_g * step),
                int(start_b + delta_b * step)
            )
            for (start_r, start_g, start_b), (delta_r, delta_g, delta_b) in zip(start_frame, delta_frame)
        ]
        result.append(frame)

    return result

## Returns a color which is half as bright (RGB values / 2)
def half_tone(color : tuple(int,int,int)):
    return tuple(c >> 1 for c in color)

## Duplicates a frame count times
def dup(frame : list[tuple[int,int,int]],
        count : int
)-> list[list[tuple[int,int,int]]] :
    result = []
    if count > 0:
        for _ in range(count):
            result.append(frame)

    return result

fluid_cylon = lambda : compose(lambda : cylon(half_tone(red), 5, 15, 3, 10, 3),
                               lambda : fade([half_tone(red) if i == 5 else (0,0,0) for i in range(num_leds)],
                                             [half_tone(blue) if i == 5 else (0,0,0) for i in range(num_leds)],
                                             10),
                               lambda : cylon(half_tone(blue), 5, 15, 3, 10, 3),
                               lambda : fade([half_tone(blue) if i == 5 else (0,0,0) for i in range(num_leds)],
                                             [half_tone(red) if i == 5 else (0,0,0) for i in range(num_leds)],
                                             10))

ambiguous_alliance = lambda : compose(lambda : dup(all_half_red, 20),
                                      lambda : fade(all_half_red,
                                                    all_half_blue,
                                                    8),
                                      lambda : dup(all_half_blue, 20),
                                      lambda : fade(all_half_blue,
                                                    all_half_red,
                                                    8))

patterns = {
    b"0": (orange_purple_gradient_long, 0.10), # Default
    b"1": (dueling_serpents, 0.20), # Auto/ Transition Shift
    b"2": (teal_orange_purple, 0.1), # Hub is active
    b"3": (breathe_orange_purple, 0.1), # Hub inst ative
    b"4": (rainbow_gradient_long_run, 0.010), # End Game
    b"5": (tada, 0.10), # Climbing
    b"6": (lambda : cylon(half_tone(red), 5, 15, 3, 30, 3), .5 / num_leds),
    b"7": (fluid_cylon, .5 / num_leds)
}

led_pin = Pin(LED_DATA_PIN,Pin.OUT)
neo_out = NeoPixel(led_pin, num_leds, 3)

uart = UART(1, 9600, tx=Pin(SER_TX_PIN), rx=Pin(SER_RX_PIN), timeout = 1)

animator = Animator(neo_out)

# Default animation is ambiguous alliance
animator.set_animation(compose(lambda : dup(all_half_red, 20),
                               lambda : fade(all_half_red,
                                             all_half_blue,
                                             8),
                               lambda : dup(all_half_blue, 20),
                               lambda : fade(all_half_blue,
                                             all_half_red,
                                             8)), 0.05)

try:

    while True:
        read_key = uart.read(1)

        if(read_key is not None and read_key in patterns):
            robot_key = read_key

            if(robot_key in patterns):
                frames_function, sleep_duration = patterns[robot_key]
                animator.set_animation(frames_function(), sleep_duration)

        if(debug_single_step):
            print("Press ENTER to step")
            input()

        animator.advance()

finally:
    neo_out.fill(off)
    neo_out.write()
