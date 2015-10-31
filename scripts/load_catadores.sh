#!/bin/bash

cat ../data/long_lat_pimp_carroceiros_app.sql | sqlite3 ../app_site/db.sqlite3

# Para visualizar atraves de uma GUI o db, eh possivel utilizar o sqlitebrowser passando o db.sqlite3 como argumento
# sqlitebrowser db.sqlite3
