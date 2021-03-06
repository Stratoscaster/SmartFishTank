import os
import glob
import time
from queue import Queue

class TempReader:

    def __init__(self):
        # os.system('sudo dtoverlay w1-gpio gpiopin=6 pullup=0')
        # os.system('sudo dtoverlay w1-gpio gpiopin=4 pullup=0')
        # os.system('modprobe w1-gpio')
        # os.system('modprobe w1-therm')
        self.base_dir = '/sys/bus/w1/devices/'
        self.device_folder = glob.glob(self.base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep
            # NO SPACES IN DTOVERLAY, YOU NEED TO CHANGE IT FOR IT TO BE FIXED(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            if temp_f >= 185.0:
                # print(temp_f, temp_c)
                # print('Error reading temperatures. Check your pins.')
                return self.read_temp()  # try again if there is an error reading the temp
            return temp_c, temp_f


temp_reader = TempReader()  
print(temp_reader.read_temp())

