import logging

class TempUtils:
    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        return (celsius * 9 / 5) + 32

class KafkaCallback:
    @staticmethod
    def delivery_report(err, msg):
        """
        Generic callback for Kafka message delivery reports.
        Can be used by both producers and consumers.
        """
        if err is not None:
            logging.error('Message delivery failed: %s', err)
        else:
            logging.info('Message delivered to %s [%d] at offset %d',
                        msg.topic(), msg.partition(), msg.offset())

