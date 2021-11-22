import os
import time

for i in range(50):
        os.system(f'libcamera-jpeg -o /home/pi/Desktop/Spectrum1/{i}.jpg --gain=25 --shutter=600000')
        time.sleep(10)