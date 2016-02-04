#!/bin/bash

#TEST
#bsub -q 8nh -u pippo1234 run.sh testsubmit 1 data_all data 

#TEST SoftID
#bsub -q 8nh -u pippo1234 run.sh testsubmit 4 mc_all mclocal 
#bsub -q 8nh -u pippo1234 run.sh testsubmit 4 data_all data 

#FINAL SUBMISSION

#MC
#bsub -q 8nh -u pippo1234 run.sh _v1 1 mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v1 2 mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v1 3 mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v1 4 mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v1 6 mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v1 7 mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v1 8 mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v1 9 mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v1 10 mc_all mc 

#DATA
#bsub -q 8nh -u pippo1234 run.sh _v2 noiso loose data_all data 
#bsub -q 8nh -u pippo1234 run.sh _v2 noiso medium data_all data 
#bsub -q 8nh -u pippo1234 run.sh _v2 noiso tight data_all data 
#bsub -q 8nh -u pippo1234 run.sh _v2 noiso soft data_all data 
#iso
bsub -q 8nh -u pippo1234 run.sh _v2 loose loose data_all data 
bsub -q 8nh -u pippo1234 run.sh _v2 loose medium data_all data 
bsub -q 8nh -u pippo1234 run.sh _v2 loose tight data_all data 
bsub -q 8nh -u pippo1234 run.sh _v2 tight medium data_all data 
bsub -q 8nh -u pippo1234 run.sh _v2 tight tight data_all data 
