""" Utility Functions used with pysmartweather. """
import datetime
import json


def getDataSet(data, ignore_errors=False):
    """ Returns a the specic dataset from raw data. """
    try:
        jsondata = json.loads(data)

        if jsondata['type'] == 'rapid_wind':
            return RapidWind(jsondata['ob'])
        elif jsondata['type'] == 'obs_sky':
            return SkyOberservation(jsondata['obs'][0])
        elif jsondata['type'] == 'obs_air':
            return AirOberservation(jsondata['obs'][0])
        else:
            return None
    except:
        if not ignore_errors:
            raise

class RapidWind:
    """ Return the Rapid Wind data Structure. """
    def __init__(self, data):
        self.type = 'rapid_wind'
        self.timestamp = data[0]
        self.wind_speed = data[1]
        self.wind_bearing = data[2]
        self.temperature = 0
        self.precipitation_rate = 0
        self.airbattery = 0
        self.skybattery = 0

class SkyOberservation:
    """ Returns the SKY Observation Dataset. """
    def __init__(self, data):
        self.type = 'sky'
        self.timestamp = data[0]
        self.precipitation_rate = data[3]
        self.temperature = 0
        self.wind_speed = 0
        self.wind_bearing = 0
        self.airbattery = 0
        self.skybattery = data[8]

class AirOberservation:
    """ Returns the AIR Observation Dataset. """
    def __init__(self, data):
        self.type = 'air'
        self.timestamp = data[0]
        self.temperature = data[2]
        self.precipitation_rate = 0
        self.wind_speed = 0
        self.wind_bearing = 0
        self.airbattery = data[6]
        self.skybattery = 0
