#!/usr/bin/env python3

# Control script to run in a loop to maintain a target temperature of 38 to 40F

import time
from time import sleep
from time import strftime
import os
from  prometheus_client import Gauge, Counter, start_http_server
import pdb

#to support the turning on/off of the gpio pins that switch the relays for the AC and the power to the liar heating probe
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Create metrics for the turning on and turning off of the liar 
turned_off_liar = Counter('turned_off_liar', "A number which increments each time the control script turns off the liar heater probe")
turned_on_liar = Counter('turned_on_liar', "A number which increments each time the control script turns on the liar heater probe")

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
  TEMP6 = int(float(get_temp6()))
  TEMP7 = int(float(get_temp7()))
  TEMP8 = int(float(get_temp8()))

  AVG_TEMP_IN_C = ((TEMP2 + TEMP3 + TEMP6 + TEMP7 + TEMP8) / 5)
  AVG_TEMP_IN_F = (AVG_TEMP_IN_C * (9/5) +32)

  return(AVG_TEMP_IN_F)

def get_current_heater_temp():
    f = open("/home/pi/temp1.txt", "r")
    HEATER_PROBE_TEMP_CELSIUS = f.read()
    return(HEATER_PROBE_TEMP_CELSIUS)

def get_heater_temp():
    HEATER_TEMP = int(float(get_current_heater_temp()))
    return(HEATER_TEMP)


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
    start_http_server(8004)
    #pdb.set_trace()
    while True:
        try:
            AVG_TEMP_IN_F = get_avg_interior_temps()
            HEATER_TEMP_F = ((get_heater_temp()) * (9/5) +32)

            while HEATER_TEMP_F < 50:
                turn_on_liar()
                sleep(3)
                HEATER_TEMP_F = ((get_heater_temp()) * (9/5) +32)
            
            if AVG_TEMP_IN_F > 42:
                turn_on_liar()
                turned_on_liar.incr()
                print("I turned on the liar") 
                print(f"The current temperature in F is", AVG_TEMP_IN_F)
                print(strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))
                time.sleep(5)
                turn_off_liar()
                # # So we've detected we're over target temperature, and we want to cut on the AC, but if we run the AC for any length of time really we dip below target temp by too much.   So based on some observing, I think a minimum of 90 seconds will let the liar probe warm up enough to have cut the ac on. 
                # time.sleep(10)
                # # so now, at 90 seconds of the liar heater being on, we ant to start checking if it's above 65F to ensure the AC would have cut on.  (AC cuts on at 62 so there's some buffer)        
                # binary_liar_above_65 = 0        
                # while binary_liar_above_65 == 0:
                #     try:
                #         HEATER_TEMP_F = ((get_heater_temp()) * (9/5) +32)
                #         if HEATER_TEMP_F > 65:
                #             binary_liar_above_65 = 1
                #             #The liar heater is now warmer than 65, and presumably our AC will kick on - so let's turn off the liar to try to have a minimum cycle. 
                #             turn_off_liar()
                #             turned_off_liar.incr()
                #             print("I turned off the liar")
                #             print(f"The current temperature in F is", AVG_TEMP_IN_F)
                #             print(strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))
                #         time.sleep(5)
                #     except:
                #         pass
            if AVG_TEMP_IN_F < 38:
                while HEATER_TEMP_F < 50:
                    turn_on_liar()
                    HEATER_TEMP_F = ((get_heater_temp()) * (9/5) +32)
                    sleep(5)
                turn_off_liar()
                turned_off_liar.incr()
                print("I turned off the liar")
                print(f"The current temperature in F is", AVG_TEMP_IN_F)
                print(strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))
            time.sleep(5)
        except:
            pass
main()
