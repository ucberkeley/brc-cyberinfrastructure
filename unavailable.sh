#!/bin/bash
sinfo -R --format "unavailable,date=%H,reason=%E,node=%N,partition=%R"
