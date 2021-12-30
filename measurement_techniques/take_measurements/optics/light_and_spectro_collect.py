# Lux = https://github.com/adafruit/Adafruit_CircuitPython_VEML7700
# spectro = https://github.com/adafruit/Adafruit_CircuitPython_AS7341

from time import sleep
import board
import json
import time
import itertools
from adafruit_as7341 import AS7341
import adafruit_veml7700

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = AS7341(i2c)
veml7700 = adafruit_veml7700.VEML7700(i2c)

vial_color = input("What color is the vial?")
vial_age_years = input("how many years old is the vial?")

adafruit_VEML7700_gains = [2, 1, 0.25, 0.125]
adafruit_VEML7700_integration_times = [15, 50, 100, 200, 400, 800]
adafruit_AS7341_gains = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

x = 0
result = {}

for adafruit_VEML7700_gain, adafruit_VEML7700_integration_time, adafruit_AS7341_gain in list(itertools.product(adafruit_VEML7700_gains, adafruit_VEML7700_integration_times, adafruit_AS7341_gains)):
    sensor.gain = adafruit_AS7341_gain
    veml7700.light_integration_time = adafruit_VEML7700_integration_time
    veml7700.light_gain = adafruit_VEML7700_gain

    result[x] = {'vial_color': vial_color,
              'vial_age_years': vial_age_years,
              'unix_time_ns': time.time_ns(),
              'lux': veml7700.lux,
              'target_wavelengths': {
                  '415': {
                      'color_name': 'Violet',
                      'color_intensity': sensor.channel_415nm,
                  },
                  '445': {
                      'color_name': 'Indigo',
                      'color_intensity': sensor.channel_445nm,
                  },
                  '480': {
                      'color_name': 'Blue',
                      'color_intensity': sensor.channel_480nm,
                  },
                  '515': {
                      'color_name': 'Cyan',
                      'color_intensity': sensor.channel_515nm,
                  },
                  '555': {
                      'color_name': 'Green',
                      'color_intensity': sensor.channel_555nm,
                  },
                  '590': {
                      'color_name': 'Yellow',
                      'color_intensity': sensor.channel_590nm,
                  },
                  '630': {
                      'color_name': 'Orange',
                      'color_intensity': sensor.channel_630nm,
                  },
                  '680': {
                      'color_name': 'Red',
                      'color_intensity': sensor.channel_680nm,
                  },
              },
              'special_measurements': {
                  'Clear': {
                      'color_name': 'Clear',
                      'color_intensity': sensor.channel_clear,
                  },
                  'NIR': {
                      'color_name': 'Near-IR',
                      'color_intensity': sensor.channel_nir,
                  },
              },
              'sensor_configs': {
                  'adafruit_VEML7700': {
                      'integration_time_value': veml7700.integration_time_value(),
                      'gain_value': veml7700.gain_value()
                  },
                  'adafruit_AS7341': {
                      'gain': sensor.gain
                  }
              }
              }
    x += 1

print(json.dumps(result, indent=1))
