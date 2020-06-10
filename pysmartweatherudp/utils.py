""" Utility Functions used with pysmartweatherudp. """
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
        elif jsondata['type'] == 'obs_st':
            return StObservation(jsondata['obs'][0], units)
        else:
            return None
    except:
        if not ignore_errors:
            raise

class StObservation:
    """ Return the Combined Station data Structure. """
    def __init__(self, data, units):
        # Rapid Wind Data
        self.type = 'st'
        self.timestamp = data[0]
        self.illuminance = data[9]
        self.uv = data[10]
        self.precipitation_rate = UnitConversion.volume(self, data[12], units)
        self.wind_speed = UnitConversion.speed(self, data[2], units)
        self.wind_bearing = data[4]
        self.wind_lull = UnitConversion.speed(self, data[1], units)
        self.wind_gust = UnitConversion.speed(self, data[2], units)
        self.skybattery = data[16]
        self.solar_radiation = data[11]
        self.wind_direction = UnitConversion.wind_direction(self, data[4])
        # Air Data
        self.pressure = UnitConversion.pressure(self, data[6], units)
        self.temperature = round(data[7],1)
        self.humidity = data[8]
        self.lightning_count = data[15]
        self.lightning_distance = UnitConversion.distance(self, data[14], units)
        self.lightning_time = datetime.datetime.today().strftime('%Y-%m-%d') if data[15] > 0 else None
        self.airbattery = data[16]
        self.dewpoint = WeatherFunctions.getDewPoint(self, data[7], data[8])
        self.heat_index = WeatherFunctions.getHeatIndex(self, data[7], data[8])
        # Rapid Wind Data
        self.wind_speed_rapid = 0
        self.wind_bearing_rapid = 0
        # Calculated Values
        self.wind_chill = 0
        self.feels_like = 0

class RapidWind:
    """ Return the Rapid Wind data Structure. """
    def __init__(self, data, units):
        # Rapid Wind Data
        self.type = 'rapid_wind'
        self.timestamp = data[0]
        self.wind_speed_rapid = UnitConversion.speed(self, data[1], units)
        self.wind_bearing_rapid = data[2]
        # Air Data
        self.pressure = 0
        self.temperature = 0
        self.humidity = 0
        self.lightning_count = 0
        self.lightning_distance = 0
        self.lightning_time = None
        self.airbattery = 0
        self.dewpoint = 0
        self.heat_index = 0
        # Sky Data
        self.illuminance = 0
        self.uv = 0
        self.precipitation_rate = 0
        self.wind_speed = 0
        self.wind_bearing = 0
        self.wind_lull = 0
        self.wind_gust = 0
        self.skybattery = 0
        self.solar_radiation = 0
        self.wind_direction = None
        # Calculated Values
        self.wind_chill = 0
        self.feels_like = 0

class SkyOberservation:
    """ Returns the SKY Observation Dataset. """
    def __init__(self, data, units):
        # Sky Data
        self.type = 'sky'
        self.timestamp = data[0]
        self.illuminance = data[1]
        self.uv = data[2]
        self.precipitation_rate = UnitConversion.volume(self, data[3], units)
        self.wind_speed = UnitConversion.speed(self, data[5], units)
        self.wind_bearing = data[7]
        self.wind_lull = UnitConversion.speed(self, data[4], units)
        self.wind_gust = UnitConversion.speed(self, data[6], units)
        self.skybattery = data[8]
        self.solar_radiation = data[10]
        self.wind_direction = UnitConversion.wind_direction(self, data[7])
        # Air Data
        self.pressure = 0
        self.temperature = 0
        self.humidity = 0
        self.lightning_count = 0
        self.lightning_distance = 0
        self.lightning_time = None
        self.airbattery = 0
        self.dewpoint = 0
        self.heat_index = 0
        # Rapid Wind Data
        self.wind_speed_rapid = 0
        self.wind_bearing_rapid = 0
        # Calculated Values
        self.wind_chill = 0
        self.feels_like = 0

class AirOberservation:
    """ Returns the AIR Observation Dataset. """
    def __init__(self, data, units):
        # Air Data
        self.type = 'air'
        self.timestamp = data[0]
        self.pressure = UnitConversion.pressure(self, data[1], units)
        self.temperature = round(data[2],1)
        self.humidity = data[3]
        self.lightning_count = data[4]
        self.lightning_distance = UnitConversion.distance(self, data[5], units)
        self.lightning_time = datetime.datetime.today().strftime('%Y-%m-%d') if data[4] > 0 else None
        self.airbattery = data[6]
        self.dewpoint = WeatherFunctions.getDewPoint(self, data[2], data[3])
        self.heat_index = WeatherFunctions.getHeatIndex(self, data[2], data[3])
        # Sky Data
        self.illuminance = 0
        self.uv = 0
        self.precipitation_rate = 0
        self.wind_speed = 0
        self.wind_bearing = 0
        self.wind_lull = 0
        self.wind_gust = 0
        self.skybattery = 0
        self.solar_radiation = 0
        self.wind_direction = None
        # Rapid Wind Data
        self.wind_speed_rapid = 0
        self.wind_bearing_rapid = 0
        # Calculated Values
        self.wind_chill = 0
        self.feels_like = 0
        
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
    def volume(self, value, unit):
        if unit.lower() == 'imperial':
            # Return value in
            return value * 0.0393700787
        else:
            # Return value mm
            return value

    def pressure(self, value, unit):
        if unit.lower() == 'imperial':
            # Return value inHg
            return round(value * 0.0295299801647,3)
        else:
            # Return value mb
            return round(value,1)

    def speed(self, value, unit):
        if unit.lower() == 'imperial':
            # Return value in mi/h
            return round(value*2.2369362921,1)
        else:
            # Return value in m/s
            return round(value,1)

    def distance(self, value, unit):
        if unit.lower() == 'imperial':
            # Return value in mi
            return round(value*0.621371192,1)
        else:
            # Return value in m/s
            return round(value,0)

    def wind_direction(self, bearing):
        direction_array = ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW','N']
        direction = direction_array[int((bearing + 11.25) / 22.5)]
        return direction

class WeatherFunctions:
    """ Weather Specific Math Functions. """
    def getDewPoint(self, temperature, humidity):
        """ Returns Dew Point in Celcius """
        return round(243.04*(math.log(humidity/100)+((17.625*temperature)/(243.04+temperature)))/(17.625-math.log(humidity/100)-((17.625*temperature)/(243.04+temperature))),1)

    def getWindChill(self, wind_speed, temperature):
        """ Returns Wind Chill in Celcius """
        if wind_speed < 1.3:
            return round(temperature,1)
        else:
            windKmh = wind_speed * 3.6
            return round(13.12 + (0.6215 * temperature) - (11.37 * math.pow(windKmh, 0.16)) + (0.3965 * temperature * math.pow(windKmh, 0.16)), 1)

    def getHeatIndex(self, temperature, humidity):
        """ Returns Heat Index in Celcius """
        T = temperature * 9/5 + 32 #Convert to Fahrenheit
        RH = humidity
        c1 = -42.379
        c2 = 2.04901523
        c3 = 10.14333127
        c4 = -0.22475541
        c5 = -6.83783e-3
        c6 = -5.481717e-2
        c7 = 1.22874e-3
        c8 = 8.5282e-4
        c9 = -1.99e-6

        # try simplified formula first (used for HI < 80)
        HI = 0.5 * (T + 61. + (T - 68.) * 1.2 + RH * 0.094)

        if HI >= 80:
            # use Rothfusz regression
            HI = math.fsum([
                c1,
                c2 * T,
                c3 * RH,
                c4 * T * RH,
                c5 * T**2,
                c6 * RH**2,
                c7 * T**2 * RH,
                c8 * T * RH**2,
                c9 * T**2 * RH**2,
            ])

        # Return value in Celcius
        return round((HI - 32) * 5/9, 1)

    def getFeelsLike(self, temperature, wind_chill, heat_index):
        """ Returns the Feels Like Temperature in Celcius """
        if temperature > 26.666666667:
            return heat_index
        elif temperature < 10:
            return wind_chill
        else:
            return round(temperature,1)
