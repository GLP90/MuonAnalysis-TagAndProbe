#!/bin/bash

#TEST
#bsub -q 8nh -u pippo1234 run.sh testsubmit 1 data_all data 

#TEST SoftID
#bsub -q 8nh -u pippo1234 run.sh testsubmit 4 mc_all mclocal 
#bsub -q 8nh -u pippo1234 run.sh testsubmit 4 data_all data 

#FINAL SUBMISSION

#OLD MC
#bsub -q 8nh -u pippo1234 run.sh _v3 1 mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v3 2 mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v3 3 mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v3 4 mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v3 6 mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v3 7 mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v3 8 mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v3 9 mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v3 10 mc_all mc 

#MC
#bsub -q 8nh -u pippo1234 run.sh _v2 noiso loose mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v2 noiso medium mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v2 noiso tight mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v2 noiso soft mc_all mc 
#iso
#bsub -q 8nh -u pippo1234 run.sh _v3 loose loose mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v3 loose medium mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v3 loose tight mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v3 tight medium mc_all mc 
#bsub -q 8nh -u pippo1234 run.sh _v3 tight tight mc_all mc 

#DATA
#bsub -q 8nh -u pippo1234 run.sh _v3_Cheb50_60pt noiso loose data_all data 
#bsub -q 8nh -u pippo1234 run.sh _v3_Cheb50_60pt noiso medium data_all data 
#bsub -q 8nh -u pippo1234 run.sh _v3_Cheb50_60pt noiso tight data_all data 
#bsub -q 8nh -u pippo1234 run.sh _v3_Cheb50_60pt noiso soft data_all data 
#iso
#bsub -q 8nh -u pippo1234 run.sh _v2 loose loose data_all data 
#bsub -q 8nh -u pippo1234 run.sh _v2 loose medium data_all data 
#bsub -q 8nh -u pippo1234 run.sh _v2 loose tight data_all data 
#bsub -q 8nh -u pippo1234 run.sh _v2 tight medium data_all data 
#bsub -q 8nh -u pippo1234 run.sh _v2 tight tight data_all data 

################
#FOR VHBB
################
#MC
#bsub -q 8nh -u pippo1234 runvhbb.sh _vhbb_v2 noiso loose mc_all mc 
#bsub -q 8nh -u pippo1234 runvhbb.sh _vhbb_v2 noiso tight mc_all mc 
#iso
#bsub -q 8nh -u pippo1234 runvhbb.sh _vhbb_v2 loose loose mc_all mc 

#DATA
#bsub -q 8nh -u pippo1234 runvhbb.sh _vhbb_v2 noiso loose data_all data 
#bsub -q 8nh -u pippo1234 runvhbb.sh _vhbb_v2 noiso tight data_all data 
#iso
#bsub -q 8nh -u pippo1234 runvhbb.sh _vhbb_v2 loose loose data_all data 

##############
#For JPSI
#############

#MC
#bsub -q 8nh -u pippo1234 runjpsi.sh _jpsi_v2 gentracks loose mc_all mc 
#bsub -q 8nh -u pippo1234 runjpsi.sh _jpsi_v2 gentracks tight mc_all mc 

#DATA
#bsub -q 8nh -u pippo1234 runjpsi.sh _jpsi_v2 gentracks loose data_all data 
#bsub -q 8nh -u pippo1234 runjpsi.sh _jpsi_v2 gentracks tight data_all data 
