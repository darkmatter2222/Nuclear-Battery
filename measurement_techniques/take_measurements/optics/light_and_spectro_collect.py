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

result = {'lux': veml7700.lux,
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
          'sensor_config': {
              'adafruit_VEML7700': {
                  'integration_time_value': veml7700.integration_time_value(),
                  'gain_value': veml7700.gain_value()
              }
          }
          }

print(json.dumps(result, indent=1))
