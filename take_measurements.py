import RPi.GPIO as GPIO
import time
import datetime
import threading
import Adafruit_ADS1x15
from pymongo import MongoClient
import pymongo
import os
import json
from dotenv import load_dotenv

from pathlib import Path

dotenv_path = Path('/home/pi/source/repos/.env')
load_dotenv(dotenv_path=dotenv_path)

myclient = pymongo.MongoClient(os.getenv('nuclear_battery_mongo_connection_string'))
mydb = myclient["nuclear_battery"]
mycol = mydb["testing_data"]

GPIO.setmode(GPIO.BCM)
measurement_pin = 26
reset_pin = 19
GPIO.setup(measurement_pin,GPIO.OUT)
GPIO.setup(reset_pin,GPIO.OUT)

cell_number = input("what is the cell number?")
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
duration=30
results = []
time_of_test = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")


def perform_measurement(upload_to_mongo = False):
    global duration
    global adc
    global results
    global time_of_test
    GPIO.output(measurement_pin, GPIO.HIGH)
    time.sleep(0.5)
    value = adc.read_adc(0, gain=GAIN)
    voltage = round((4.096 * value) / 32767, 6)
    GPIO.output(measurement_pin, GPIO.LOW)
    print(f"voltage:{voltage} duration:{duration}")
    results.append({'time': duration, 'voltage': voltage, 'cell_number': cell_number, 'time_of_test': time_of_test})
    duration += 30
    if upload_to_mongo:
        dict = {'time_of_test': time_of_test, 'tests': results}
        mycol.insert_one(dict)
        time_of_test = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        duration = 30
        results = []

number_of_tests = 20

while True:
    print("resetting cap...")
    GPIO.output(reset_pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(reset_pin, GPIO.LOW)
    print("cap reset.")

    for i in range(20):
        final = False
        if 1 == number_of_tests - 1:
            final = True
        t = threading.Thread(target=perform_measurement, args=(final))
        time.sleep(30)
        t.start()
