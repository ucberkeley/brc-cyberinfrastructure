#!/bin/bash

PROJECT=$1
SQL_STATEMENT="select projects.\"Project Name\", projects.\"Faculty Email\", requests.\"PI's Campus Division or Department\" from projects, requests where projects.\"Faculty Email\" = requests.\"PI Contact Email Address\" and projects.\"Project Name\" = \"$1\";"

RESULT=$(sqlite3 db.sqlite3 "$SQL_STATEMENT")

echo $RESULT
