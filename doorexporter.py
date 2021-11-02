#!/usr/bin/env python3

#Prometheus exporter for a standard magnetic door/window sensor on pin 16
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
