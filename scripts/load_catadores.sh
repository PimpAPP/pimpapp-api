#!/bin/bash

set -e

sqlite3 ../app/db.sqlite3 "SELECT * FROM sqlite_master WHERE type='table';"
cat ../data/long_lat_pimp_catadores_app.sql | sqlite3 ../app/db.sqlite3
sqlite3 ../app/db.sqlite3 "SELECT * FROM catador;"
