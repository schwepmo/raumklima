from datetime import datetime, timezone
import time
import os

# sensor reading functions (all temps are celsius, idc about fahr(t)enheit)
from read_dht11 import read_dht11
from read_ds18b20 import read_ds18b20


from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "home"

client = InfluxDBClient.from_config_file("env.toml")
write_api = client.write_api(write_options=SYNCHRONOUS)

# get time
now = datetime.now(timezone.utc)
# get measurements
dht11_temp, dht11_humid = read_dht11()
ds18b20_temp = read_ds18b20()
points = [
    Point("env_measurement")
    .tag("location", "livingroom")
    .tag("sensor_type", "dht11")
    .field("temperature", dht11_temp)
    .field("humidity", dht11_humid)
    .time(now),

    Point("env_measurement")
    .tag("location", "livingroom")
    .tag("sensor_type", "ds18B20")
    .field("temperature", ds18b20_temp)
    .time(now)
]

write_api.write(bucket=bucket, record=points)
print(f"Wrote sensors at {datetime.now()}")
