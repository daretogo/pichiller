# installing two module relay 

Since I already have these little two-relay modules it seems like taking advantage of both makes sense.  I'm going to use one switch to power the AC itself, and the other to turn on and off the AC->DC adapter that supplies the 9v power that runs through the "heater" probe. 

So a relay is pretty straight forward - it has 4 pins that wire up to the pi:
-Power (5v)
-GND
-In1
-In2

For our purposes, some really simple code can be used to turn the GPIO pins on/off:

```
pi@raspberrypi:~ $ cat off-gpio1.py 
#!/usr/bin/env python3

import time

import RPi.GPIO as GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.HIGH)
```


```
pi@raspberrypi:~ $ cat on-gpio1.py 
#!/usr/bin/env python3

import time

import RPi.GPIO as GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.LOW)
pi@raspberrypi:~ $ 

```

I do have two sets of these scripts, the only difference is the other one is on pin 22 instead of pin 27. 

Because I have one of the temperature probes mounted to the heater probe - I get temperature on how hot it gets when we turn on the GPIO pin and cause the 9v to flow through it. 
Later, we'll use this in overall control logic to selectively turn on the heater probe when we want the AC to continue to run.