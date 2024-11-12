import logging
from datetime import datetime
from confluent_kafka import Consumer, Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer, AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField
from utils.kafka_utils import KafkaCallback, TempUtils
from config.settings import get_consumer_config, get_kafka_config, get_schema_registry_config

class WeatherConsumer:
    def __init__(self, input_schema: str, output_schema: str, group_id: str):
        self.schema_registry_client = SchemaRegistryClient(get_schema_registry_config())

        self.avro_deserializer = AvroDeserializer(
            self.schema_registry_client,
            input_schema
        )

        self.avro_serializer = AvroSerializer(
            self.schema_registry_client,
            output_schema
        )

        self.consumer = Consumer(get_consumer_config(group_id))
        self.producer = Producer(get_kafka_config())

    def process_message(self, msg, output_topic: str):
        try:
            # Deserialize the message using the input schema
            weather_data = self.avro_deserializer(
                msg.value(),
                SerializationContext(msg.topic(), MessageField.VALUE)
            )

            # Transform data to match the final schema
            transformed_data = {
                'time': weather_data['time'],
                'interval': weather_data['interval'],
                'temperature_celsius': weather_data['temperature_2m'],
                'apparent_temperature_celsius': weather_data['apparent_temperature'],
                'temperature_fahrenheit': TempUtils.celsius_to_fahrenheit(weather_data['temperature_2m']),
                'apparent_temperature_fahrenheit': TempUtils.celsius_to_fahrenheit(weather_data['apparent_temperature']),
                'timestamp': weather_data['timestamp']
            }

            # Produce transformed message
            self.producer.produce(
                topic=output_topic,
                key=msg.key(),
                value=self.avro_serializer(
                    transformed_data,
                    SerializationContext(output_topic, MessageField.VALUE)
                ),
                callback=KafkaCallback.delivery_report
            )
            self.producer.flush()

        except Exception as e:
            logging.error("Error processing message: %s", e)

    def consume_weather(self, input_topic: str, output_topic: str):
        try:
            self.consumer.subscribe([input_topic])

            while True:
                msg = self.consumer.poll(1.0)

                if msg is None:
                    logging.debug("No messages received")
                    continue
                if msg.error():
                    logging.error("Consumer error: %s", msg.error())
                    continue

                self.process_message(msg, output_topic)

        except KeyboardInterrupt:
            logging.info("Stopping consumer...")
        finally:
            self.consumer.close()
