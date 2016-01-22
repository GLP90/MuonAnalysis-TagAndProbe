#!/bin/bash
cd `dirname $0`

eval `scramv1 runtime -sh`
cmsRun fitMuonID.py $1 $2 $3 $4 
