import os

for i in range(20):
        os.system(f'libcamera-jpeg -o /home/pi/Desktop/Spectrum1/{i}.jpg --gain=25 --shutter=600000')