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
        #print "The file is", file
        f = r.TFile.Open(_path+file)
        r.gDirectory.cd(_tptree)
        for key in  r.gDirectory.GetListOfKeys():
            print "The name of the key is", key.GetName()
            r.gDirectory.cd(key.GetName())
            r.gDirectory.cd('fit_eff_plots')
            PLOTS = r.gDirectory.GetListOfKeys()
            PAR = getparameter(_file)
            for plot in PLOTS:
                print 'plot is', plot.GetName()
                for par in PAR:
                    if plot.GetName().startswith(par):
                        print 'xxxxxxxxxxxxxxxxx'
                        print "making ratio for ", plot
                        print 'xxxxxxxxxxxxxxxxx'
                        _canvas = _tptree + '/' + key.GetName() + '/fit_eff_plots' +'/' + plot.GetName() 
                        CANVAS.append(_canvas)
    return CANVAS

def getparameter(_file):
    _par = [] 
    if _file.find('VAR_eta') != -1: _par.append('eta_PLOT')
    elif _file.find('VAR_pt') != -1: _par.append('pt_PLOT')
    elif _file.find('VAR_map_pt_eta') != -1: 
        _par.append('pt_PLOT_abseta_bin0')
        _par.append('pt_PLOT_abseta_bin1')
        _par.append('pt_PLOT_abseta_bin2')
        _par.append('pt_PLOT_abseta_bin3')
    elif _file.find('pt_highabseta') != -1:_par.append('pt_PLOT')
    elif _file.find('VAR_vtx') != -1: _par.append('tag_nVertices_PLOT')
    elif _file.find('_phi') != -1: _par.append('phi_PLOT')
    elif _file.find('VAR_map_activity_eta') != -1: 
        _par.append('pfCombRelActivitydBCorr_PLOT_abseta_bin0')
        _par.append('pfCombRelActivitydBCorr_PLOT_abseta_bin1')
    elif _file.find('VAR_map_activity_pt') != -1: 
        _par.append('pfCombRelActivitydBCorr_PLOT_pt_bin0')
        _par.append('pfCombRelActivitydBCorr_PLOT_pt_bin1')
        _par.append('pfCombRelActivitydBCorr_PLOT_pt_bin2')
    else: 
        print "@ERROR: parameter not found !"
        sys.exit()
    return _par

import sys, os
args = sys.argv[1:]

#print 'starting making ratio plots'

iteration = '1'
if len(args) > 0: iteration =  args[0]
#print 'iteration is', iteration
scenario1 = 'DATA'
if len(args) > 1: scenario1 =  args[1]
#print 'scenario1 is', scenario1 
bspace1 = '50ns'
if len(args) > 2: bspace1 = args[2]
#print 'bspace1 is', bspace1
run1 = '2015B'
if len(args) > 3: run1 = args[3]
#print 'run1 is', run1 
order1 = ''
if len(args) > 4 and scenario1 == 'MC': order1 = args[4]
#print 'order1 is', order1 
scenario2 = 'DATA'
if len(args) > 5: scenario2 =  args[5]
#print 'scenario2 is', scenario2 
bspace2 = '50ns'
if len(args) > 6: bspace2 = args[6]
#print 'bspace2 is', bspace2
run2 = '2015B'
if len(args) > 7: run2 = args[7]
#print 'run2 is', run2 
order2 = ''
if len(args) > 8 and scenario2 == 'MC': order2 = args[8]
#print 'order2 is', order2 

_output = os.getcwd() + '/RatioPlots' + iteration
if not os.path.exists(_output): 
    os.makedirs(_output)
##print '_output is ', _output
if not os.path.exists(_output):
    os.makedirs(_output)

r.gROOT.LoadMacro("make_ratioplots.C+")
debug = True 

inputeff = os.getcwd() + "/Efficiency" + iteration 

_path1 = os.getcwd() + "/Efficiency" + iteration + '/' + scenario1 + bspace1 + run1 + order1 + '/'
_path2 = os.getcwd() + "/Efficiency" + iteration + '/' + scenario2 + bspace2 + run2 + order2 + '/'

comparison = 'mcdata'
if scenario1 == scenario2 and scenario1 == 'DATA': comparison = 'mcdata'
elif scenario1 == scenario2 and scenario1 == 'MC': comparison = 'mcmc'

_output += '/' + scenario1 + bspace1 + run1 + order1 + '_' + scenario2 + bspace2 + run2 + order2 +'/'
if not os.path.exists(_output): 
    os.makedirs(_output)
if not os.path.exists(_output):
    os.makedirs(_output)

_tptree = 'tpTree'

##!! Get the list of files
dir = os.listdir(_path1)
for file in dir:
    if debug: print 'the file is ', file
    if file.find('TnP_MuonID') != -1: 
        if not os.path.isfile(_path2 + '/' + file):
            if debug: print 'The file ', file, 'doesn\'t exist in ', _path2
            continue
        else:
            if debug: print 'The file', file, 'exists !'
            CANVAS = getplotpath( file, _path1, _tptree)
            if debug: print "CANVAS is", CANVAS
            for _canvas in CANVAS:
                r.make_ratioplots(file, _canvas, _path1, _path2, _output, comparison)
