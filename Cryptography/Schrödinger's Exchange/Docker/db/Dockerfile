FROM mysql:latest

ARG DB_NAME
ARG DB_ROOT_PASSWORD

COPY init_db.sql /docker-entrypoint-initdb.d/
WORKDIR /docker-entrypoint-initdb.d

RUN /bin/sed -i "s/db_name/$DB_NAME/g" init_db.sql && \
    /bin/sed -i "s/db_password/$DB_ROOT_PASSWORD/g" init_db.sql

WORKDIR /etc/mysql

RUN echo "[mysqld]" >> my.cnf && \
    echo "sql_mode=NO_ENGINE_SUBSTITUTION" >> my.cnf && \
    echo "max_connections = 100000" >> my.cnf && \
    echo "default_authentication_plugin=mysql_native_password" >> my.cnf