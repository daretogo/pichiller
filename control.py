#!/usr/bin/env python3

# Control script to run in a loop to maintain a target temperature of 38 to 40F

import time
from time import sleep
from time import strftime
import os
from  prometheus_client import Gauge, Counter, start_http_server
import pdb
import logging

logging.basicConfig(filename='/home/pi/control.log', level=logging.INFO)

#to support the turning on/off of the gpio pins that switch the relays for the AC and the power to the liar heating probe
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Create metrics for the turning on and turning off of the liar 
turned_off_liar = Counter('turned_off_liar', "A number which increments each time the control script turns off the liar heater probe")
turned_on_liar = Counter('turned_on_liar', "A number which increments each time the control script turns on the liar heater probe")
avg_temp_f_control = Gauge('avg_temp_f_control', "Temperature in F as calculated by the control script")

# We need current temperature data

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
  #Temp4 is the probe right across the intake finns of the AC
  TEMP6 = int(float(get_temp6()))
  TEMP7 = int(float(get_temp7()))
  #Temp8 is the probe in the 5 gallon bucket of water. 

  AVG_TEMP_IN_C = ((TEMP2 + TEMP3 + TEMP6 + TEMP7) / 4)
  AVG_TEMP_IN_F = (AVG_TEMP_IN_C * (9/5) +32)

  logging.debug('AVG_TEMP_IN_C: %s', AVG_TEMP_IN_C )
  logging.debug('AVG_TEMP_IN_F: %s', AVG_TEMP_IN_F )

  return(AVG_TEMP_IN_F)

def get_current_heater_temp():
    f = open("/home/pi/temp1.txt", "r")
    HEATER_PROBE_TEMP_CELSIUS = f.read()
    return(HEATER_PROBE_TEMP_CELSIUS)

def get_heater_temp():
    HEATER_TEMP = int(float(get_current_heater_temp()))
    logging.debug('HEATER_TEMP: %s', HEATER_TEMP)
    return(HEATER_TEMP)


def get_intake_finns_temp():
    TEMP4 = int(float(get_temp4()))

def turn_off_liar():
    #taken from the off-gpio1.py
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, GPIO.HIGH)
    logging.debug('turn_off_liar')

def turn_on_liar():
    #taken from the on-gpio1.py
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, GPIO.LOW)
    logging.debug('turn_on_liar')

def turn_off_ac_power():
    #taken from off-gpio2.py
    GPIO.setup(22, GPIO.OUT)
    GPIO.output(22, GPIO.HIGH)
    logging.debug('turn_off_ac')

def turn_on_ac_power():
    #taken from on-gpio2.py
    GPIO.setup(22, GPIO.OUT)
    GPIO.output(22, GPIO.LOW)
    logging.debug('turn_on_ac')


def turn_on_heater_if_its_below_45():
    HEATER_TEMP_F = ((get_heater_temp()) * (9/5) +32)
    if HEATER_TEMP_F < 45:
        turn_on_liar()

def turn_on_heater_if_its_below_65():
    HEATER_TEMP_F = ((get_heater_temp()) * (9/5) +32)
    if HEATER_TEMP_F < 65:
        turn_on_liar()


def turn_off_heater_if_its_above_45():
    HEATER_TEMP_F = ((get_heater_temp()) * (9/5) +32)
    if HEATER_TEMP_F > 45:
        turn_off_liar()

def turn_off_heater_if_its_above_80():
    HEATER_TEMP_F = ((get_heater_temp()) * (9/5) +32)
    if HEATER_TEMP_F > 80:
        turn_off_liar()


def maintain_50F_at_liar():
    HEATER_TEMP_F = ((get_heater_temp()) * (9/5) +32)
    if HEATER_TEMP_F < 50:
        turn_on_liar()
    if HEATER_TEMP_F > 50:
        turn_off_liar()

def maintain_70F_at_liar():
    HEATER_TEMP_F = ((get_heater_temp()) * (9/5) +32)
    if HEATER_TEMP_F < 70:
        turn_on_liar()
    if HEATER_TEMP_F > 70:
        turn_off_liar()


def main():
    start_http_server(8004)
    #pdb.set_trace()
    while True:
        try:
            AVG_TEMP_IN_F = get_avg_interior_temps()
            logging.info('AVG_TEMP_IN_F: %s', AVG_TEMP_IN_F)
            avg_temp_f_control.set(AVG_TEMP_IN_F)
            
            #We believe the AC will turn off when it's probe is below 62F
            #We believe the AC will turn on when it's probe is above 62F

            #Let's make it our goal to maintian a temperature of 50F, so we don't have to climb much to turn 
            maintain_50F_at_liar()
            logging.info('Defaut set liar to 50F')
            

            #Now, when the cooler temp is above our target temp of 48F we want the AC to come on
            if AVG_TEMP_IN_F > 48:
                turn_on_ac_power()
                maintain_70F_at_liar()
                logging.info('Temp was greater than 48F, turned on AC and set liar to 70F')

            #Once we've cooled off, and the temp is below our target temp of 48F we want the AC to go off
            if AVG_TEMP_IN_F < 48:
                maintain_50F_at_liar()
                logging.info('Temp was less than 48F, set liar to 50F')

            #So it seems even a minimum cycle time cooling is too much - we have to cut it short by powering off the AC
            #and when we do this, we keep the AC off for at least 1 minute to give time for pressure equalization. 
            if AVG_TEMP_IN_F < 38:
                turn_off_ac_power()
                turn_off_liar
                logging.info('Temp was less than 38F, turned off AC, turn off liar. Also going to sleep for 60 seconds.')
                time.sleep(60)
                logging.info('One Minute Safety Sleep complete, setting liar to 50F')
                maintain_50F_at_liar()

            if 48 > AVG_TEMP_IN_F > 38:
                logging.info('Temp greater than 38 but less than 48, so we are cooled, but likely warming.  Turn AC on, but dont set liar high enough to trigger it.')
                turn_on_ac_power()
                maintain_50F_at_liar()

            #For emergencies - if the temp gets this low then something has happened and we want to shut down and be off for 10 min. 
            if AVG_TEMP_IN_F < 20:
                logging.info('Temp was less than 20F, turned off AC power for safety and sleep for 10 minutes')
                turn_off_ac_power()
                time.sleep(600)
                logging.info('10 Minute Safety Sleep complete.')

            time.sleep(0.3)
        except:
            pass

main()