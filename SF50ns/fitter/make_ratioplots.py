import ROOT as r
import os

def getplotpath(_file, _path, _tptree):
    "Take as first input the root file containing the efficiency plot. The function returns the path to the plot within the tree"
    CANVAS = []
    ##!! Get the list of files
    dir = os.listdir(_path)
    for file in dir:
        if file == 'Plots': continue
        if not file == _file: continue
        print file
        f = r.TFile.Open(_path+file)
        r.gDirectory.cd(_tptree)
        for key in  r.gDirectory.GetListOfKeys():
            #print key.GetName()
            r.gDirectory.cd(key.GetName())
            r.gDirectory.cd('fit_eff_plots')
            PLOTS = r.gDirectory.GetListOfKeys()
            if len(PLOTS) == 1:
                #print 'is a vtx plot'
                _eff = PLOTS[0].GetName() 
                _canvas = _tptree + '/' + key.GetName() + '/fit_eff_plots' +'/' + _eff 
                #r.retrieve_plots(file, _canvas)
                #print 'the canvas is ', _canvas
                #return _canvas
                CANVAS.append(_canvas)
                #print 'debug2' 
            if len(PLOTS) > 1:
                #print 'debug3' 
                #print 'more than one efficiency plot'
                '''
                if key.GetName().find('_eta') != -1:
                    #print 'is an eta plot'
                    for plot in PLOTS:
                        #print 'the name of the plot is ', plot.GetName()
                        if plot.GetName().find('eta_PLOT_pt_bin0') != -1 or plot.GetName().find('eta_PLOT_pt_bin1') != -1:
                            _canvas = _tptree + '/' + key.GetName() + '/fit_eff_plots' +'/' + plot.GetName() 
                            #r.retrieve_plots(file, _canvas)
                            #print 'the name of the plot is', plot.GetName()
                            #print 'the canvas is ', _canvas
                            #return _canvas
                            CANVAS.append(_canvas)
                            '''
                if key.GetName().find('_pt') != -1:
                    #print 'is an pt plot'
                    for plot in PLOTS:
                        if plot.GetName().find('pt_PLOT_abseta_bin0') != -1 or plot.GetName().find('pt_PLOT_abseta_bin1') != -1:
                            _canvas = _tptree + '/' + key.GetName() + '/fit_eff_plots' +'/' + plot.GetName() 
                            #r.retrieve_plots(file, _canvas)
                            #print 'the name of the plot is', plot.GetName()
                            #print 'the canvas is ', _canvas
                            #return _canvas
                            CANVAS.append(_canvas)
                #else:
                    #print '===================='
                    #print 'ERROR: neither eta nor pt plot'
                    #print '===================='
    #print 'CANVAS is ', CANVAS
    return CANVAS



r.gROOT.LoadMacro("make_ratioplots2.C+")
#r.make_ratioplots2('TnP_MuonID_data_all_Loose_noIP_eta.root','tpTree/Loose_noIP_eta/fit_eff_plots/eta_PLOT_pt_bin0_&_tag_IsoMu20_pass')
#r.make_ratioplots2("TnP_MuonID_data_all_Tight_noIP_vtx.root", "tpTree/Tight_noIP_vtx/fit_eff_plots/tag_nVertices_PLOT_tag_IsoMu20_pass")


debug = True 

_path1 = '/afs/cern.ch/work/g/gaperrin/private/CMSSW_7_4_7/src/MuonAnalysis/TagAndProbe/SF50ns/fitter/DATAeff4/'
_path2 = '/afs/cern.ch/work/g/gaperrin/private/CMSSW_7_4_7/src/MuonAnalysis/TagAndProbe/SF50ns/fitter/MCeff4/'
_tptree = 'tpTree'

##!! Get the list of files
dir = os.listdir(_path1)
for file in dir:
    print 'the file is ', file
    if file.find('TnP_MuonID') != -1:
        if not os.path.isfile(_path2 + '/' + file):
            if debug: print 'The file ', file, 'doesn\'t exist in ', _path2
            continue
        else:
            if debug: print 'The file exists !'
            CANVAS = getplotpath( file, _path1, _tptree)
            for _canvas in CANVAS:
                r.make_ratioplots2(file, _canvas)









