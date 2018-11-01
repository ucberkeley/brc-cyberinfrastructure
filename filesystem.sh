#!/bin/bash
df | awk '{ if (NR > 1) { print "filesystems,filesystem=" $1 ",mountpoint=" $6 " used=" $3 ",available=" $4} }'
