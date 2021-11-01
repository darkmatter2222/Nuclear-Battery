import RPi.GPIO as GPIO
import time
import datetime
import threading
import Adafruit_ADS1x15
from pymongo import MongoClient
import pymongo
import os
import json
from tqdm import tqdm
from dotenv import load_dotenv

from pathlib import Path

dotenv_path = Path('/home/pi/source/repos/.env')
load_dotenv(dotenv_path=dotenv_path)

myclient = pymongo.MongoClient(os.getenv('nuclear_battery_mongo_connection_string'))
mydb = myclient["nuclear_battery"]
mycol = mydb["testing_data_v2"]

GPIO.setmode(GPIO.BCM)
voltage_measurement_pin = 26
current_measurement_pin = 6
reset_pin = 19
GPIO.setup(voltage_measurement_pin, GPIO.OUT)
GPIO.setup(current_measurement_pin, GPIO.OUT)
GPIO.setup(reset_pin, GPIO.OUT)

tritium_cell_number = input("What tritium cell number is this?")
solar_cell_number = input("What solar cell number is this?")
adc = Adafruit_ADS1x15.ADS1115()

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1
total_duration = 600
duration = 0
interval = 10
number_of_tests = int(total_duration / interval)
results = []
time_of_test = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")


def average(lst):
    return sum(lst) / len(lst)


def take_voltage_measurement(pin, adc_channel):
    count_measurements = 50
    total_measurement_duration = 0.5
    inter_duration = total_measurement_duration / count_measurements
    measurements = []

    # tap in and measure
    GPIO.output(pin, GPIO.HIGH)
    for i in range(count_measurements):
        time.sleep(inter_duration)
        measurements.appen(adc.read_adc(adc_channel, gain=GAIN))
    GPIO.output(pin, GPIO.LOW)
    # tap out, measurements complete

    value = average(measurements)
    voltage = round((4.096 * value) / 32767, 6)
    return voltage


def take_current_measurement(resistor_ohms=100000):
    voltage = take_voltage_measurement(current_measurement_pin, 1)
    amperage = voltage / resistor_ohms
    return amperage


def get_voltage():
    return take_voltage_measurement(voltage_measurement_pin, 0)


def get_current():
    return take_current_measurement()


def perform_measurement(upload_to_mongo=False, v=False):
    global duration
    global adc
    global results
    global time_of_test
    duration += interval
    voltage = get_voltage()
    time.sleep(0.5)
    amperage = get_current()

    if v:
        print(f"voltage (V):{voltage}, amperage (A):{format(amperage, '.12f')}, duration interval (s):{duration}")
    results.append({'time': duration, 'voltage': voltage, 'amperage': format(amperage, '.12f'),
                    'tritium_cell_number': tritium_cell_number,
                    'solar_cell_number': solar_cell_number, 'time_of_test': time_of_test})

    if upload_to_mongo:
        dict = {'time_of_test': time_of_test, 'tests': results, 'features': ['time', 'voltage', 'amperage',
                                                                            'tritium_cell_number', 'solar_cell_number',
                                                                            'time_of_test']}
        mycol.insert_one(dict)
        time_of_test = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        duration = 0
        results = []


verbose = True

while True:
    print("Resetting Cap...")
    GPIO.output(reset_pin, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(reset_pin, GPIO.LOW)
    print("Cap Reset.")
    time.sleep(2)
    print("Starting Test...")
    for i in tqdm(range(number_of_tests)):
        time.sleep(interval)
        final = False
        if i == number_of_tests - 1:
            final = True
            perform_measurement(final, verbose,)
        else:
            t = threading.Thread(target=perform_measurement, args=(final, verbose,))
            t.start()



