#!/bin/bash

bsub -q 1nh -u pippo1234 run.sh data_all Id_noIP
bsub -q 1nh -u pippo1234 run.sh data_all Id_IP
bsub -q 1nh -u pippo1234 run.sh data_all LooseIso_LooseId_noIP
bsub -q 1nh -u pippo1234 run.sh data_all LooseIso_MediumId_noIP
bsub -q 1nh -u pippo1234 run.sh data_all LooseIso_TightId_noIP
bsub -q 1nh -u pippo1234 run.sh data_all LooseIso_LooseId_IP
bsub -q 1nh -u pippo1234 run.sh data_all LooseIso_MediumId_IP
bsub -q 1nh -u pippo1234 run.sh data_all LooseIso_TightId_IP
bsub -q 1nh -u pippo1234 run.sh data_all LooseIso_TightId_TightIP
bsub -q 1nh -u pippo1234 run.sh data_all TightIso_LooseId_noIP
bsub -q 1nh -u pippo1234 run.sh data_all TightIso_MediumId_noIP
bsub -q 1nh -u pippo1234 run.sh data_all TightIso_TightId_noIP
bsub -q 1nh -u pippo1234 run.sh data_all TightIso_LooseId_IP
bsub -q 1nh -u pippo1234 run.sh data_all TightIso_MediumId_IP
bsub -q 1nh -u pippo1234 run.sh data_all TightIso_TightId_IP
bsub -q 1nh -u pippo1234 run.sh data_all TightIso_TightId_TightIP

#bsub -q 1nh -u pippo1234 run.sh mc_all Id_noIP
#bsub -q 1nh -u pippo1234 run.sh mc_all Id_IP
#bsub -q 1nh -u pippo1234 run.sh mc_all LooseIso_LooseId_noIP
#bsub -q 1nh -u pippo1234 run.sh mc_all LooseIso_MediumId_noIP
#bsub -q 1nh -u pippo1234 run.sh mc_all LooseIso_TightId_noIP
#bsub -q 1nh -u pippo1234 run.sh mc_all LooseIso_LooseId_IP
#bsub -q 1nh -u pippo1234 run.sh mc_all LooseIso_MediumId_IP
#bsub -q 1nh -u pippo1234 run.sh mc_all LooseIso_TightId_IP
#bsub -q 1nh -u pippo1234 run.sh mc_all LooseIso_TightId_TightIP
#bsub -q 1nh -u pippo1234 run.sh mc_all TightIso_LooseId_noIP
#bsub -q 1nh -u pippo1234 run.sh mc_all TightIso_MediumId_noIP
#bsub -q 1nh -u pippo1234 run.sh mc_all TightIso_TightId_noIP
#bsub -q 1nh -u pippo1234 run.sh mc_all TightIso_LooseId_IP
#bsub -q 1nh -u pippo1234 run.sh mc_all TightIso_MediumId_IP
#bsub -q 1nh -u pippo1234 run.sh mc_all TightIso_TightId_IP
#bsub -q 1nh -u pippo1234 run.sh mc_all TightIso_TightId_TightIP



