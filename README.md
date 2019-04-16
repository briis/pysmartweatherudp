# pySmartWeatherUDP
Python 2 and 3 module to interact via UDP with a Smart Weather station from WeatherFlow

![GitHub release](https://img.shields.io/github/release/briis/pysmartweatherudp.svg)

This module communicates with a Smart Home Weather station from the company [WeatherFlow](http://weatherflow.com/smart-home-weather-stations/) using the UDP API. It retrieves current weather data from the attached units. Currently there are two types of Units:
* **AIR** - This unit measures Temperature, Humidity, Pressure and Lightning Strikes
* **SKY** - This unit measures Precipitation, Wind, Illuminance and UV
They are both attached to a central hub, that broadcasts the data via UDP and sends the data to a cloud database managed by WeatherFlow. This module retrieves the data by listening to the UDP broadcast on the local network.

There are several broadcasts being send by the system, and currently this module only uses three of them:
* *rapid_wind* - This contains current wind speed and bearing, and is updated every 3 seconds
* *air_obs* - Here we get Temperature, Humidity, Pressure and Lightning Strikes. This sends out data every minute
* *sky_obs* - This is where we get Precipitation, Wind, Illuminance and UV. Also broadcasts every minute.

The function is built specifically to be used with [Home Assistant](https://www.home-assistant.io/), so data is formatted to suit that. But it might easily be modified for other purposes.

## Functions
The module exposes the following functions:<br>
### SWReceiver(host, port, units)
this will return a Data Class with all the data collected from a specific Station.<br>

**host**<br>
(string)(optional) The IP address to listen to.<br>
Default value: 0.0.0.0 (All IP addresses)

**port**<br>
(integer)(Optional) The broadcast port to listen to. WeatherFlow only sends data to port 50222<br>
Default value: 50222

**units**<br>
(string)(optional) The unit system to use. Metric or Imperial<br>
Default value: Metric<br>

**Data Class Definition**<br>
* **timestamp** - Time of last update in EPOCH time
* **temperature** - Current temperature. **Note:** As this module was designed to be used with Home Assistant, no Temperature conversion will take place, even if *units* are supplied when calling the module. Temperatures will always be Celsius.
* **feels_like** - How the temperature Feels Like. A combination of Heat Index and Wind Chill
* **heat_index** - A temperature measurement combining Humidity and temperature. How hot does it feel. Only used when temperature is above 26.67°C (80°F)
* **wind_chill** - How cold does it feel. Only used if temperature is below 10°C (50°F)
* **dewpoint** - Dewpoint. The atmospheric temperature (varying according to pressure and humidity) below which water droplets begin to condense and dew can form
* **wind_speed** - Average Wind Speed for the last minute
* **wind_speed_rapid** - Current Wind Speed
* **wind_gust** - Highest Wind Speed in the last minute
* **wind_lull** - Lowest Wind Speed in the last minute
* **wind_bearing** - Average Wind bearing in degrees for the last minute (Example: 287°)
* **wind_bearing_rapid** - Current Wind bearing in degrees (Example: 287°)
* **wind_direction** - Wind bearing as directional text (Example: NNW)
* **precipitation** - Precipitation since midnight. Due to the nature of the UDP data, this number is calculated in memory. So if the module is restarted, the counter goes back to 0. Unfortunately it is not possible to catch up the data after a restart
* **precipitation_rate** - The current precipitation rate - 0 if it is not raining
* **humidity** - Current humidity in %
* **pressure** - Current barometric pressure, taking in to account the position of the station
* **uv** - The UV index
* **solar_radiation** - The current Solar Radiation measured in W/m2
* **illuminance** - Shows the brightness in Lux
* **lightning_count** - Shows the numbers of lightning strikes for last minute.
* **airbattery** - The current voltage of the AIR unit
* **skybattery** - The current voltage of the SKY unit
<hr>
