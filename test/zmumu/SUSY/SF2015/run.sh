#!/bin/bash
cd /afs/cern.ch/work/g/gaperrin/private/TnP/TnP_v3/CMSSW_7_4_10/src/MuonAnalysis/TagAndProbe/test/zmumu/SUSY/SF2015/ 

eval `scramv1 runtime -sh`
cmsRun fitMuonID.py $1 $2 $3 $4 $5
