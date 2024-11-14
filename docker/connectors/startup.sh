#!/bin/bash

# Start Kafka Connect in the background
/etc/confluent/docker/run &

# Store the PID
KAFKA_CONNECT_PID=$!

# Wait for Kafka Connect to start
echo "Waiting for Kafka Connect to start..."
while ! curl -s -f http://localhost:8083/ > /dev/null; do
    echo "Waiting for Kafka Connect..."
    sleep 5
done

echo "Kafka Connect is up. Creating connector..."

# Create the connector
curl -X POST -H "Content-Type: application/json" \
     --data @/etc/kafka/connect/connectors/mysql-connector.json \
     http://localhost:8083/connectors

echo "Connector creation request sent."

wait $KAFKA_CONNECT_PID

# Keep the container running
tail -f /dev/null
