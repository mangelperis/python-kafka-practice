-- Specifics only
-- GRANT REPLICATION SLAVE, REPLICATION CLIENT, SUPER, SELECT, SHOW DATABASES, RELOAD, LOCK TABLES ON *.* TO 'dev'@'%';

GRANT ALL PRIVILEGES ON *.* TO 'dev'@'%';
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS weather;
USE weather;

CREATE TABLE forecast (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    time VARCHAR(50) NOT NULL,
    interval_seconds INT NOT NULL,
    temperature_2m DOUBLE NOT NULL,
    relative_humidity_2m DOUBLE NOT NULL,
    apparent_temperature DOUBLE NOT NULL,
    is_day TINYINT NOT NULL,
    precipitation DOUBLE NOT NULL,
    rain DOUBLE NOT NULL,
    timestamp VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_timestamp (timestamp),
    INDEX idx_time (time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE forecast_transformed (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    time VARCHAR(50) NOT NULL,
    interval_seconds INT NOT NULL,
    temperature_celsius DOUBLE NOT NULL,
    apparent_temperature_celsius DOUBLE NOT NULL,
    temperature_fahrenheit DOUBLE NOT NULL,
    apparent_temperature_fahrenheit DOUBLE NOT NULL,
    timestamp VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_timestamp (timestamp),
    INDEX idx_time (time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



