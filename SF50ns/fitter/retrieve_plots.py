import ROOT as r
import os

def save_canvas(_folder, _file, _folder_out):
    _fit_folder = _file.replace('.root', '')

    if not os.path.exists(_folder + _folder_out):
        os.makedirs(_folder+_folder_out)

    if not os.path.exists(_folder + _folder_out + _fit_folder):
        os.makedirs(_folder + _folder_out + _fit_folder)
        
    _folder_out = _folder + _folder_out + _fit_folder
    
    print 'the folder out is', _folder_out
    
    
    f = r.TFile.Open(_folder+_file)
    for key in f.GetListOfKeys():
        c = r.gROOT.GetClass(key.GetClassName())
        #print 'The class name is ', c
        #print 'The name is ', key.GetName()
        if str(c).find('TDirectoryFile') != -1:
            #print 'directory'
            r.gDirectory.cd(key.GetName())
            for key2 in r.gDirectory.GetListOfKeys():
                c2 = r.gROOT.GetClass(key2.GetClassName())
                #print 'The class name is ', c2
                #print 'The name is ', key2.GetName()
            if str(c2).find('TDirectoryFile') != -1:
                #print 'directory'
                r.gDirectory.cd(key2.GetName())
                for key3 in r.gDirectory.GetListOfKeys():
                    c3 = r.gROOT.GetClass(key3.GetClassName())
                    #print 'The class name is ', c3
                    #print 'The name is ', key3.GetName()
                    if str(c3).find('TDirectoryFile') != -1 and key3.GetName().find('_eff') == -1:
                        #print 'directory'
                        r.gDirectory.cd(key3.GetName())
                        #print 'changed directory'
                        for key4 in r.gDirectory.GetListOfKeys():
                            c4 = r.gROOT.GetClass(key4.GetClassName())
                            #print 'The class name is ', c4
                            #print 'The name is ', key4.GetName()
                            if key4.GetName() == 'fit_canvas' and str(c4).find('TCanvas') != -1:
                                #print 'gonna save the canvas'
                                canvas  = key4.ReadObj()
                                canvas.SaveAs(_folder_out + '/' + key3.GetName() + '_TEST.pdf')

#_folder = 'MCeff4/'
_folder = 'DATAeff4/'
_folder_out = 'FitPlots/'

dir = os.listdir(_folder)
for file in dir:
    if file.find('TnP_MuonID') != -1:
        save_canvas(_folder, file, _folder_out) 




