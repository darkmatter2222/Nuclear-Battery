import os
import time

for i in range(50):
        os.system(f'libcamera-still -o /home/pi/Desktop/Spectrum1/test.jpg --shutter 30000000 --gain 100 --awbgains 1,1 --immediate')
        time.sleep(10)