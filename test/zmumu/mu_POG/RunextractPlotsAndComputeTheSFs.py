import ROOT as r
import os
import sys

def getIDname(_file):
    _file = _file.replace('TnP_','')
    _file = _file.replace('.root','')
    return _file

args = sys.argv[1:]
iteration = '1'
if len(args) > 0: iteration =  args[0]
print 'iteration is', iteration
sample1 = ''
if len(args) > 1: sample1 = args[1]
print 'Data sample is', sample1
sample2 = ''
if len(args) > 2: sample2 = args[2]
print 'MC sample is', sample2

r.gROOT.LoadMacro("plotsAndSFsExtractor/extractPlotsAndComputeTheSFs.C+")

inputeff = os.getcwd() + "/Efficiency" + iteration 

_path1 = os.getcwd() + "/Efficiency" + iteration + '/' + sample1 + '/'
_path2 = os.getcwd() + "/Efficiency" + iteration + '/' + sample2 + '/'

_tptree = 'tpTree'

##!! Get the list of files
dir = os.listdir(_path1)
for file in dir:
    if file.find('TnP_') != -1: 
        if not os.path.isfile(_path2 + '/' + file):
            continue
        else:
            #Warning: _path1 must be data, _path2 mc
            if sample1.find("DATA") != -1 and sample2.find("MC") != -1:
                r.extractPlotsAndComputeTheSFs(getIDname(file), _path1 + '/' + file, _path2 + '/' + file);
            elif sample1.find("MC") != -1 and sample2.find("DATA") != -1:
                r.extractPlotsAndComputeTheSFs(getIDname(file), _path2 + '/' + file, _path1 + '/' + file);
            else:
                print "@ERROR: Need to have both DATA and MC"



