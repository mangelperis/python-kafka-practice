WEATHER_API_VALUE_SCHEMA = """
{
    "namespace": "weather.avro",
    "type": "record",
    "name": "WeatherCurrent",
    "fields": [
        {"name": "time", "type": "string"},
        {"name": "interval", "type": "int"},
        {"name": "temperature_2m", "type": "double"},
        {"name": "relative_humidity_2m", "type": "double"},
        {"name": "apparent_temperature", "type": "double"},
        {"name": "is_day", "type": "int"},
        {"name": "precipitation", "type": "double"},
        {"name": "rain", "type": "double"},
        {"name": "timestamp", "type": "string"}
    ]
}
"""


WEATHER_FINAL_SCHEMA = """
{
    "namespace": "weather.avro",
    "type": "record",
    "name": "WeatherCurrentFinal",
    "fields": [
        {"name": "time", "type": "string"},
        {"name": "interval", "type": "int"},
        {"name": "temperature_celsius", "type": "double"},
        {"name": "apparent_temperature_celsius", "type": "double"},
        {"name": "temperature_fahrenheit", "type": "double"},
        {"name": "apparent_temperature_fahrenheit", "type": "double"},
        {"name": "timestamp", "type": "string"}
    ]
}
"""

KEY_SCHEMA = """
{
    "namespace": "weather.avro",
    "type": "string"
}
"""