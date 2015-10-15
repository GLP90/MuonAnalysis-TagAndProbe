#!/bin/bash

#DATA

#bsub -q 8nh -u pippo1234 run.sh data_all 25ns 2015D 1
#bsub -q 8nh -u pippo1234 run.sh data_all 25ns 2015D 2
#bsub -q 8nh -u pippo1234 run.sh data_all 25ns 2015D 3
#bsub -q 8nh -u pippo1234 run.sh data_all 25ns 2015D 4
#bsub -q 8nh -u pippo1234 run.sh data_all 25ns 2015D 5
#bsub -q 8nh -u pippo1234 run.sh data_all 25ns 2015D 6
#bsub -q 8nh -u pippo1234 run.sh data_all 25ns 2015D 7
#bsub -q 8nh -u pippo1234 run.sh data_all 25ns 2015D 8 

bsub -q 8nh -u pippo1234 run.sh mc_all 25ns 2015D 1 NLO 
bsub -q 8nh -u pippo1234 run.sh mc_all 25ns 2015D 2 NLO
bsub -q 8nh -u pippo1234 run.sh mc_all 25ns 2015D 3 NLO
bsub -q 8nh -u pippo1234 run.sh mc_all 25ns 2015D 4 NLO
bsub -q 8nh -u pippo1234 run.sh mc_all 25ns 2015D 5 NLO
bsub -q 8nh -u pippo1234 run.sh mc_all 25ns 2015D 6 NLO
bsub -q 8nh -u pippo1234 run.sh mc_all 25ns 2015D 7 NLO
bsub -q 8nh -u pippo1234 run.sh mc_all 25ns 2015D 8 NLO

bsub -q 8nh -u pippo1234 run.sh mc_all 25ns 2015D 1 LO 
bsub -q 8nh -u pippo1234 run.sh mc_all 25ns 2015D 2 LO
bsub -q 8nh -u pippo1234 run.sh mc_all 25ns 2015D 3 LO
bsub -q 8nh -u pippo1234 run.sh mc_all 25ns 2015D 4 LO
bsub -q 8nh -u pippo1234 run.sh mc_all 25ns 2015D 5 LO
bsub -q 8nh -u pippo1234 run.sh mc_all 25ns 2015D 6 LO
bsub -q 8nh -u pippo1234 run.sh mc_all 25ns 2015D 7 LO
bsub -q 8nh -u pippo1234 run.sh mc_all 25ns 2015D 8 LO

