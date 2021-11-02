#!/usr/bin/env python3

# Prometheus Exporter for DS18B20 temp sensors connected to a raspberry pi via one wire
# Usage: ./tempexporter.py

import time
from ds18b20 import DS18B20
from prometheus_client import Gauge, start_http_server
import os

# Create empty metrics variable for the temp off each sensor.
ds18b20_1_temperature_celsius = Gauge('ds18b20_1_temperature_celsius', "Temperature in celsius provided by the first DS18B20 sensor")
ds18b20_2_temperature_celsius = Gauge('ds18b20_2_temperature_celsius', "Temperature in celsius provided by the second DS18B20 sensor")
ds18b20_3_temperature_celsius = Gauge('ds18b20_3_temperature_celsius', "Temperature in celsius provided by the third DS18B20 sensor")
ds18b20_4_temperature_celsius = Gauge('ds18b20_4_temperature_celsius', "Temperature in celsius provided by the fourth DS18B20 sensor")
ds18b20_5_temperature_celsius = Gauge('ds18b20_5_temperature_celsius', "Temperature in celsius provided by the fifth DS18B20 sensor")
ds18b20_6_temperature_celsius = Gauge('ds18b20_6_temperature_celsius', "Temperature in celsius provided by the sixth DS18B20 sensor")
ds18b20_7_temperature_celsius = Gauge('ds18b20_7_temperature_celsius', "Temperature in celsius provided by the seventh DS18B20 sensor")
ds18b20_8_temperature_celsius = Gauge('ds18b20_8_temperature_celsius', "Temperature in celsius provided by the eighth DS18B20 sensor")

sensor1 = DS18B20("0517b14708ff")
sensor2 = DS18B20("0417b2cac8ff")
sensor3 = DS18B20("031097944ab9")
sensor4 = DS18B20("03139794118a")
sensor5 = DS18B20("01192cab6914")
sensor6 = DS18B20("030997945dc6")
sensor7 = DS18B20("030997946b69")
sensor8 = DS18B20("03109794052d")


def read_sensor():
  temp1 = sensor1.get_temperature()
  ds18b20_1_temperature_celsius.set(temp1)
  file = open("/home/pi/temp1.txt", "w")
  file.write(str(temp1))
  file.close()

def read_sensor2():
  temp2 = sensor2.get_temperature()
  ds18b20_2_temperature_celsius.set(temp2)
  file = open("/home/pi/temp2.txt", "w")
  file.write(str(temp2))
  file.close()

def read_sensor3():
  temp3 = sensor3.get_temperature()
  ds18b20_3_temperature_celsius.set(temp3)
  file = open("/home/pi/temp3.txt", "w")
  file.write(str(temp3))
  file.close()

def read_sensor4():
  temp4 = sensor4.get_temperature()
  ds18b20_4_temperature_celsius.set(temp4)
  file = open("/home/pi/temp4.txt", "w")
  file.write(str(temp4))
  file.close()

def read_sensor5():
  temp5 = sensor5.get_temperature()
  ds18b20_5_temperature_celsius.set(temp5)
  file = open("/home/pi/temp5.txt", "w")
  file.write(str(temp5))
  file.close()

def read_sensor6():
  temp6 = sensor6.get_temperature()
  ds18b20_6_temperature_celsius.set(temp6)
  file = open("/home/pi/temp6.txt", "w")
  file.write(str(temp6))
  file.close()

def read_sensor7():
  temp7 = sensor7.get_temperature()
  ds18b20_7_temperature_celsius.set(temp7)
  file = open("/home/pi/temp7.txt", "w")
  file.write(str(temp7))
  file.close()

def read_sensor8():
  temp8 = sensor8.get_temperature()
  ds18b20_8_temperature_celsius.set(temp8)
  file = open("/home/pi/temp8.txt", "w")
  file.write(str(temp8))
  file.close()

#main function to start the prometheus metrics server and then read each sensor every 10 seconds.
def main():
    start_http_server(8001)
    while True:
      try:
        read_sensor()
        read_sensor2()
        read_sensor3()
        read_sensor4()
        read_sensor5()
        read_sensor6()
        read_sensor7()
        read_sensor8()
        time.sleep(10)
      except:
        pass
main()
