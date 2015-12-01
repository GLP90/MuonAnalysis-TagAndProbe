import ROOT as r
import os

canvas = None
def save_canvas(_folder, _file, _folder_out):
    r.gROOT.SetBatch()
    global canvas
    _fit_folder = _file.replace('.root', '')

    if not os.path.exists(_folder_out + _fit_folder):
        os.makedirs(_folder_out + _fit_folder)
        
    _folder_out += _fit_folder
    
    print 'the folder out is', _folder_out
    
    f = r.TFile.Open(_folder+_file)
    for key in f.GetListOfKeys():
        c = r.gROOT.GetClass(key.GetClassName())
        if str(c).find('TDirectoryFile') != -1:
            r.gDirectory.cd(key.GetName())
            for key2 in r.gDirectory.GetListOfKeys():
                c2 = r.gROOT.GetClass(key2.GetClassName())
            if str(c2).find('TDirectoryFile') != -1:
                r.gDirectory.cd(key2.GetName())
                for key3 in r.gDirectory.GetListOfKeys():
                    c3 = r.gROOT.GetClass(key3.GetClassName())
                    if str(c3).find('TDirectoryFile') != -1 and key3.GetName().find('_eff') == -1:
                        r.gDirectory.cd(key3.GetName())
                        for key4 in r.gDirectory.GetListOfKeys():
                            c4 = r.gROOT.GetClass(key4.GetClassName())
                            #print 'The class name is ', c4,
                            #print 'The name is ', key4.GetName()
                            if key4.GetName() == 'fit_canvas' and str(c4).find('TCanvas') != -1:
                                canvas  = key4.ReadObj()
                                #print canvas,type(canvas),canvas.GetClassName()
                                #print 'The name of the folder out is', _folder_out + '/' + key3.GetName() + '.pdf'
                                _plot = key3.GetName()
                                #if _folder_out.find("_vtx_bin") == -1:
                                    #_plot = _plot[_plot.find('tag_nVertices'):]
                                    #_plot = _plot[:_plot.find('tag_nVertices') + 19:]
                                #canvas.SaveAs(_folder_out + '/' + key3.GetName() + '.pdf')
                                savepath = str((_folder_out + '/' + _plot + '.png'))
                                canvas.Draw()
                                canvas.SaveAs(savepath)
                                canvas.SaveAs(_folder_out + '/' + _plot + '.pdf')
                        r.gDirectory.cd("..")
                r.gDirectory.cd("..")
            r.gDirectory.cd("..")

import sys, os
args = sys.argv[1:]
iteration = '1'
if len(args) > 0: iteration =  args[0]
print "The iteration is ", iteration
_sample = '/DATA25ns2015D/'
#_sample = '/MC25ns2015DLO/'
#_sample = '/MC25ns2015DNLO/'
if len(args) > 1: _sample =  args[1]
print "The sample is", _sample 
_folder = os.getcwd() + '/Efficiency' + iteration + '/' + _sample + '/'
_folder_out = _folder +  'FitPlots/'
if not os.path.exists(_folder + '/FitPlots'):
    os.makedirs(_folder + '/FitPlots')

dir = os.listdir(_folder)
for file in dir:
    if(file.find('TnP_') != -1 and os.stat(_folder + file).st_size > 9999):
        print 'hello'
        save_canvas(_folder, file, _folder_out) 




