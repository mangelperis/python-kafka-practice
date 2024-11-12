import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_ENV = os.getenv('KAFKA_ENV', 'local')

# Confluent Cloud Kafka Configuration
CONFLUENT_KAFKA_CONFIG = {
    'bootstrap.servers': os.getenv('CONFLUENT_BOOTSTRAP_SERVERS'),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.getenv('CONFLUENT_API_KEY'),
    'sasl.password': os.getenv('CONFLUENT_API_SECRET')
}

# Local Kafka Configuration
LOCAL_KAFKA_CONFIG = {
    'bootstrap.servers': 'localhost:9092'
}

# Schema Registry Configurations
CONFLUENT_SR_CONFIG = {
    'url': os.getenv('CONFLUENT_SCHEMA_REGISTRY_URL'),
    'basic.auth.user.info': f"{os.getenv('CONFLUENT_SR_API_KEY')}:{os.getenv('CONFLUENT_SR_API_SECRET')}"
}

LOCAL_SR_CONFIG = {
    'url': 'http://localhost:8081'
}

def get_kafka_config():
    """Get Kafka configuration based on environment"""
    return CONFLUENT_KAFKA_CONFIG if KAFKA_ENV == 'cloud' else LOCAL_KAFKA_CONFIG

def get_schema_registry_config():
    """Get Schema Registry configuration based on environment"""
    return CONFLUENT_SR_CONFIG if KAFKA_ENV == 'cloud' else LOCAL_SR_CONFIG

def get_consumer_config(group_id: str):
    """Get consumer configuration"""
    config = get_kafka_config()
    config.update({
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    })
    return config
