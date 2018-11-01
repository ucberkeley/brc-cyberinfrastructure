#!/bin/bash
SCRIPTS=$(dirname $0)
$SCRIPTS/partition-usage.sh savio
$SCRIPTS/partition-usage.sh savio2
$SCRIPTS/partition-usage.sh savio2_1080ti
$SCRIPTS/partition-usage.sh savio2_bigmem
$SCRIPTS/partition-usage.sh savio2_gpu
$SCRIPTS/partition-usage.sh savio2_htc
$SCRIPTS/partition-usage.sh savio2_knl
$SCRIPTS/partition-usage.sh savio2_bigmem
