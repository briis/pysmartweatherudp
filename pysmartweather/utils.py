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
        # Rapid Wind Data
        self.type = 'rapid_wind'
        self.timestamp = data[0]
        self.wind_speed = data[1]
        self.wind_bearing = data[2]
        # Air Data
        self.pressure = 0
        self.temperature = 0
        self.humidity = 0
        self.lightning_count = 0
        self.lightning_distance = 0
        self.airbattery = 0
        # Sky Data
        self.illuminance = 0
        self.uv = 0
        self.precipitation_rate = 0
        self.wind_lull = 0
        self.wind_gust = 0
        self.skybattery = 0
        self.solar_radiation = 0

class SkyOberservation:
    """ Returns the SKY Observation Dataset. """
    def __init__(self, data):
        # Sky Data
        self.type = 'sky'
        self.timestamp = data[0]
        self.illuminance = data[1]
        self.uv = data[2]
        self.precipitation_rate = data[3]
        self.wind_lull = data[4]
        self.wind_gust = data[6]
        self.skybattery = data[8]
        self.solar_radiation = data[10]
        # Air Data
        self.pressure = 0
        self.temperature = 0
        self.humidity = 0
        self.lightning_count = 0
        self.lightning_distance = 0
        self.airbattery = 0
        # Rapid Wind Data
        self.wind_speed = 0
        self.wind_bearing = 0

class AirOberservation:
    """ Returns the AIR Observation Dataset. """
    def __init__(self, data):
        # Air Data
        self.type = 'air'
        self.timestamp = data[0]
        self.pressure = data[1]
        self.temperature = data[2]
        self.humidity = data[3]
        self.lightning_count = data[4]
        self.lightning_distance = data[5]
        self.airbattery = data[6]
        # Sky Data
        self.illuminance = 0
        self.uv = 0
        self.precipitation_rate = 0
        self.wind_lull = 0
        self.wind_gust = 0
        self.skybattery = 0
        self.solar_radiation = 0
        # Rapid Wind Data
        self.wind_speed = 0
        self.wind_bearing = 0
