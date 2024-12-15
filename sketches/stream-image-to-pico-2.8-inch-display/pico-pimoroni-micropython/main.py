import machine
import random
import time
from pimoroni import RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2
import sys
from machine import UART

# Initialize UART for serial communication
uart = UART(0, baudrate=115200)  # Using UART0 (GPIO 0 and 1)

# set up the display and drawing constants
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, rotate=90)
display.set_backlight(0.5)

WIDTH, HEIGHT = display.get_bounds()
BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)

led = RGBLED(26, 27, 28)

def draw_loading_message():
    display.set_pen(WHITE)
    display.text("Loading...", 60, 150, 0, 3)

def draw_pixel(x, y, r, g, b):
    color = display.create_pen(r, g, b)
    display.set_pen(color)
    display.pixel(x, y)

def read_serial_data():
    if uart.any():
        return uart.read()
    return None

while True:
    # init "loading"
    display.set_pen(BLACK)
    display.clear()
    draw_loading_message()
    display.update()
    led.set_rgb(100, 30, 0)
    
    # Wait for and process incoming data
    y = 0
    while y < HEIGHT:
        x = 0
        while x < WIDTH:
            data = read_serial_data()
            if data:
                # Expect data in format: x,y,r,g,b
                try:
                    pixel_data = data.decode().strip().split(',')
                    if len(pixel_data) == 5:
                        px, py, r, g, b = map(int, pixel_data)
                        draw_pixel(px, py, r, g, b)
                        if x % 4 == 0:  # Update every 4 pixels
                            display.update()
                except:
                    pass
            x += 1
        y += 1
    
    led.set_rgb(0, 100, 0)  # Signal completion
    time.sleep(1)  # Wait before accepting new image