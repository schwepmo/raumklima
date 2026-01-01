#!/usr/bin/env python3
import time
import board
import adafruit_dht

MAX_MEASURE_ATTEMPTS=5
# DHT11 setup (change D17 to your GPIO pin)
DHT_PIN = board.D17  # or board.D4, board.D18, etc.
dht_device = adafruit_dht.DHT11(DHT_PIN, use_pulseio=False)

def read_dht11():
    attempts = 0
    while attempts < MAX_MEASURE_ATTEMPTS:
        try:
            dht_temp_c = dht_device.temperature
            if dht_temp_c is not None:
                dht_humidity = dht_device.humidity
                return dht_temp_c, dht_humidity
        except:
            time.sleep(1)
    return None, None

