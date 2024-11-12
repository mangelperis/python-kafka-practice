import json
import logging
from datetime import datetime
import requests
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField
from utils.kafka_utils import KafkaCallback
from config.settings import get_producer_config, get_schema_registry_config

# Define a GPS position
latitude = 39.5333
longitude = -0.3333
town_name = 'Meliana'

class WeatherProducer:
    def __init__(self, value_schema: str):
        self.schema_registry_client = SchemaRegistryClient(get_schema_registry_config())
        self.avro_serializer = AvroSerializer(self.schema_registry_client, value_schema)
        self.producer = Producer(get_producer_config())

    @staticmethod
    def get_weather():
        response = requests.get("https://api.open-meteo.com/v1/forecast", params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain",
            "timezone": "auto"
        })
        response.raise_for_status()
        return response.json()

    def produce_weather(self, topic: str):
        try:
            weather_data = self.get_weather()
            logging.info("API Response: %s", json.dumps(weather_data, indent=2))

            value = {
                **weather_data['current'],
                'timestamp': datetime.now().isoformat()
            }

            self.producer.produce(
                topic=topic,
                key=town_name,
                value=self.avro_serializer(
                    value,
                    SerializationContext(topic, MessageField.VALUE)
                ),
                callback=KafkaCallback.delivery_report
            )
            self.producer.flush()

        except Exception as e:
            logging.error("Error producing message: %s", e)
