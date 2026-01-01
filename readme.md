# Raumklima Playground
This repo contains a small setup that logs time series data to an influxdb2 bucket. Data is visualized using grafana.

## Setup
__Hardware:__

* Raspberry Pi 4 (1GB RAM):
    * DHT11: temperature/humidity sensor connected to GPIO-pin 17
    * DS18B20: temperature sensor connected to GPIO-pin 4 (ONEWIRE)

__Software:__

* OS: Debian GNU/Linux 13 (trixie)
* Python: v3.13.5
* InfluxDB2: v2.8.0
* Grafana: TODO

# Get Things Running
0. Manage your wiring and setup your Raspi for reading the sensors
This isn't straight forward as my particular sensors came with handy breakout boards.
Depending on your sensor you might need to add a pull-up resistor. Also make sure to enable one-wire using `raspi-config`.
Connect your data wires to the respective pins aswell as VCC and ground.
1. Setup Python 
Setup your virtual environment and install requirements using 
```shell
pip install -r requirements.txt
```
2. Make sure sensor data is read 
Activate your venv (`source venv/bin/activate`) and run `python sensor_test.py`.
If everything is connected properly sensor values should be written to the terminal.
3. Setup the systemd service
TODO
4. Setup Grafana
