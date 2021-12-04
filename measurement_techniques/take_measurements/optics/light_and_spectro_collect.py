# Lux = https://github.com/adafruit/Adafruit_CircuitPython_VEML7700
# spectro = https://github.com/adafruit/Adafruit_CircuitPython_AS7341

from time import sleep
import board
import json
from adafruit_as7341 import AS7341
import adafruit_veml7700

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = AS7341(i2c)
veml7700 = adafruit_veml7700.VEML7700(i2c)

result = {'lux': 0,
          'target_wavelengths': {
              '415': {
                  'color_name': 'Violet',
                  'color_intensity': 0,
              },
              '445': {
                  'color_name': 'Indigo',
                  'color_intensity': 0,
              },
              '480': {
                  'color_name': 'Blue',
                  'color_intensity': 0,
              },
              '515': {
                  'color_name': 'Cyan',
                  'color_intensity': 0,
              },
              '555': {
                  'color_name': 'Green',
                  'color_intensity': 0,
              },
              '590': {
                  'color_name': 'Yellow',
                  'color_intensity': 0,
              },
              '630': {
                  'color_name': 'Orange',
                  'color_intensity': 0,
              },
              '680': {
                  'color_name': 'Red',
                  'color_intensity': 0,
              },
          },
          'special_measurements': {
              'Clear': {
                  'color_name': 'Clear',
                  'color_intensity': 0,
              },
              'NIR': {
                  'color_name': 'Near-IR',
                  'color_intensity': 0,
              },
          }
          }


def bar_graph(read_value):
    scaled = int(read_value / 1000)
    return "[%5d] " % read_value + (scaled * "*")

# begin taking measurement
result['lux'] = veml7700.lux
result['target_wavelengths']['415'] = sensor.channel_415nm
result['target_wavelengths']['445'] = sensor.channel_445nm
result['target_wavelengths']['480'] = sensor.channel_480nm
result['target_wavelengths']['515'] = sensor.channel_515nm
result['target_wavelengths']['555'] = sensor.channel_555nm
result['target_wavelengths']['590'] = sensor.channel_590nm
result['target_wavelengths']['630'] = sensor.channel_630nm
result['target_wavelengths']['680'] = sensor.channel_680nm
result['special_measurements']['Clear'] = sensor.channel_clear
result['special_measurements']['NIR'] = sensor.channel_nir

print(json.loads(result, indent=1))
