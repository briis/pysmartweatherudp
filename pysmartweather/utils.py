""" Utility Functions used with pysmartweather. """
import datetime
import json
import math


def getDataSet(data, units, ignore_errors=False):
    """ Returns a the specic dataset from raw data. """
    try:
        jsondata = json.loads(data)

        if jsondata['type'] == 'rapid_wind':
            return RapidWind(jsondata['ob'], units)
        elif jsondata['type'] == 'obs_sky':
            return SkyOberservation(jsondata['obs'][0], units)
        elif jsondata['type'] == 'obs_air':
            return AirOberservation(jsondata['obs'][0], units)
        else:
            return None
    except:
        if not ignore_errors:
            raise

class RapidWind:
    """ Return the Rapid Wind data Structure. """
    def __init__(self, data, units):
        # Rapid Wind Data
        self.type = 'rapid_wind'
        self.timestamp = data[0]
        self.wind_speed = UnitConversion.speed(data[1], units)
        self.wind_bearing = data[2]
        self.wind_direction = UnitConversion.wind_direction(data[2])
        # Air Data
        self.pressure = 0
        self.temperature = 0
        self.humidity = 0
        self.lightning_count = 0
        self.lightning_distance = 0
        self.lightning_time = None
        self.airbattery = 0
        self.dewpoint = 0
        # Sky Data
        self.illuminance = 0
        self.uv = 0
        self.precipitation_rate = 0
        self.wind_lull = 0
        self.wind_gust = 0
        self.skybattery = 0
        self.solar_radiation = 0
        # Calculated Values
        self.wind_chill = 0

class SkyOberservation:
    """ Returns the SKY Observation Dataset. """
    def __init__(self, data, units):
        # Sky Data
        self.type = 'sky'
        self.timestamp = data[0]
        self.illuminance = data[1]
        self.uv = data[2]
        self.precipitation_rate = UnitConversion.volume(data[3], units)
        self.wind_lull = UnitConversion.speed(data[4], units)
        self.wind_gust = UnitConversion.speed(data[6], units)
        self.skybattery = data[8]
        self.solar_radiation = data[10]
        # Air Data
        self.pressure = 0
        self.temperature = 0
        self.humidity = 0
        self.lightning_count = 0
        self.lightning_distance = 0
        self.lightning_time = None
        self.airbattery = 0
        self.dewpoint = 0
        # Rapid Wind Data
        self.wind_speed = 0
        self.wind_bearing = 0
        self.wind_direction = None
        # Calculated Values
        self.wind_chill = 0

class AirOberservation:
    """ Returns the AIR Observation Dataset. """
    def __init__(self, data, units):
        # Air Data
        self.type = 'air'
        self.timestamp = data[0]
        self.pressure = UnitConversion.pressure(data[1], units)
        self.temperature = data[2]
        self.humidity = data[3]
        self.lightning_count = data[4]
        self.lightning_distance = UnitConversion.distance(data[5], units)
        self.lightning_time = datetime.datetime.today().strftime('%Y-%m-%d') if data[4] > 0 else None
        self.airbattery = data[6]
        self.dewpoint = WeatherFunctions.getDewPoint(data[2], data[3])
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
        self.wind_direction = None
        # Calculated Values
        self.wind_chill = 0

class UnitConversion:
    """
    Conversion Class to convert between different units.
    WeatherFlow always delivers values in the following formats:
    Temperature: C
    Wind Speed: m/s
    Wind Direction: Degrees
    Pressure: mb
    Distance: km
    """
    def volume(value, unit):
        if unit.lower() == 'imperial':
            # Return value in
            return round(value * 0.0393700787,2)
        else:
            # Return value mm
            return round(value,1)

    def pressure(value, unit):
        if unit.lower() == 'imperial':
            # Return value inHg
            return round(value * 0.0295299801647,3)
        else:
            # Return value mb
            return round(value,1)

    def speed(value, unit):
        if unit.lower() == 'imperial':
            # Return value in mi/h
            return round(value*2.2369362921,1)
        else:
            # Return value in m/s
            return round(value,1)

    def distance(value, unit):
        if unit.lower() == 'imperial':
            # Return value in mi
            return round(value*0.621371192,1)
        else:
            # Return value in m/s
            return round(value,0)

    def wind_direction(bearing):
        direction_array = ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW','N']
        direction = direction_array[int((bearing + 11.25) / 22.5)]
        return direction

class WeatherFunctions:
    """ Weather Specific Math Functions. """
    def getDewPoint(temperature, humidity):
        return round(243.04*(math.log(humidity/100)+((17.625*temperature)/(243.04+temperature)))/(17.625-math.log(humidity/100)-((17.625*temperature)/(243.04+temperature))),1)

    def getWindChill(wind_speed, temperature):
        if wind_speed < 1.3:
            return temperature
        else:
            return round((12.1452 + 11.6222 * math.sqrt(wind_speed) - 1.16222 * wind_speed) * (33 - temperature),2)
