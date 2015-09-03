#!/bin/bash
cd /afs/cern.ch/work/g/gaperrin/private/CMSSW_7_4_7/src/MuonAnalysis/TagAndProbe/SF50ns/Ischia/

eval `scramv1 runtime -sh`
cmsRun fitMuonID.py $1 $2 $3
