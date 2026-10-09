#!/bin/sh
set -e
FLAG="$(tr -d '\r\n' < /flag.txt)"
mariadb -uroot -p"${MYSQL_ROOT_PASSWORD:-$MARIADB_ROOT_PASSWORD}" shop \
  -e "INSERT INTO internal_notes (secret) VALUES ('${FLAG}');"
