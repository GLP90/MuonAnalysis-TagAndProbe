#!/bin/bash
cd `dirname $0`

eval `scramv1 runtime -sh`
#cmsRun fitMuonID.py $1 $2 $3 $4 
cmsRun fitMuonID_v2.py $1 $2 $3 $4 $5
