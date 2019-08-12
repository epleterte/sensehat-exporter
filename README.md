Sensehat Prometheus Exporter
============================

A simple Prometheus exporter for exporting values from the Raspberry Pi SenseHat.


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


TODO
----

* Export more sensor data - currently only temperature, humidity and pressure is exported.
* Possibly make additional sensors configurable.

License
-------

This software is licensed under the ISC license.
