FROM mysql:8.0.39

# Copy custom configurations if needed
COPY docker/mysql/mysql.cnf /etc/mysql/conf.d/mysql.cnf

# Copy initialization scripts (will be executed on first run)
COPY docker/mysql/init.sql /docker-entrypoint-initdb.d/init.sql

# Set default configuration
CMD ["mysqld", \
     "--character-set-server=utf8mb4", \
     "--collation-server=utf8mb4_unicode_ci", \
     "--default-authentication-plugin=mysql_native_password", \
     "--binlog-format=ROW", \
     "--binlog-row-image=FULL", \
     "--log-bin=mysql-bin"]
