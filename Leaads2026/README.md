# Getting Started
1. Install [Thonny](https://thonny.org/)

1. Install Mycropython Firmware for RP2 / Pimoroni - Tiny 2024 (w/Pimoroni Libraries)
    1. Connect device to USB while holding RESET to convert to USB mode
    1. Hold BOOT, press RESET, release RESET to convert to USB mode
    1. In Thonny, go to Run > Configure Interpreter, then "Install or update MicroPython"

1. Connect the LED strip
    1. +5V
    1. GND
    1. Data (check main.py for recommended and configured pins)

1. Try to get a sample running
    ```
    import machine
    import neopixel
    import time

    # Number of NeoPixels on your strip
    NUM_LEDS = 21
    # GPIO pin for data, typically GPIO 0 on Tiny 2350 and GPIO 15 on Plasma 2350
    DATA_PIN = 0 

    # Setup the strip
    np = neopixel.NeoPixel(machine.Pin(DATA_PIN), NUM_LEDS)

    def set_color(r, g, b):
        for i in range(NUM_LEDS):
            np[i] = (r, g, b)
        np.write()

    # Example: Run a simple red cycle
    while True:
        set_color(255, 0, 0) # Red
        time.sleep(1)
        set_color(0, 255, 0) # Green
        time.sleep(1)
        set_color(0, 0, 255) # Blue
        time.sleep(1)
    ```
1. Run code from this repo
    1. Take care to set the DATA_PIN value as appropriate

1. Install the code on the board so it runs without USB connection
    1. In Thonny, click "Save" and choose "RP2040" (or similar)
    1. Name the file `main.py`

1. Set up serial connection for control
    1. TX and RX pins (check main.py for recommended and configured pins)
    1. In Robot code, use the SerialPort class. You probably want the kOnboard
       port. Match baud rate. Send pattern numbers as a single byte (e.g. 0x01)
       not as strings (e.g. "1" which is 0x31).

1. Try something more advanced like PWM for brightness
    1. https://forums.pimoroni.com/t/tiny-2040-rgb-led-control-tutorial/16604

## References
* [Plasma 2350 Documentation](https://shop.pimoroni.com/products/plasma-2350?variant=42092628246611)
* [Tiny 2350 Documentation](https://shop.pimoroni.com/products/tiny-2350?variant=42092638699603)
* [MicroPython UART Documentation](https://docs.micropython.org/en/latest/library/machine.UART.html)
* [MicroPython NeoPixel Documentation](https://docs.micropython.org/en/latest/library/neopixel.html)

## Troubleshooting
MicroPython will tell you what modules are installed:

```>>> help("modules")```

Look for modules like "pimoroni" and "neopixel". To find out what's in them, try:

```
>>> import pimoroni
>>> dir(pimoroni)

['__class__', '__name__', 'ADC', 'PWM', 'Pin', '__dict__', '__file__', 'time', 'Analog', 'AnalogMux', 'BREAKOUT_GARDEN_I2C_PINS', 'BREAKOUT_GARDEN_SPI_SLOT_BACK', 'BREAKOUT_GARDEN_SPI_SLOT_FRONT', 'Button', 'Buzzer', 'HEADER_I2C_PINS', 'NORMAL_DIR', 'PICOVISION_I2C_PINS', 'PICO_EXPLORER_I2C_PINS', 'PICO_EXPLORER_SPI_ONBOARD', 'PID', 'PWMLED', 'REVERSED_DIR', 'RGBLED', 'ShiftRegister']

>>> import neopixel
>>> dir(neopixel)
['__class__', '__name__', '__dict__', '__file__', '__version__', 'bitstream', 'NeoPixel']
```
