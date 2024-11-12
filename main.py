import logging
from logging import DEBUG
from config.settings import KAFKA_ENV
from schemas.weather import (
    WEATHER_API_VALUE_SCHEMA,
    WEATHER_FINAL_SCHEMA
)
from producers.weather_producer import WeatherProducer
from consumers.weather_consumer import WeatherConsumer


def main():
    INPUT_TOPIC = "weather-forecast"
    OUTPUT_TOPIC = "weather-forecast-transformed"

    # Setup logging
    logging.basicConfig(
        level=DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logging.info("Running in %s mode", KAFKA_ENV)

    try:
        producer = WeatherProducer(value_schema=WEATHER_API_VALUE_SCHEMA)
        logging.info("Producing weather message...")
        producer.produce_weather(INPUT_TOPIC)

        # Create and run consumer
        logging.info("Starting consumer...")
        consumer = WeatherConsumer(
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
