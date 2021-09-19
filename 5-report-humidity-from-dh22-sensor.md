# DHT22 addition

The DHT22 add on board that I have already has the pull up resistor built onto the little PCB and has just 3 pins out instead of the actual 4 pins that come off the DHT22 itself. 
If you have a raw DHT22 sensor - follow along here: https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/ 

In our case, we wire up:

```
-Pwr (3v3)
-GND 
-Out (data / signal to pin 17)
```

I also foudn that pypi or python or maybe it's pip is somewhat case sensitive - I had some trouble with a message about "cannot find module Adafruit_DHT" even after running the pip3 install suceessfully.  I think this was down to a capitalization issue - so if you copy from my examples below you should be fine. 

```
pip3 install Adafruit_DHT
pip3 install board
```

So then we have to set up the humidity exporter itself, it's just in the /home/pi/humidityexporter.py: 

```
#!/usr/bin/env python3

# Prometheus exporter for a DHT22 sensor wired up to BCM numbering pin 17. 
# Usage: ./humidityexporter.py

import Adafruit_DHT
from board import * 
import time
from  prometheus_client import Gauge, start_http_server

# Create metrics for the temp and humidity off the sensor

dht22_1_temperature_celsius = Gauge('dht22_1_temperature_celsius', "Temperature in celsius provided by the DHT22 sensor")
dht22_1_humidity = Gauge('dht22_1_humidity', "Humidity provided by the DHT22 Sensor")

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 17

def read_sensors():
  humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
  dht22_1_temperature_celsius.set(temperature)
  dht22_1_humidity.set(humidity)

def main():
    start_http_server(8002)
    while True:
      try:
        read_sensors() 
        time.sleep(10)
      except:
        pass

main()

```

Now that we've got a humidity exporter, let's get it running serving those metrics all the time even after a reboot so we need to create a service:

```
sudo vi /etc/systemd/system/humidityexporter.service

[Unit]
Description=Humidity Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=pi
ExecStart=/home/pi/humidityexporter.py

[Install]
WantedBy=default.target
```

then to see the new service, make it persist reboots, and start it up:

```
sudo systemctl daemon-reload
sudo systemctl enable humidityexporter
sudo systemctl start humidityexporter
sudo systemctl status humidityexporter
```

So now on our local IP address of the Pi we can visit port 8002 and we should see another prometheus metrics formatted page, and at the bottom have the temp and humidity data from the dht22 sensor.

https://192.168.1.106:8002

![example of what you'll see on port 8002](/images/humidity_exporter_metrics.jpg)


So now, in order to get these metrics reporting into Prometheus, and ultimately available to us for dashboarding in Grafana cloud we need to tell prometheus to go scrape those additional metrics that are on port 8002. 

So we edit the /home/pi/prometheus/prometheus.yml file and that same static_configs area from earlier we're going to add port 8002:

```
    static_configs:
      - targets: ["localhost:9090","localhost:8001", "localhost:8002"]
```

Then a quick `sudo systemctl restart prometheus` to restart the prometheus instance which will start grabbing and shipping those metrics. 

I found that after a restart prometheus still didn't send the metrics like I was expecting so I ended up doing a full reboot of the pi and then things behaved as I expected.  
This is one of the reasons we target services and setting them up this way so they can restart nicely with just a quick `sudo reboot now` command. 



