FROM mariadb:11

COPY flag.txt /flag.txt
COPY schema.sql /docker-entrypoint-initdb.d/01-schema.sql
COPY seed-flag.sh /docker-entrypoint-initdb.d/02-seed-flag.sh
RUN chmod 0444 /flag.txt && chmod 0555 /docker-entrypoint-initdb.d/02-seed-flag.sh
