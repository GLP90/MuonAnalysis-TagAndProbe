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
    if _file.find('_eta') != -1: _par.append('eta_PLOT')
    elif _file.find('pt_alleta') != -1: _par.append('pt_PLOT')
    elif _file.find('pt_spliteta') != -1: 
        _par.append('pt_PLOT_abseta_bin0')
        _par.append('pt_PLOT_abseta_bin1')
    elif _file.find('_vtx') != -1: _par.append('tag_nVertices_PLOT')
    else: 
        print "@ERROR: parameter not found !"
        sys.exit()
    return _par

import sys, os
args = sys.argv[1:]
comparison = 'mcdata'
if len(args) > 0: comparison =  args[0]
iteration = '1'
if len(args) > 1: iteration =  args[1]
bspace = '50nsB'
if len(args) > 1: bspace = args[2]
print 'bspace is', bspace
#mcOrder = 'LO'
mcOrder = 'NLO'
#mcOrder = 'LONLO'
if len(args) > 2: mcOrder = args[3]
print 'mcOrder is', mcOrder 
_output = os.getcwd() + '/RatioPlots' + iteration
if not os.path.exists(_output): 
    os.makedirs(_output)
if comparison == 'mcdata': _output += "/DATA_MC" + bspace + mcOrder + "/"
elif comparison == 'mcmc': _output += "/MC_MC" + bspace + mcOrder + "/"
print '_output is ', _output
if not os.path.exists(_output):
    os.makedirs(_output)

r.gROOT.LoadMacro("make_ratioplots.C+")
debug = True 

inputeff = os.getcwd() + "/Efficiency" + iteration 

_path1 = ''
_path2 = ''

if comparison == 'mcdata':
    if bspace == '50nsB':
        if mcOrder == 'LO':
            _path1 = os.getcwd() + "/Efficiency" + iteration + '/DATA50nsBeff/'
            _path2 = os.getcwd() + "/Efficiency" + iteration + '/MC50nsLO/'
        elif mcOrder == 'NLO':
            _path1 = os.getcwd() + "/Efficiency" + iteration + '/DATA50nsBeff/'
            _path2 = os.getcwd() + "/Efficiency" + iteration + '/MC50nsNLO/'
    if bspace == '50nsC':
        if mcOrder == 'LO':
            _path1 = os.getcwd() + "/Efficiency" + iteration + '/DATA50nsCeff/'
            _path2 = os.getcwd() + "/Efficiency" + iteration + '/MC50nsLO/'
        elif mcOrder == 'NLO':
            _path1 = os.getcwd() + "/Efficiency" + iteration + '/DATA50nsCeff/'
            _path2 = os.getcwd() + "/Efficiency" + iteration + '/MC50nsNLO/'
    elif bspace == '25ns':
        if mcOrder == 'LO':
            _path1 = os.getcwd() + "/Efficiency" + iteration + '/DATA25nseff/'
            _path2 = os.getcwd() + "/Efficiency" + iteration + '/MC25nsLO/'
        elif mcOrder == 'NLO':
            _path1 = os.getcwd() + "/Efficiency" + iteration + '/DATA25nseff/'
            _path2 = os.getcwd() + "/Efficiency" + iteration + '/MC25nsNLO/'
elif comparison == 'mcmc':
    if bspace.find('50ns') != -1:
            _path1 = os.getcwd() + "/Efficiency" + iteration + '/MC50nsLO/'
            _path2 = os.getcwd() + "/Efficiency" + iteration + '/MC50nsNLO/'
    elif bspace.find('25ns') != -1:
            _path1 = os.getcwd() + "/Efficiency" + iteration + '/MC25nsLO/'
            _path2 = os.getcwd() + "/Efficiency" + iteration + '/MC25nsNLO/'

print 'path1 is', _path1
print 'path2 is', _path2
_tptree = 'tpTree'

##!! Get the list of files
dir = os.listdir(_path1)
for file in dir:
    #print 'the file is ', file
    if file.find('TnP_MuonID') != -1:
        if not os.path.isfile(_path2 + '/' + file):
            if debug: print 'The file ', file, 'doesn\'t exist in ', _path2
            continue
        else:
            if debug: print 'The file', file, 'exists !'
            CANVAS = getplotpath( file, _path1, _tptree)
            print "CANVAS is", CANVAS
            for _canvas in CANVAS:
                print 'will retrieve the canvas ', _canvas
                r.make_ratioplots(file, _canvas, _path1, _path2, _output, comparison)
