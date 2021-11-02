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
