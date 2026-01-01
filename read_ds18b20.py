#!/usr/bin/env python3
import time
import glob

MAX_MEASURE_ATTEMPTS=5
# 1-Wire DS18B20 setup
base_dir = '/sys/bus/w1/devices/'

def read_ds18b20_raw(device_file):
    """Read raw data from DS18B20"""
    try:
        with open(device_file, 'r') as f:
            lines = f.readlines()
        return lines
    except:
        return None

def read_ds18b20():
    """Parse DS18B20 temperature with retry"""
    device_folders = glob.glob(base_dir + '28*')
    if not device_folders:
        return None, None

    device_folder = device_folders[0]
    device_file = device_folder + '/w1_slave'

    lines = read_ds18b20_raw(device_file)
    if not lines:
        return None, None

    # Retry until good CRC
    attempts = 0
    while lines[0].strip()[-3:] != 'YES' and attempts < MAX_MEASURE_ATTEMPTS:
        time.sleep(0.2)
        lines = read_ds18b20_raw(device_file)
        attempts += 1

    if len(lines) < 2:
        return None, None

    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    return None

