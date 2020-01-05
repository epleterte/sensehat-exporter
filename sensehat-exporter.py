#!/usr/bin/env python3
# Simple collector/exporter for Raspberry Pi SenseHat
#
# Copyright 2019 Christian Bryn <chr.bryn@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import argparse
import logging
import sys
import time
import signal

from prometheus_client import start_http_server, Metric, Summary, REGISTRY
from sense_hat import SenseHat

# logging setup
log = logging.getLogger('sensehat-exporter')
log.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

class SenseHatCollector():
    """ This sets up a custom collector for the SenseHat """
    def __init__(self, orientation=False):
        self.sense = SenseHat()
        self.orientation = orientation

    @REQUEST_TIME.time()
    def collect(self):
        """ Collect our metrics from the SenseHat """
        log.info('collecting metrics')

        temperature = self.sense.get_temperature()
        humidity = self.sense.get_humidity()
        pressure = self.sense.get_pressure()

        metric = Metric('rpi_sensehat', 'sensehat metric values', 'gauge')
        metric.add_sample('rpi_sensehat_temperature', value=temperature, labels={'name': 'SenseHat Temperature'})
        metric.add_sample('rpi_sensehat_humidity', value=humidity, labels={'name': 'SenseHat Humidity'})
        metric.add_sample('rpi_sensehat_pressure', value=pressure, labels={'name': 'SenseHat Pressure'})
        if self.orientation:
            roll = self.sense.orientation['roll']
            yaw = self.sense.orientation['yaw']
            pitch = self.sense.orientation['pitch']
            metric.add_sample('rpi_sensehat_roll', value=roll, labels={'name': 'SenseHat Roll'})
            metric.add_sample('rpi_sensehat_yaw', value=yaw, labels={'name': 'SenseHat Yaw'})
            metric.add_sample('rpi_sensehat_pitch', value=pitch, labels={'name': 'SenseHat Pitch'})

        yield metric


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--port', nargs='?', const=9101, help='The TCP port to listen on', default=9101)
    parser.add_argument('--bind', nargs='?', const='0.0.0.0', help='The interface/IP to bind to', default='0.0.0.0')
    parser.add_argument('--orientation', help='Output orientation data', action='store_true')
    parser.set_defaults(orientation=False)
    args = parser.parse_args()
    log.info('listening on http://%s:%d/metrics', args.bind, int(args.port))

    REGISTRY.register(SenseHatCollector(orientation=args.orientation))
    start_http_server(int(args.port), addr=args.bind)

    while True:
        signal.pause()
