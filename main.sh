#!/bin/bash
SCRIPTS=$(dirname $0)
$SCRIPTS/allocation.sh
$SCRIPTS/queue.sh
# $SCRIPTS/unavailable.sh
# $SCRIPTS/temp.sh
# $SCRIPTS/filesystem.sh
