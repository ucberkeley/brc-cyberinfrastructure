#!/bin/bash

START_TIME=$1
END_TIME=$2
sacct -PX -o JobID,Start,End,Elapsed,AllocCPUS,Partition,Account,State -S "$START_TIME" -E "$END_TIME" -a | awk '{ gsub("\\|", ",", $0); print $0 }'
