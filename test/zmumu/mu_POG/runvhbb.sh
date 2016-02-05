#!/bin/bash
cd `dirname $0`

eval `scramv1 runtime -sh`
cmsRun fitMuonIDvhbb.py $1 $2 $3 $4 $5
