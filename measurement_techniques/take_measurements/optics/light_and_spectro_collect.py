# Lux = https://github.com/adafruit/Adafruit_CircuitPython_VEML7700
# spectro = https://github.com/adafruit/Adafruit_CircuitPython_AS7341

from time import sleep
import board
import json
from tqdm import tqdm
import time
import itertools
from adafruit_as7341 import AS7341
import adafruit_veml7700

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = AS7341(i2c)
veml7700 = adafruit_veml7700.VEML7700(i2c)

vial_color = input("What color is the vial?")
vial_age_years = input("how many years old is the vial?")

adafruit_VEML7700_gains = [veml7700.ALS_GAIN_2, veml7700.ALS_GAIN_1, veml7700.ALS_GAIN_1_4, veml7700.ALS_GAIN_1_8]
adafruit_VEML7700_integration_times = [veml7700.ALS_25MS, veml7700.ALS_50MS, veml7700.ALS_100MS, veml7700.ALS_200MS, veml7700.ALS_400MS, veml7700.ALS_800MS]
adafruit_AS7341_gains = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

x = 0
result = {}

for adafruit_VEML7700_gain, adafruit_VEML7700_integration_time, adafruit_AS7341_gain in tqdm(list(itertools.product(adafruit_VEML7700_gains, adafruit_VEML7700_integration_times, adafruit_AS7341_gains))):
    try:
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
    except:
        print(adafruit_AS7341_gain)
        print(adafruit_VEML7700_integration_time)
        print(adafruit_VEML7700_gain)
        print('###')

f = open(f"{vial_color}.json", "w")
f.write(json.dumps(result, indent=1))
f.close()
