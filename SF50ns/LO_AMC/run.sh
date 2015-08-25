#!/bin/bash
cd /afs/cern.ch/user/g/gaperrin/public/CMSSW_7_4_7/src/SF50ns/LO_AMC/
eval `scramv1 runtime -sh`
cmsRun fitMuonID.py $1 $2 $3
