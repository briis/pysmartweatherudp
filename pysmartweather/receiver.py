"""
Interface to receive UDP packages from a Smart Weather station.
"""
# pylint: disable=import-error
import os
import select
import socket
import sys
import json
import threading
import time
import datetime

from . import utils

from .constants import (
    DEFAULT_HOST,
    DEFAULT_PORT
)

class SWReceiver(threading.Thread):
    """ Open a UDP socket to monitor for incoming packets. """

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        """Construct a Smart Weather interface object."""
        threading.Thread.__init__(self)
        self.stopped = threading.Event()
        self._callbacks = []
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        self._socket.bind((host, port))
        self._state = 'idle'

        """ Variables to store last read state. """
        # Air Data
        self._pressure = 0
        self._temperature = 0
        self._humidity = 0
        self._lightning_count = 0
        self._lightning_distance = 0
        self._airbattery = 0
        # Sky Data
        self._precipitation = 0
        self._precipitation_rate = 0
        self._precipitation_date = datetime.datetime.today().strftime('%Y-%m-%d')
        self._illuminance = 0
        self._uv = 0
        self._wind_lull = 0
        self._wind_gust = 0
        self._skybattery = 0
        self._solar_radiation = 0
        # Rapid Wind Data
        self._wind_bearing = 0
        self._wind_speed = 0

    def registerCallback(self, callback):
        self._callbacks.append(callback)

    def run(self):
        """Main loop of Smart Weather thread."""
        while not self.stopped.isSet():
            try:
                # if the current state is idle, just block and wait forever
                # if the current state is any other state, then a timeout of 200ms should
                # be reasonable in all cases.
                timeout = (self._state != 'idle') and 0.2 or None
                rdlist, _, _ = select.select([self._socket.fileno()], [], [], timeout)
                if not rdlist:
                    if self._state != 'idle':
                        self._state = 'idle'
                    continue
                data = self._socket.recv(1024)
                if not data:
                    # check if the socket is still valid
                    try:
                        os.fstat(recv._socket.fileno())
                    except socket.error:
                        break
                    continue

                ds = utils.getDataSet(data, ignore_errors=True)
                jsondata = json.loads(data)
                if jsondata['type'] == 'rapid_wind':
                    ds.precipitation = self._precipitation
                    ds.precipitation_rate = self._precipitation_rate
                    ds.temperature = self._temperature
                    ds.airbattery = self._airbattery
                    ds.skybattery = self._skybattery
                    self._wind_bearing = ds.wind_bearing
                    self._wind_speed = ds.wind_speed
                elif jsondata['type'] == 'obs_sky':
                    ds.temperature = self._temperature
                    ds.wind_bearing = self._wind_bearing
                    ds.wind_speed = self._wind_speed
                    ds.airbattery = self._airbattery
                    self._skybattery = ds.skybattery
                    self._precipitation_rate = ds.precipitation_rate
                    # Reset the Precipitation at Midnight
                    if datetime.datetime.fromtimestamp(ds.timestamp).strftime('%Y-%m-%d') != self._precipitation_date:
                        self._precipitation_date = datetime.datetime.fromtimestamp(ds.timestamp).strftime('%Y-%m-%d')
                        self._precipitation = 0
                    self._precipitation = self._precipitation + ds.precipitation_rate
                elif jsondata['type'] == 'obs_air':
                    ds.wind_bearing = self._wind_bearing
                    ds.wind_speed = self._wind_speed
                    ds.precipitation = self._precipitation
                    ds.precipitation_rate = self._precipitation_rate
                    ds.skybattery = self._skybattery
                    self._airbattery = ds.airbattery
                    self._temperature = ds.temperature
                else:
                    ds = None

                if ds:
                    for callback in self._callbacks:
                        callback(ds)
            except:
                time.sleep(0.1)

    def stop(self):
        self.stopped.set()
        # force receiver thread to wake from select
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((self.host, self.port))
        msg = "stop"
        datagram = sys.version_info[0] == 2 and bytes(msg) or bytes(msg, "utf-8")
        sock.send(datagram)
        sock.close()
        self.join()
        self._socket.close()
