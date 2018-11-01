#!/bin/bash
$(dirname $0)/raw-queue.sh | python $(dirname $0)/parse-queue.py
