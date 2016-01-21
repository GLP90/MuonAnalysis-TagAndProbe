import ROOT as r
import os
import sys

def getplotpath(_file, _path, _tptree):
    "Take as first input the root file containing the efficiency plot. The function returns the path to the plot within the tree"
    print '\nStart getplotpath'
    print '=================\n'
    CANVAS = []
    ##!! Get the list of files
    dir = os.listdir(_path)
    for file in dir:
        if file == 'Plots': continue
        if not file == _file: continue
        print "The file is", file
        f = r.TFile.Open(_path+file)
        r.gDirectory.cd(_tptree)
        for key in  r.gDirectory.GetListOfKeys():
            print "The name of the key is", key.GetName()
            r.gDirectory.cd(key.GetName())
            r.gDirectory.cd('fit_eff_plots')
            PLOTS = r.gDirectory.GetListOfKeys()
            PAR = getparameter(_file)
            print "PAR is", PAR
            for plot in PLOTS:
                print 'plot is', plot.GetName()
                for par in PAR:
                    if plot.GetName().startswith(par):
                        print '============\n'
                        print 'name checked'
                        print '============\n'

                        _canvas = _tptree + '/' + key.GetName() + '/fit_eff_plots' +'/' + plot.GetName() 
                        CANVAS.append(_canvas)
                        print "_canvas is", _canvas
    print '\nEnd getplotpath'
    print '=================\n'
    return CANVAS

def getparameter(_file):
    _par = [] 
    if _file.find('PAR_eta') != -1: _par.append('eta_PLOT')
    elif _file.find('coarse_eta') != -1: _par.append('abseta_PLOT')
    elif _file.find('pt_alleta') != -1: _par.append('pt_PLOT')
    elif _file.find('pt_spliteta') != -1: 
        _par.append('pt_PLOT_abseta_bin0')
        _par.append('pt_PLOT_abseta_bin1')
        _par.append('pt_PLOT_abseta_bin2')
        _par.append('pt_PLOT_abseta_bin3')
    elif _file.find('pt_highabseta') != -1:_par.append('pt_PLOT')
    elif _file.find('_vtx') != -1: _par.append('tag_nVertices_PLOT')
    elif _file.find('_phi') != -1: _par.append('phi_PLOT')
    else: 
        print "@ERROR: parameter not found !"
        sys.exit()
    return _par

import sys, os
args = sys.argv[1:]

print 'starting making ratio plots'

iteration = '1'
if len(args) > 0: iteration =  args[0]
print 'iteration is', iteration
sample1 = 'sample1'
if len(args) > 1: sample1 = args[1]
print 'sample1 is', sample1
sample2 = 'sample2'
if len(args) > 2: sample2 = args[2]
print 'sample2 is', sample2

_output = os.getcwd() + '/RatioPlots' + iteration
if not os.path.exists(_output): 
    os.makedirs(_output)
#print '_output is ', _output
if not os.path.exists(_output):
    os.makedirs(_output)

r.gROOT.LoadMacro("make_ratioplots.C+")
debug = True 

inputeff = os.getcwd() + "/Efficiency" + iteration 

#_path1 = os.getcwd() + "/Efficiency" + iteration + '/' + scenario1 + bspace1 + run1 + order1 + '/'
#_path2 = os.getcwd() + "/Efficiency" + iteration + '/' + scenario2 + bspace2 + run2 + order2 + '/'
_path1 = os.getcwd() + "/Efficiency" + iteration + '/' + sample1 + '/'
_path2 = os.getcwd() + "/Efficiency" + iteration + '/' + sample2 + '/'

comparison = 'mcdata'
#if scenario1 == scenario2 and scenario1 == 'DATA': comparison = 'mcdata'
#elif scenario1 == scenario2 and scenario1 == 'MC': comparison = 'mcmc'

#_output += '/' + scenario1 + bspace1 + run1 + order1 + '_' + scenario2 + bspace2 + run2 + order2 +'/'
_output += '/' + sample1 + '_' + sample2 + '/'
if not os.path.exists(_output): 
    os.makedirs(_output)
#print '_output is ', _output
if not os.path.exists(_output):
    os.makedirs(_output)

print 'path1 is', _path1
print 'path2 is', _path2
_tptree = 'tpTree'

##!! Get the list of files
dir = os.listdir(_path1)
for file in dir:
    print 'the file is ', file
    if file.find('TnP_') != -1: 
        if not os.path.isfile(_path2 + '/' + file):
            if debug: print 'The file ', file, 'doesn\'t exist in ', _path2
            continue
        else:
            if debug: print 'The file', file, 'exists !'
            CANVAS = getplotpath( file, _path1, _tptree)
            print "hello"
            print "CANVAS is", CANVAS
            for _canvas in CANVAS:
                print 'will retrieve the canvas ', _canvas
                r.make_ratioplots(file, _canvas, _path1, _path2, _output, comparison)