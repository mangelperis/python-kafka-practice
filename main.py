import logging
from logging import DEBUG
from schemas.weather import (
    WEATHER_API_VALUE_SCHEMA,
    WEATHER_FINAL_SCHEMA
)
from producers.weather_producer import WeatherProducer
from consumers.weather_consumer import WeatherConsumer


def main():
    # Configuration
    SCHEMA_REGISTRY_URL = "http://localhost:8081"
    BOOTSTRAP_SERVERS = "localhost:9092"
    INPUT_TOPIC = "weather-forecast"
    OUTPUT_TOPIC = "weather-forecast-transformed"

    # Setup logging
    logging.basicConfig(
        level=DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    try:
        # Create and run producer
        producer = WeatherProducer(
            schema_registry_url=SCHEMA_REGISTRY_URL,
            bootstrap_servers=BOOTSTRAP_SERVERS,
            value_schema=WEATHER_API_VALUE_SCHEMA
        )

        # Produce one weather message
        logging.info("Producing weather message...")
        producer.produce_weather(INPUT_TOPIC)

        # Create and run consumer
        logging.info("Starting consumer...")
        consumer = WeatherConsumer(
            schema_registry_url=SCHEMA_REGISTRY_URL,
            bootstrap_servers=BOOTSTRAP_SERVERS,
            input_schema=WEATHER_API_VALUE_SCHEMA,
            output_schema=WEATHER_FINAL_SCHEMA,
            group_id='weather-transformer'
        )

        # Start consuming messages
        consumer.consume_weather(INPUT_TOPIC, OUTPUT_TOPIC)

    except KeyboardInterrupt:
        logging.info("Application stopped by user")
    except Exception as e:
        logging.error(f"Application error: {e}")


if __name__ == "__main__":
    main()
