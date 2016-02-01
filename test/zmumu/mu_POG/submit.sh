#!/bin/bash

#TEST
bsub -q 8nh -u pippo1234 run.sh testsubmit 1 data_all data 

#TEST SoftID
bsub -q 8nh -u pippo1234 run.sh testsubmit 4 mc_all mclocal 
#bsub -q 8nh -u pippo1234 run.sh testsubmit 4 data_all data 
