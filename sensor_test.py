#!/usr/bin/env python3
import time
import os
import glob
import board
import adafruit_dht

# DHT11 setup (change D17 to your GPIO pin)
DHT_PIN = board.D17  # or board.D4, board.D18, etc.
dht_device = adafruit_dht.DHT11(DHT_PIN, use_pulseio=False)

# 1-Wire DS18B20 setup
base_dir = '/sys/bus/w1/devices/'

def read_ds18b20_raw(device_file):
    """Read raw data from DS18B20"""
    try:
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
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
    while lines[0].strip()[-3:] != 'YES' and attempts < 3:
        time.sleep(0.2)
        lines = read_ds18b20_raw(device_file)
        attempts += 1
    
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
    return None, None

def read_dht11():
    dht_temp_c = dht_device.temperature
    if dht_temp_c is not None:
        dht_temp_f = dht_temp_c * (9 / 5) + 32
        dht_humidity = dht_device.humidity
        return dht_temp_c, dht_temp_f, dht_humidity
    else:
        return None, None, None

print("Starting DHT11 + DS18B20 sensor readings...")
print("Press Ctrl+C to stop")

while True:
    try:
        # DHT11 readings
        print("=== DHT11 ===")
        dht_temp_c, dht_temp_f, dht_humidity = read_dht11()
        if dht_temp_c is not None:
            print(f"Temp: {dht_temp_c:.1f}°C / {dht_temp_f:.1f}°F  Humidity: {dht_humidity:.1f}%")
        else:
            print("DHT11: No reading")
        
        # DS18B20 readings
        print("=== DS18B20 ===")
        ds_temp_c, ds_temp_f = read_ds18b20()
        if ds_temp_c is not None:
            print(f"Temp: {ds_temp_c:.1f}°C / {ds_temp_f:.1f}°F")
        else:
            print("DS18B20: No sensor detected or read error")
        
        print("-" * 30)
        
    except RuntimeError as error:
        print(f"DHT11 Error: {error.args[0]}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    time.sleep(2.0)

