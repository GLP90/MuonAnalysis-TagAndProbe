#!/bin/bash

bsub -q 8nh -u pippo1234 run.sh data_all 
bsub -q 8nh -u pippo1234 run.sh mc_all LO
bsub -q 8nh -u pippo1234 run.sh mc_all NLO
