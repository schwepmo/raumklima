# Raumklima Playground
This repo contains a small setup that logs time series data to an influxdb2 bucket. Data is visualized using grafana.

![screenshot](screenhsot.png)

## Setup
__Hardware:__

* Raspberry Pi 4 (1GB RAM):
    * DHT11: temperature/humidity sensor connected to GPIO-pin 17
    * DS18B20: temperature sensor connected to GPIO-pin 4 (ONEWIRE)

__Software:__

* OS: Debian GNU/Linux 13 (trixie)
* Python: v3.13.5
* InfluxDB2: v2.8.0
* Grafana: 12.3.1

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
3. Setup InfluxDB2
Install and setup a InfluxDB2 with a respective org and bucket.
add a `env.toml` file with your credentials, which will be read by the python script to allow writing to influx using the python client.
4. Setup the systemd service
Add symbolic links to the service files:
```
ln -s ~/raumklima/environment_measurement.timer ~/.config/systemd/user/
ln -s ~/raumklima/environment_measurement.service ~/.config/systemd/user/
```
Start timer:
```
systemctl --user daemon-reload
systemctl --user enable --now environment_measurement.timer
```

Make sure to enable lingering so your user services are automatically started and continue being run after logout.
```
loginctl list-users # get your username
loginctl enable-linger <username>
```

4. Setup Grafana
Install grafana following their installation guide and import the `dashboard-simple.yaml` for a very basic dashboard showcasing the current temperature and humidity as well as a time-series plot over the last 12h (with a 5min rolling-window).
