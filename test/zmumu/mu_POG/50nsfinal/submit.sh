#!/bin/bash

#DATA

#bsub -q 1nh -u pippo1234 run.sh data_all 50nsB 1
#bsub -q 1nh -u pippo1234 run.sh data_all 50nsB 2
#bsub -q 1nh -u pippo1234 run.sh data_all 50nsB 3
#bsub -q 1nh -u pippo1234 run.sh data_all 50nsB 4
#bsub -q 1nh -u pippo1234 run.sh data_all 50nsB 5
#bsub -q 1nh -u pippo1234 run.sh data_all 50nsB 6
#bsub -q 1nh -u pippo1234 run.sh data_all 50nsB 7
#
#bsub -q 1nh -u pippo1234 run.sh data_all 50nsC 1
#bsub -q 1nh -u pippo1234 run.sh data_all 50nsC 2
#bsub -q 1nh -u pippo1234 run.sh data_all 50nsC 3
#bsub -q 1nh -u pippo1234 run.sh data_all 50nsC 4
#bsub -q 1nh -u pippo1234 run.sh data_all 50nsC 5
#bsub -q 1nh -u pippo1234 run.sh data_all 50nsC 6
#bsub -q 1nh -u pippo1234 run.sh data_all 50nsC 7

#MC

bsub -q 8nh -u pippo1234 run.sh mc_all LO 1
bsub -q 8nh -u pippo1234 run.sh mc_all LO 2
bsub -q 8nh -u pippo1234 run.sh mc_all LO 3
bsub -q 8nh -u pippo1234 run.sh mc_all LO 4
bsub -q 8nh -u pippo1234 run.sh mc_all LO 5
bsub -q 8nh -u pippo1234 run.sh mc_all LO 6
bsub -q 8nh -u pippo1234 run.sh mc_all LO 7

bsub -q 8nh -u pippo1234 run.sh mc_all NLO 1
bsub -q 8nh -u pippo1234 run.sh mc_all NLO 2
bsub -q 8nh -u pippo1234 run.sh mc_all NLO 3
bsub -q 8nh -u pippo1234 run.sh mc_all NLO 4
bsub -q 8nh -u pippo1234 run.sh mc_all NLO 5
bsub -q 8nh -u pippo1234 run.sh mc_all NLO 6
bsub -q 8nh -u pippo1234 run.sh mc_all NLO 7

