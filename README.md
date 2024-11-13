**KAFKA + PYTHON**

Practice repo

*BACKUP PYTHON DEPENDENCIES*
```
 pip freeze > requirements.txt
```

*LIST TOPICS*
```
docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092
``` 

*CREATE TOPIC*
```
docker exec -it kafka kafka-topics \
    --create \
    --topic weather-forecast \
    --bootstrap-server localhost:9092 \
    --partitions 1 \
    --replication-factor 1
```


*DESCRIBE TOPIC*
```
docker exec -it kafka kafka-topics \                                       
    --bootstrap-server localhost:9092 \
    --topic weather-forecast \
    --describe     
```
   

*DELETE TOPIC*
```
 docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --delete --topic weather-forecast
```

*CONSUMER (JSON)*
```
docker exec -it kafka kafka-console-consumer \
    --bootstrap-server localhost:9092 \
    --topic weather-forecast \
    --from-beginning \
    --property print.key=true \
    --property print.timestamp=true
```

*CONSUMER (AVRO)*
```
docker exec -it schema-registry kafka-avro-console-consumer \
    --bootstrap-server kafka:29092 \
    --topic weather-forecast \
    --from-beginning \
    --property schema.registry.url=http://schema-registry:8081
```

*VERIFY Schema Registry is running with:*
```
curl http://localhost:8081/schemas/types
```

*INPUT TOPIC CONSUMER*
```
docker exec -it schema-registry kafka-avro-console-consumer \
    --bootstrap-server kafka:29092 \
    --topic weather-forecast \
    --from-beginning \
    --property schema.registry.url=http://schema-registry:8081
```

*OUTPUT TOPIC CONSUMER (transformed)*
```
docker exec -it schema-registry kafka-avro-console-consumer \
    --bootstrap-server kafka:29092 \
    --topic weather-forecast-transformed \
    --from-beginning \
    --property schema.registry.url=http://schema-registry:8081
```