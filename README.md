# pichiller
A standard home window AC unit is quite powerful, and with a little finess can serve as the cooling source of a DIY "walk in cooler".   The goal of the pichiller is to provide a platform for controlling and temperature logging for this walk in cooler.  Additional non temperature features like detecting a door being left open are desired too. 

## Why?
There is a commercial product offered for sale for an obsenely high $400 price point that is designed to allow a user to leverage the cooling power of a window AC unit to create a walk in cooler.  It is the goal of this pichiller repo to do the same thing for way cheaper using a raspberry pi and some cheap off the shelf sensors. 

## Following along

Start here with our [first one wire readings](1-first-one-wire-readings.md) where you'll wire up some DS18B20 temperature sensors and install a python service to read them and offer the temperature as a prometheus formatted metrics. 

From there, we move on [to installing Prometheus on our pi and setting it to collect the metrics](2-install-prometheus-collect-temps.md) from the service we just set up. 

