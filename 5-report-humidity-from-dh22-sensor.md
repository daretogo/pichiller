# DHT22 addition

The DHT22 has 3 pins


sudo pip3 install Adafruit_DHT
pip3 install board


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

SENSOR_PIN = D17

dht22 = adafruit_dht.DHT22(SENSOR_PIN, use_pulseio=False)

def read_temp_sensor():
  dht22_1_temperature_celsius.set(dht22.temperature)



def read_humidity_sensor():
  dht22_1_humidity.set(dht22.humidity)


def main():
    start_http_server(8002)
    while True:
      try:
        read_temp_sensor()
        read_humidity_sensor()
        time.sleep(10)
      except:
        pass

main()

```
