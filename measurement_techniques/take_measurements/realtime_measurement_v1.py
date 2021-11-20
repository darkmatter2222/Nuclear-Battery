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
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

GPIO.setmode(GPIO.BCM)
voltage_measurement_pin = 26
current_measurement_pin = 6
reset_pin = 19
GPIO.setup(voltage_measurement_pin, GPIO.OUT)
GPIO.setup(current_measurement_pin, GPIO.OUT)
GPIO.setup(reset_pin, GPIO.OUT)

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


def average(lst):
    return sum(lst) / len(lst)


GAIN = 1
max_list_length = 30

voltage_list = []
current_list = []


def perform_measurement():
    global voltage_list
    global current_list

    channel = 0
    value = adc.read_adc(channel, gain=GAIN)
    voltage = round((4.096 * value) / 32767, 6)
    voltage_list.append(voltage)
    if len(voltage_list) > max_list_length:
        del voltage_list[0]

    channel = 1
    value = adc.read_adc(channel, gain=GAIN)
    voltage = round((4.096 * value) / 32767, 6)
    amperage = voltage / 100000
    current_list.append(amperage)
    if len(current_list) > max_list_length:
        del current_list[0]



GPIO.output(voltage_measurement_pin, GPIO.HIGH)

print("Resetting Cap...")
GPIO.output(reset_pin, GPIO.HIGH)
time.sleep(2)
GPIO.output(reset_pin, GPIO.LOW)
print("Cap Reset.")

try:
    print("Beginning...")
    while True:
        #time.sleep(0.5)
        perform_measurement()
        plt.clf()
        plt.plot(voltage_list, color='blue')
        plt.axhline(y=average(voltage_list), color='red', linestyle='-')
        plt.pause(0.05)
except Exception as e:
    print(e)

#GPIO.output(voltage_measurement_pin, GPIO.LOW)

