# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import digitalio
import displayio
from adafruit_display_text import label
from adafruit_seesaw.seesaw import Seesaw

import gc9a01

moisture_dry_below = 200
moisture_wet_above = 400

temp_cold_below = 15
temp_hot_above = 30

priority = "moisture"

read_int = 5

display_width = 240
display_height = 280

moods = {
    "happy": "",
    "dry": "",
    "wet": "",
    "hot": "",
    "cold": "",
}


i2c = busio.I2C(board.SCL, board.SDA)
soil_sensor = Seesaw(i2c, addr=0x36)


def read_sensor():
    moisture = soil_sensor.moisture_read()
    temperature = soil_sensor.get_temp()
    return moisture, temperature


displayio.release_displays()

spi = busio.SPI(clock=board.GP9, MOSI=board.GP11)

tft_cs = board.GP1
tft_dc = board.GP2
tft_rst = board.GP3
blacklight_pin = board.GP4


backlight = digitalio.DigitalInOut(blacklight_pin)
backlight.direction = digitalio.Direction.OUTPUT
backlight.value = True

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = gc9a01.GC9A01(display_bus, width=240, height=280)

main_group = displayio.Group()
display.root_group = main_group

_image_cache = {}
_current_tile = None


def draw_mood(mood_key):
    global _current_tile

    if mood_key not in _image_cache:
        bitmap, palette = adafruit_imageload.load(
            moods[mood_key],
            bitmap=displayio.Bitmap,
            palette=displayio.Palette,
        )
        _image_cache[mood_key] = (bitmap, palette)

        bitmap, palette = _image_cache[mood_key]
        new_tile = displayio.TileGrid(bitmap, pixel_shader=palette)

    if _current_tile is not None:
        main_group.remove(_current_tile)
    main_group.append(new_tile)
    _current_tile = new_tile




while True:
    # read moisture level through capacitive touch pad
    touch = ss.moisture_read()

    # read temperature from the temperature sensor
    temp = ss.get_temp()

    print("temp: " + str(temp) + "  moisture: " + str(touch))
    time.sleep(1)

if temp > 40:
