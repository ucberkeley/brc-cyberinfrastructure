#!/bin/bash
squeue --noheader -o "jobid=%A|partition=%P|state=%T|cpus=%C|nodes=%D|time_remaining=%L|reason=%R|account=%a"
