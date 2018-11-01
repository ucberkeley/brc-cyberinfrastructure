#!/bin/bash
SCRIPTS=$(dirname $0)
$SCRIPTS/main.sh | awk "{ print \$0 \" $(date +%s000000000)\"; }"
