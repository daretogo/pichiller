# pichiller
A standard home window AC unit is quite powerful, and with a little finess can serve as the cooling source of a DIY "walk in cooler".   The goal of the pichiller is to provide a platform for controlling and temperature logging for this walk in cooler.  Additional non temperature features like detecting a door being left open are desired too. 

## Why?
There is a commercial product offered for sale for an obsenely high $400 price point that is designed to allow a user to leverage the cooling power of a window AC unit to create a walk in cooler.  It is the goal of this pichiller repo to do the same thing for way cheaper using a raspberry pi and some cheap off the shelf sensors. 

end goal:  hopefully a easy to setup software package to support a custom raspberry pi hat that can serve as a easy to use substitute for that commercial product I mentioned. 

## Following along

Start here with our [first one wire readings](1-first-one-wire-readings.md) where you'll wire up some DS18B20 temperature sensors and install a python service to read them and offer the temperature as a prometheus formatted metrics. 

From there, we move on [to installing Prometheus on our pi and setting it to collect the metrics](2-install-prometheus-collect-temps.md) from the service we just set up. 

Now that we're getting temperature metrics into Prometheus - we can ask prometheus to send those metrics up to grafana cloud.   Grafana cloud has a free tier that seems to be sufficient for these purposes. 

By [sending my metrics over to grafana cloud](3-sending-metrics-to-grafana-cloud.md), I'll be able to plot them visually on a dashboard that I can access from my phone even when I'm out and about, and they have alerting rules that tie into discord so I can get alerts if a temp is too high or too low (or if it's not logging data). 


The core idea of how you make a Window AC unit cool down to refridgerator type temperatures is that you "lie" to the Window unit by convincing it that it's actually warmer than it really is.  You do that by finding the temperature probe on the AC unit - and mating it up with a little heater. 

So what I did was I ordered some 3W 100Ohm resistors which are these super fat little resistors, and after some experimenting I found that if I hooked up this old 9v 500ma power supply through it then it would heat up to the 100F+ range, but not get too crazy hot.  I did also get a little real world experience with this and a 7v power supply was insufficient.  

So anyways - we need to be able to swtich power to this "heater" on and off so as to be able to heat up the Window AC probe to keep it running even when the temp gets below like 62 where it wants to shut off. 

Another thing it seems that it would be good to control is the power to the AC unit itself. 
I've got these Sainsmart 2 relay modules, so we're gonna [install a two relay module](4-install-two-relay-module.md) one side will switch the heater probe, the other will power the AC itself. 

I'm also somewhat interested in humidity data inside my cooler, eventually that could be more important if I was to get into aging cheeses or something but at the very least I'm thinking it'd be good to ensure the humidity level doesn't get too high as that could promote rot or mold.  I picked up a DHT22 sensor for getting this data.  The DHT22 will actually report both temperature and humidity so this will be our sixth temperature sensor but first humidity. So lets [add this dht22 sensor and get data from it](5-report-humidity-from-dh22-sensor.md)
