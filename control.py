#!/usr/bin/env python3

# Control script to run in a loop to maintain a target temperature of 38 to 40F

import time
import os

#to support the turning on/off of the gpio pins that switch the relays for the AC and the power to the liar heating probe
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# We need current temperature data

def get_current_heater_temp():
    f = open("/home/pi/temp1.txt", "r")
    HEATER_PROBE_TEMP_CELSIUS = f.read()
    return(HEATER_PROBE_TEMP_CELSIUS)

def get_temp2():
    f = open("/home/pi/temp2.txt", "r")
    TEMP_2_CELSIUS = f.read()
    return(TEMP_2_CELSIUS)

def get_temp3():
    f = open("/home/pi/temp3.txt", "r")
    TEMP_3_CELSIUS = f.read()
    return(TEMP_3_CELSIUS)

def get_temp4():
    f = open("/home/pi/temp4.txt", "r")
    TEMP_4_CELSIUS = f.read()
    return(TEMP_4_CELSIUS)

# In my setup probe 5 is outside the cooler area and therfore not relevant for cooler control. 
#def get_temp5():
#    f = open("/home/pi/temp5.txt", "r")
#    temp1inc = f.read()
#    return(TEMP_5_CELSIUS)

def get_temp6():
    f = open("/home/pi/temp6.txt", "r")
    TEMP_6_CELSIUS = f.read()
    return(TEMP_6_CELSIUS)

def get_temp7():
    f = open("/home/pi/temp7.txt", "r")
    TEMP_7_CELSIUS = f.read()
    return(TEMP_7_CELSIUS)  

def get_temp8():
    f = open("/home/pi/temp8.txt", "r")
    TEMP_8_CELSIUS = f.read()
    return(TEMP_8_CELSIUS)  

def get_avg_interior_temps():
  TEMP2 = int(float(get_temp2()))
  TEMP3 = int(float(get_temp3()))
  TEMP6 = int(float(get_temp6()))
  TEMP7 = int(float(get_temp7()))
  TEMP8 = int(float(get_temp8()))

  AVG_TEMP_IN_C = ((TEMP2 + TEMP3 + TEMP6 + TEMP7 + TEMP8) / 5)
  AVG_TEMP_IN_F = (AVG_TEMP_IN_C * (9/5) +32)

  return(AVG_TEMP_IN_F)

def get_heater_temp():
    HEATER_TEMP = get_current_heater_temp()


def get_intake_finns_temp():
    TEMP4 = int(float(get_temp4()))

def turn_off_liar():
    #taken from the off-gpio1.py
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, GPIO.HIGH)

def turn_on_liar():
    #taken from the on-gpio1.py
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, GPIO.LOW)

def turn_off_ac_power():
    #taken from off-gpio2.py
    GPIO.setup(22, GPIO.OUT)
    GPIO.output(22, GPIO.HIGH)

def turn_on_ac_power():
    #taken from on-gpio2.py
    GPIO.setup(22, GPIO.OUT)
    GPIO.output(22, GPIO.LOW)

def main():
    AVG_TEMP_IN_F = get_avg_interior_temps()
    if AVG_TEMP_IN_F > 42:
        turn_on_liar()
        print("I turned on the liar")
    if AVG_TEMP_IN_F < 38:
        turn_off_liar()
        print("I turned off the liar")
    print(f"The current temperature in F is", AVG_TEMP_IN_F)
main()
