## Installing prometheus 

So since we can now visit http://192.168.1.106:8001 and see the current temperature reading lets start capturing those readings and storing the data with prometheus. 

Since I'm running a rPi 3 that means I need Armv7 builds of prometheus, but they publish Armv6 builds so I think if you were running an Rpi2 or a Rpi Zero you could use the ArmV6 builds with these same instructions. 

First I'd pop over to https://github.com/prometheus/prometheus/releases/ and see what the latest release of prometheus is.  As of the time of me writing this it was 2.30.0 so I grabbed the download link and then use `wget` to pull it down and then unpack it. I also create a symbolic link from /home/pi/prometheus to the specific version found in /home/pi -  hopefully this makes an upgrade in the future easier...

```
wget https://github.com/prometheus/prometheus/releases/download/v2.30.0/prometheus-2.30.0.linux-armv7.tar.gz
gunzip -c prometheus-2.30.0.linux-armv7.tar.gz | tar -xvf -
pi@raspberrypi:~ $ rm prometheus-2.30.0.linux-armv7.tar.gz 
pi@raspberrypi:~ $ ln -s prometheus-2.30.0.linux-armv7/ prometheus

pi@raspberrypi:~ $ ls -l
total 8
lrwxrwxrwx 1 pi pi   30 Sep 18 20:09 prometheus -> prometheus-2.30.0.linux-armv7/
drwxr-xr-x 4 pi pi 4096 Sep 14 11:28 prometheus-2.30.0.linux-armv7
-rwxr-xr-x 1 pi pi 1864 Sep 18 19:44 tempexporter.py
```

So now we need a service to start prometheus and keep it running, and restart it when the pi reboots. 

```
sudo vi /etc/systemd/system/prometheus.service

[Unit]
Description=Prometheus Server
Documentation=https://prometheus.io/docs/introduction/overview/
After=network-online.target

[Service]
User=pi
Restart=on-failure

ExecStart=/home/pi/prometheus/prometheus \
  --config.file=/home/pi/prometheus/prometheus.yml \
  --storage.tsdb.path=/home/pi/prometheus/data

[Install]
WantedBy=multi-user.target

```

Now, we can daemon reload, enable, and start the prometheus service:

```
pi@raspberrypi:~/prometheus $ sudo systemctl daemon-reload
pi@raspberrypi:~/prometheus $ sudo systemctl enable prometheus
Created symlink /etc/systemd/system/multi-user.target.wants/prometheus.service → /etc/systemd/system/prometheus.service.
pi@raspberrypi:~/prometheus $ sudo systemctl start prometheus
pi@raspberrypi:~/prometheus $ sudo systemctl status prometheus
● prometheus.service - Prometheus Server
   Loaded: loaded (/etc/systemd/system/prometheus.service; enabled; vendor preset: enabled)
   Active: active (running) since Sat 2021-09-18 20:14:39 BST; 6s ago
     Docs: https://prometheus.io/docs/introduction/overview/
 Main PID: 7486 (prometheus)
    Tasks: 9 (limit: 2200)
   Memory: 14.2M
   CGroup: /system.slice/prometheus.service
           └─7486 /home/pi/prometheus/prometheus --config.file=/home/pi/prometheus/prometheus.yml --storage.tsdb.path=/home/pi

Sep 18 20:14:39 raspberrypi prometheus[7486]: level=info ts=2021-09-18T19:14:39.262Z caller=head.go:466 component=tsdb msg="Re
Sep 18 20:14:39 raspberrypi prometheus[7486]: level=info ts=2021-09-18T19:14:39.262Z caller=head.go:500 component=tsdb msg="On
Sep 18 20:14:39 raspberrypi prometheus[7486]: level=info ts=2021-09-18T19:14:39.262Z caller=head.go:506 component=tsdb msg="Re
Sep 18 20:14:39 raspberrypi prometheus[7486]: level=info ts=2021-09-18T19:14:39.263Z caller=head.go:577 component=tsdb msg="WA
Sep 18 20:14:39 raspberrypi prometheus[7486]: level=info ts=2021-09-18T19:14:39.263Z caller=head.go:583 component=tsdb msg="WA
Sep 18 20:14:39 raspberrypi prometheus[7486]: level=info ts=2021-09-18T19:14:39.271Z caller=main.go:849 fs_type=EXT4_SUPER_MAG
Sep 18 20:14:39 raspberrypi prometheus[7486]: level=info ts=2021-09-18T19:14:39.272Z caller=main.go:852 msg="TSDB started"
Sep 18 20:14:39 raspberrypi prometheus[7486]: level=info ts=2021-09-18T19:14:39.272Z caller=main.go:979 msg="Loading configura
Sep 18 20:14:39 raspberrypi prometheus[7486]: level=info ts=2021-09-18T19:14:39.274Z caller=main.go:1016 msg="Completed loadin
Sep 18 20:14:39 raspberrypi prometheus[7486]: level=info ts=2021-09-18T19:14:39.275Z caller=main.go:794 msg="Server is ready t
lines 1-20/20 (END)
```

Now with prometheus running, we should be able to visit that same IP address of the pi from earlier but on port 9090 and see the prometheus UI:

![screen showing prometheus UI on localhost port 9090](/images/prometheus_ui.jpg)

But if we search the instance for out metrics "ds18b20_1_temperature_celsius" you will not find them.  That's because despite the metrics being on the same pi, the Prometheus instance hasn't been told that it shoudl go collect those metrics.    For this, we need a very simple modification to the prometheus configuration file:

```
cd /home/pi/prometheus/
vi prometheus.yml
```
Note at the bottom couple of lines of the configuration you'll see the existing target list for collecting metrics: 

```
static_configs:
    - targets: ["localhost:9090"]

```
We extend this list by adding our local port 8001 that we're offering our temperature metrics on:

```
static_configs:
    - targets: ['localhost:9090','localhost:8001']
```

After modifying anda dding the new  target, we need to restart promethues `sudo systemctl restart prometheus` to get it to read the new config. 
Then, post restart when we visit the prometheus UI - we should be able to search for our temperature metrics and see them return in the prometheus UI:

![example of prom ui showing  prometheus metrics from our temp exporter](/images/prom_ui_with_temp_metrics.jpg)
