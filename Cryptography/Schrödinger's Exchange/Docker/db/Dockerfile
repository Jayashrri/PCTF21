FROM mysql:latest

ARG DB_NAME
ARG DB_USERNAME
ARG DB_PASSWORD

COPY init_db.sql /docker-entrypoint-initdb.d/
WORKDIR /docker-entrypoint-initdb.d

RUN /bin/sed -i "s/db_name/$DB_NAME/g" init_db.sql && \
    /bin/sed -i "s/db_username/$DB_USERNAME/g" init_db.sql && \
    /bin/sed -i "s/db_password/$DB_PASSWORD/g" init_db.sql

WORKDIR /etc/mysql