#!/bin/bash
DIR=/sys/devices/platform/coretemp.0/hwmon/hwmon1
FILES=$(ls ${DIR}/*_label)
for FILE in $FILES; do
  FILENAME=$(basename $FILE)
  FILE_PREFIX=${FILENAME::-6}
  SENSOR=$(cat $FILE | awk '{ gsub(" ","_"); print tolower($0) }')
  VALUE=$(cat "${DIR}/${FILE_PREFIX}_input")
  echo "temperature,file=$FILE_PREFIX,sensor=$SENSOR temperature=$VALUE"
done
