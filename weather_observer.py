"""
Final Implementation of WeatherData.  Complete all the TODOs
"""


class Subject:
    # Both of the following two methods take an
    # observer as an argument; that is, the observer
    # to be registered ore removed.
    def registerObserver(observer):
        pass

    def removeObserver(observer):
        pass

    # This method is called to notify all observers
    # when the Subject's state (measuremetns) has changed.
    def notifyObservers():
        pass

# The observer class is implemented by all observers,
# so they all have to implemented the update() method. Here
# we're following Mary and Sue's lead and
# passing the measurements to the observers.


class Observer:
    def update(self, temp, humidity, pressure):
        pass

# WeatherData now implements the subject interface.


class WeatherData(Subject):

    def __init__(self):
        self.observers = []
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0

    def registerObserver(self, observer):
        # When an observer registers, we just
        # add it to the end of the list.
        self.observers.append(observer)

    def removeObserver(self, observer):
        # When an observer wants to un-register,
        # we just take it off the list.
        self.observers.remove(observer)

    def notifyObservers(self):
        # We notify the observers when we get updated measurements
        # from the Weather Station.
        for ob in self.observers:
            ob.update(self.temperature, self.humidity, self.pressure)

    def measurementsChanged(self):
        self.notifyObservers()

    def setMeasurements(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

        self.measurementsChanged()

    # other WeatherData methods here.


class CurrentConditionsDisplay(Observer):

    def __init__(self, weatherData):
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0

        self.weatherData = weatherData  # save the ref in an attribute.
        weatherData.registerObserver(self)  # register the observer
        # so it gets data updates.

    def update(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.display()

    def display(self):
        print("Current conditions: \n", self.temperature,
              "F degrees and", self.humidity, "[%] humidity",
              "and pressure", self.pressure)

class StatisticsDisplay(Observer):

    def __init__(self, weatherData):
        self.temperatures = []
        self.temp_data = {}
        self.humidities = []
        self.humidity_data = {}
        self.pressures = []
        self.pressure_data = {}
        self.weatherData = weatherData
        weatherData.registerObserver(self)
    
    def update(self, temperature, humidity, pressure):
        self.temperatures.append(temperature)
        self.humidities.append(humidity)
        self.pressures.append(pressure)

        self.temp_data = self.get_temp_stats()
        self.humidity_data = self.get_humid_stats()
        self.pressure_data = self.get_pressure_stats()

        self.display()
    
    def display(self):
        print("Statistics:")
        print(f"Temperature: Max={self.temp_data['maximum']} Min={self.temp_data['minimum']} Avg={'{:.2f}'.format(self.temp_data['average'])}")
        print(f"Humidity: Max={self.humidity_data['maximum']} Min={self.humidity_data['minimum']} Avg={'{:.2f}'.format(self.humidity_data['average'])}")
        print(f"Pressure: Max={self.pressure_data['maximum']} Min={self.pressure_data['minimum']} Avg={'{:.2f}'.format(self.humidity_data['average'])}")

    def get_temp_stats(self):
        maximum = max(self.temperatures)
        minimum = min(self.temperatures)
        avg = sum(self.temperatures) / len(self.temperatures)
        return (
            {
                "maximum" : maximum,
                "minimum" : minimum,
                "average" : avg
            }
        )
    
    def get_humid_stats(self):
        maximum = max(self.humidities)
        minimum = min(self.humidities)
        avg = sum(self.humidities) / len(self.humidities)
        return (
            {
                "maximum" : maximum,
                "minimum" : minimum,
                "average" : avg
            }
        )

    def get_pressure_stats(self):
        maximum = max(self.pressures)
        minimum = min(self.pressures)
        avg = sum(self.pressures) / len(self.pressures)
        return (
            {
                "maximum" : maximum,
                "minimum" : minimum,
                "average" : avg
            }
        )

class ForecastDisplay(Observer):
    def __init__(self, weatherData):
        self.forecast_temperature = 0
        self.forecast_humidity = 0
        self.forecast_pressure = 0

        self.weatherData = weatherData 
        weatherData.registerObserver(self) 

    def update(self, temperature, humidity, pressure):
        self.forecast_temperature = temperature + 0.11 * humidity + 0.2 * pressure
        self.forecast_humidity = humidity - 0.9 * humidity
        self.forecast_pressure = pressure + 0.1 * temperature - 0.21 * pressure

        self.display()

    def display(self):
        print("Forecast Data", '{:.2f}'.format(self.forecast_temperature),
              "F degrees and", self.forecast_humidity, "[%] humidity",
              "and pressure", '{:.2f}'.format(self.forecast_pressure), "\n")
    
class WeatherStation:
    def main(self):
        weather_data = WeatherData()
        current_display = CurrentConditionsDisplay(weather_data)
        statistics_display = StatisticsDisplay(weather_data)
        forecast_display = ForecastDisplay(weather_data)

        weather_data.setMeasurements(80, 65, 30.4)
        weather_data.setMeasurements(82, 70, 29.2)
        weather_data.setMeasurements(78, 90, 29.2)

        # un-register the observer
        weather_data.removeObserver(current_display)
        weather_data.removeObserver(statistics_display)
        weather_data.removeObserver(forecast_display)
        weather_data.setMeasurements(120, 100, 1000)


if __name__ == "__main__":
    w = WeatherStation()
    w.main()
