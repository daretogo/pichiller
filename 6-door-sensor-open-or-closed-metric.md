# Getting a magnetic door switch metric collected

```
GPIO.setmode(GPIO.BCM)  



state = 

print(state)

# 0 = closed
# 1 = open

```

```
#!/usr/bin/env python3

# Prometheus exporter for a standard magnetic door/window sensor on pin 16
# Usage: ./doorexporter.py

import RPi.GPIO as GPIO
import sys
import signal 
from board import * 
import time
from  prometheus_client import Gauge, start_http_server

# Create metrics for the state of the door
door_1_state = Gauge('door_1_state', "State of the magnetic door switch 0=closed, 1=open")

# Setup BCM numbering, and give the pin for this sensor
GPIO.setmode(GPIO.BCM) 
DOOR_SENSOR_PIN = 16

# Set up the door sensor pin with the built in pullup.
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP) 

def read_doorsensor():
  state = GPIO.input(DOOR_SENSOR_PIN) 
  door_1_state.set(state)

def main():
    start_http_server(8003)
    while True:
      try:
        read_doorsensor() 
        time.sleep(10)
      except:
        pass

main()
```

And now that we have our exporter running getting and reporting the status of the door sensor, we'll want that thing to run as a service just like the other 2:

```
[Unit]
Description=Magnetic door sensor Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=pi
ExecStart=/home/pi/doorexporter.py

[Install]
WantedBy=default.target
```

sudo systemctl daemon-reload
sudo systemctl enable doorexporter
Created symlink /etc/systemd/system/default.target.wants/doorexporter.service → /etc/systemd/system/doorexporter.service.
sudo systemctl start doorexporter

And then to add it to the prometheus config and reboot

```
    static_configs:
      - targets: ["localhost:9090","localhost:8001", "localhost:8002", "localhost:8003"]
```




