# Pretend we are streaming in pixels from serial (not happening yet) and write to all display pixels.

import machine
import random
import time
from pimoroni import RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2

# set up the display and drawing constants
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, rotate=90)

# set the display backlight to 50% 
display.set_backlight(0.5)

WIDTH, HEIGHT = display.get_bounds()
BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)

led = RGBLED(26, 27, 28)

def draw_loading_message():
    display.set_pen(WHITE)
    display.text("Loading...", 60, 150, 0, 3)

def draw_noise_pixel(x, y):
    color = display.create_pen(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    display.set_pen(color)
    display.pixel(x, y)
    
def draw_noise_row(y):
    x = 0
    while x < WIDTH:
        draw_noise_pixel(x, y)
        x = x + 1

def draw_noise_image():
    y = 0
    while y < HEIGHT:
        draw_noise_row(y)
        y = y + 1
        
        # draw not on every row update (full update takes 3.5 secs or so, this slightly slower yet more fun)
        if y % 4 == 0:
            display.update()
    #display.update()

while True:
    # init "loading"
    display.set_pen(BLACK)
    display.clear()
    draw_loading_message()
    led.set_rgb(100, 30, 0)
    
    # draw image (pretend we're streaming in data and drawing it as it comes in)
    draw_noise_image()
    
    # done "loading"
    led.set_rgb(0, 100, 0)

    # enjoy image until a new image is available... after a delay for now
    time.sleep(5)

