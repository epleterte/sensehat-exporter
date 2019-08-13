Sensehat Prometheus Exporter
============================

A simple Prometheus exporter for exporting values from the Raspberry Pi SenseHat.

Requirements
------------

* Raspberry Pi (3/3+/4)
* [Rasperry Pi SenseHat](https://www.raspberrypi.org/products/sense-hat/)

Installation
------------

    git clone https://github.com/epleterte/sensehat-exporter.git
    cd sensehat-exporter
    pip3 install -r requirements.txt
    sudo cp sensehat-exporter.py /usr/local/bin/sensehat-exporter
    # start sensehat-exporter!
    sensehat-exporter

### Run as a service

    cp sensehat-exporter.service.example /etc/systemd/system/sensehat-exporter.service
    systemctl daemon-reload
    systemctl start sensehat-exporter
    systemctl enable sensehat-exporter

Usage
-----

    usage: simpleexporter.py [-h] [--port [PORT]] [--bind [BIND]]
    
    optional arguments:
      -h, --help     show this help message and exit
      --port [PORT]  The TCP port to listen on (default: 9101)
      --bind [BIND]  The interface/IP to bind to (default: 0.0.0.0)

Configuration
-------------

Currently there are no other configuration than options IP/port and no configuration file.

Prometheus Configuration
------------------------

In _/etc/prometheus/prometheus.yml_, Add a static scrape target under `scrape_configs`:

    scrape_configs:
      - job_name: 'sensehat'
        static_configs:
        - targets: ['<ip>:9101'] 

    
TODO
----

* Upload example Grafana dashboard
* Export more sensor data - currently only temperature, humidity and pressure is exported.
* Possibly make additional sensors configurable.

Demo
----

Here's a screenshot of the data being put to use in a Grafana dashboard:

![Grafana RPi Sensehat dashboard screenshot][images/screenshot_2019-08-13.png]

License
-------

This software is licensed under the ISC license.
