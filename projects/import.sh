#!/bin/bash

module load sqlite/3.25.2
./clean.sh
rm db.sqlite3
sqlite3 db.sqlite3 < import.sql

./show-jobs.sh > jobs.csv
sqlite3 db.sqlite3 < import-jobs.sql
