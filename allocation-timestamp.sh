#!/bin/bash
sinfo --noheader -o "%P,%A,%D" | awk -F"," "{ split(\$2,alloc,\"/\"); print \"allocation,partition=\" \$1 \" allocated=\" alloc[1] \",idle=\" alloc[2] \",total=\" \$3 \",unavailable=\" \$3-alloc[2]-alloc[1] \" $(date +%s000000000)\" }"
