""" Utility Functions used with pysmartweather. """
import datetime
import json

def getDataSet(data, ignore_errors=False):
    """ Returns a formatted dataset from raw data. """

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

class SkyOberservation:
    """ Returns the SKY Observation Dataset. """
    def __init__(self, data):
        self.type = 'sky'
        self.timestamp = data[0]
        self.illuminance = data[1]
        self.uv = data[2]
        self.rain_rate = data[3]
        self.wind_lull = data[4]
        self.wind_gust = data[6]
        self.battery = data[8]
        self.solar_radiation = data[10]
        self.precipitation = data[11]

class AirOberservation:
    """ Returns the AIR Observation Dataset. """
    def __init__(self, data):
        self.type = 'air'
        self.timestamp = data[0]
        self.pressure = data[1]
        self.temperature = data[2]
        self.humidity = data[3]
        self.lightning_count = data[4]
        self.lightning_distance = data[5]
        self.battery = data[6]
