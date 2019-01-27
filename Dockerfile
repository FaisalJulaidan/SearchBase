FROM mysql

# ROOT PASSWORD
ENV MYSQL_ROOT_PASSWORD=root

ENV MYSQL_ROOT_PASSWORD root
ENV MYSQL_USER root

USER root
COPY docker_stuff/init_db.sh /docker-entrypoint-initdb.d/init_db.sh

#PORT
EXPOSE 3306


