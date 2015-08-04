#!/bin/bash

busb -q 1nh -u pippo run.sh data_all Id_noIP
busb -q 1nh -u pippo run.sh data_all Id_IP
busb -q 1nh -u pippo run.sh data_all LooseIso_LooseId_noIP
busb -q 1nh -u pippo run.sh data_all LooseIso_MediumId_noIP
busb -q 1nh -u pippo run.sh data_all LooseIso_TightId_noIP
busb -q 1nh -u pippo run.sh data_all LooseIso_LooseId_IP
busb -q 1nh -u pippo run.sh data_all LooseIso_MediumId_IP
busb -q 1nh -u pippo run.sh data_all LooseIso_TightId_IP
busb -q 1nh -u pippo run.sh data_all LooseIso_TightId_TightIP
busb -q 1nh -u pippo run.sh data_all TightIso_LooseId_noIP
busb -q 1nh -u pippo run.sh data_all TightIso_MediumId_noIP
busb -q 1nh -u pippo run.sh data_all TightIso_TightId_noIP
busb -q 1nh -u pippo run.sh data_all TightIso_LooseId_IP
busb -q 1nh -u pippo run.sh data_all TightIso_MediumId_IP
busb -q 1nh -u pippo run.sh data_all TightIso_TightId_IP
busb -q 1nh -u pippo run.sh data_all TightIso_TightId_TightIP

busb -q 1nh -u pippo run.sh mc_all Id_noIP
busb -q 1nh -u pippo run.sh mc_all Id_IP
busb -q 1nh -u pippo run.sh mc_all LooseIso_LooseId_noIP
busb -q 1nh -u pippo run.sh mc_all LooseIso_MediumId_noIP
busb -q 1nh -u pippo run.sh mc_all LooseIso_TightId_noIP
busb -q 1nh -u pippo run.sh mc_all LooseIso_LooseId_IP
busb -q 1nh -u pippo run.sh mc_all LooseIso_MediumId_IP
busb -q 1nh -u pippo run.sh mc_all LooseIso_TightId_IP
busb -q 1nh -u pippo run.sh mc_all LooseIso_TightId_TightIP
busb -q 1nh -u pippo run.sh mc_all TightIso_LooseId_noIP
busb -q 1nh -u pippo run.sh mc_all TightIso_MediumId_noIP
busb -q 1nh -u pippo run.sh mc_all TightIso_TightId_noIP
busb -q 1nh -u pippo run.sh mc_all TightIso_LooseId_IP
busb -q 1nh -u pippo run.sh mc_all TightIso_MediumId_IP
busb -q 1nh -u pippo run.sh mc_all TightIso_TightId_IP
busb -q 1nh -u pippo run.sh mc_all TightIso_TightId_TightIP



