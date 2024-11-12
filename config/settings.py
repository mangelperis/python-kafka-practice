import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Kafka Configuration
KAFKA_ENV = os.getenv('KAFKA_ENV', 'local')  # 'local' or 'cloud'

# Confluent Cloud Configuration
CONFLUENT_CLOUD_CONFIG = {
    'bootstrap.servers': os.getenv('CONFLUENT_BOOTSTRAP_SERVERS'),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.getenv('CONFLUENT_API_KEY'),
    'sasl.password': os.getenv('CONFLUENT_API_SECRET'),
    'schema.registry.url': os.getenv('CONFLUENT_SCHEMA_REGISTRY_URL'),
    'schema.registry.basic.auth.user.info': f"{os.getenv('CONFLUENT_SR_API_KEY')}:{os.getenv('CONFLUENT_SR_API_SECRET')}"
}

# Local Configuration
LOCAL_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://localhost:8081'
}


def get_kafka_config():
    """Get Kafka configuration based on environment"""
    if KAFKA_ENV == 'cloud':
        return CONFLUENT_CLOUD_CONFIG
    return LOCAL_CONFIG


def get_producer_config():
    """Get producer-specific configuration"""
    config = get_kafka_config()
    if KAFKA_ENV == 'cloud':
        return config
    return {'bootstrap.servers': config['bootstrap.servers']}


def get_consumer_config(group_id: str):
    """Get consumer-specific configuration"""
    config = get_kafka_config()
    consumer_config = {
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    }

    if KAFKA_ENV == 'cloud':
        consumer_config.update(config)
    else:
        consumer_config['bootstrap.servers'] = config['bootstrap.servers']

    return consumer_config


def get_schema_registry_config():
    """Get Schema Registry configuration"""
    config = get_kafka_config()
    return {'url': config['schema.registry.url']}
