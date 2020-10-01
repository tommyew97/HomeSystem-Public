import pyowm

class Weather:

    def __init__(self):
        self.API_key = 'dc16fa4105c1a84697ec66d16e2e1521'

    def get_weather(self):
        owm = pyowm.OWM(self.API_key)
        mgr = owm.weather_manager()
        weather = mgr.weather_at_place('Trondheim,NO').weather
        temp_dict_celsius = weather.temperature('celsius')
        return str(round(temp_dict_celsius['temp'], 1))

    def min_max_weather(self):
        owm = pyowm.OWM(self.API_key)
        mgr = owm.weather_manager()
        weather = mgr.weather_at_place('Trondheim,NO').weather
        temp_dict_celsius = weather.temperature('celsius')
        result = str(round(temp_dict_celsius["temp_min"], 1)) + "C " + str(round(temp_dict_celsius["temp_max"], 1)) + "C"
        return result

    def weather_handler(self, command):
        print(command)
        if command == "now":
            return self.get_weather()
        elif command == "min_max":
            return self.min_max_weather()
