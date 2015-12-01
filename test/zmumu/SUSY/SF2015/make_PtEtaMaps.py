import ROOT as r
import os
import glob
import sys
from array import *
import numpy as np
import string

debug = True
nEtaBins = 4

r.gROOT.SetBatch()
args = sys.argv[1:]
iteration = '1'
if len(args) > 0: iteration =  args[0]
print "The iteration is ", iteration
if len(args) > 0: order =  args[1]
_sample1 = '/DATA25ns2015D/'
_sample2 = '/MC25ns2015D' + order + '/'
_folder1 = os.getcwd() + '/Efficiency' + iteration + '/' + _sample1 + '/'
_folder2 = os.getcwd() + '/Efficiency' + iteration + '/' + _sample2 + '/'
_folder_out = os.getcwd() + '/RatioMap' + iteration + '/' + 'DATA_vs_MC' + order + '/'
if not os.path.exists(_folder_out):
    os.makedirs(_folder_out)

_tptree = 'tpTree'

dir = os.listdir(_folder1)
os.chdir(_folder1)
for file in glob.glob("*map_pt_eta*.root"):
    if debug: print 'the file is ', file
    if file.find('TnP_MuonID') != -1: 
        if not os.path.isfile(_folder1 + '/' + file):
            if debug: print 'The file ', file, 'doesn\'t exist in ', _folder1
            continue
        else:
            if debug: print 'The file', file, 'exists !'
            f = r.TFile.Open(_folder1+file)
            r.gDirectory.cd(_tptree)
            for key in  r.gDirectory.GetListOfKeys():
                print "The name of the key is", key.GetName()
                r.gDirectory.cd(key.GetName())
                r.gDirectory.cd('fit_eff_plots')
                PLOTS = r.gDirectory.GetListOfKeys()
                PLOTS.ls()
                for plot in PLOTS:
                    if plot.GetName().startswith("pt_abseta_PLOT_pair_probeMultiplicity_bin0"):
                        print plot.GetName()
                        canvas = plot.ReadObj()
                        HISTS = canvas.GetListOfPrimitives()
                        for hist in HISTS:
                            if hist.GetName().startswith("pt_abseta_PLOT_pair_probeMultiplicity_bin0"):
                                print "found map"
                                SFmap = hist
                    if plot.GetName().startswith("pt_PLOT_abseta_bin0"):
                        canvas = plot.ReadObj()
                        HISTS = canvas.GetListOfPrimitives()
                        for hist in HISTS:
                            print hist
                            if hist.GetName().startswith("hxy_fit_eff"):
                                print "found etabin0"
                                etabin0_data = hist
                    if plot.GetName().startswith("pt_PLOT_abseta_bin1"):
                        canvas = plot.ReadObj()
                        HISTS = canvas.GetListOfPrimitives()
                        for hist in HISTS:
                            print hist
                            if hist.GetName().startswith("hxy_fit_eff"):
                                print "found etabin1"
                                etabin1_data = hist
                    if plot.GetName().startswith("pt_PLOT_abseta_bin2"):
                        canvas = plot.ReadObj()
                        HISTS = canvas.GetListOfPrimitives()
                        for hist in HISTS:
                            print hist
                            if hist.GetName().startswith("hxy_fit_eff"):
                                print "found etabin2"
                                etabin2_data = hist
                    if plot.GetName().startswith("pt_PLOT_abseta_bin3"):
                        canvas = plot.ReadObj()
                        HISTS = canvas.GetListOfPrimitives()
                        for hist in HISTS:
                            print hist
                            if hist.GetName().startswith("hxy_fit_eff"):
                                print "found etabin3"
                                etabin3_data = hist


    if debug: print 'the file is ', file
    if file.find('TnP_MuonID') != -1: 
        if not os.path.isfile(_folder2 + '/' + file):
            if debug: print 'The file ', file, 'doesn\'t exist in ', _folder2
            continue
        else:
            if debug: print 'The file', file, 'exists !'
            f = r.TFile.Open(_folder2+file)
            r.gDirectory.cd(_tptree)
            for key in  r.gDirectory.GetListOfKeys():
                print "The name of the key is", key.GetName()
                r.gDirectory.cd(key.GetName())
                r.gDirectory.cd('fit_eff_plots')
                PLOTS = r.gDirectory.GetListOfKeys()
                PLOTS.ls()
                for plot in PLOTS:
                    if plot.GetName().startswith("pt_PLOT_abseta_bin0"):
                        canvas = plot.ReadObj()
                        HISTS = canvas.GetListOfPrimitives()
                        for hist in HISTS:
                            print hist
                            if hist.GetName().startswith("hxy_fit_eff"):
                                etabin0_mc = hist
                    if plot.GetName().startswith("pt_PLOT_abseta_bin1"):
                        canvas = plot.ReadObj()
                        HISTS = canvas.GetListOfPrimitives()
                        for hist in HISTS:
                            print hist
                            if hist.GetName().startswith("hxy_fit_eff"):
                                print "found etabin1"
                                etabin1_mc = hist
                    if plot.GetName().startswith("pt_PLOT_abseta_bin2"):
                        canvas = plot.ReadObj()
                        HISTS = canvas.GetListOfPrimitives()
                        for hist in HISTS:
                            print hist
                            if hist.GetName().startswith("hxy_fit_eff"):
                                print "found etabin2"
                                etabin2_mc = hist
                    if plot.GetName().startswith("pt_PLOT_abseta_bin3"):
                        canvas = plot.ReadObj()
                        HISTS = canvas.GetListOfPrimitives()
                        for hist in HISTS:
                            print hist
                            if hist.GetName().startswith("hxy_fit_eff"):
                                print "found etabin3"
                                etabin3_mc = hist

    
    pt_data = 0
    eff_data = 0
    pt_data = r.Double(pt_data)
    eff_data = r.Double(eff_data)
 
    pt_mc = 0
    eff_mc = 0
    pt_mc = r.Double(pt_mc)
    eff_mc = r.Double(eff_mc)
 
    for eta in range(nEtaBins):
        for i in range(etabin0_data.GetN()):
            if eta==0:
                etabin0_data.GetPoint(i, pt_data, eff_data)
                errh_data = etabin0_data.GetErrorYhigh(i)
                errl_data = etabin0_data.GetErrorYlow(i)
                etabin0_mc.GetPoint(i, pt_mc, eff_mc)
                errh_mc = etabin0_mc.GetErrorYhigh(i)
                errl_mc = etabin0_mc.GetErrorYlow(i)
                a = eff_data/eff_mc * ((errh_data/eff_data)**2 + (errh_mc/eff_mc)**2)**.5 
                b = eff_data/eff_mc * ((errl_data/eff_data)**2 + (errl_mc/eff_mc)**2)**.5 
                err = max(a,b)
                SFmap.SetBinContent(i+1, eta+1, eff_data/eff_mc)
                SFmap.SetBinError(i+1, eta+1, err)
            if eta==1:
                etabin1_data.GetPoint(i, pt_data, eff_data)
                errh_data = etabin1_data.GetErrorYhigh(i)
                errl_data = etabin1_data.GetErrorYlow(i)
                etabin1_mc.GetPoint(i, pt_mc, eff_mc)
                errh_mc = etabin1_mc.GetErrorYhigh(i)
                errl_mc = etabin1_mc.GetErrorYlow(i)
                a = eff_data/eff_mc * ((errh_data/eff_data)**2 + (errh_mc/eff_mc)**2)**.5 
                b = eff_data/eff_mc * ((errl_data/eff_data)**2 + (errl_mc/eff_mc)**2)**.5 
                err = max(a,b)
                SFmap.SetBinContent(i+1, eta+1, eff_data/eff_mc)
                SFmap.SetBinError(i+1, eta+1, err)
            if eta==2:
                etabin1_data.GetPoint(i, pt_data, eff_data)
                errh_data = etabin2_data.GetErrorYhigh(i)
                errl_data = etabin2_data.GetErrorYlow(i)
                etabin2_mc.GetPoint(i, pt_mc, eff_mc)
                errh_mc = etabin2_mc.GetErrorYhigh(i)
                errl_mc = etabin2_mc.GetErrorYlow(i)
                a = eff_data/eff_mc * ((errh_data/eff_data)**2 + (errh_mc/eff_mc)**2)**.5 
                b = eff_data/eff_mc * ((errl_data/eff_data)**2 + (errl_mc/eff_mc)**2)**.5 
                err = max(a,b)
                SFmap.SetBinContent(i+1, eta+1, eff_data/eff_mc)
                SFmap.SetBinError(i+1, eta+1, err)
            if eta==3:
                etabin3_data.GetPoint(i, pt_data, eff_data)
                errh_data = etabin3_data.GetErrorYhigh(i)
                errl_data = etabin3_data.GetErrorYlow(i)
                etabin3_mc.GetPoint(i, pt_mc, eff_mc)
                errh_mc = etabin3_mc.GetErrorYhigh(i)
                errl_mc = etabin3_mc.GetErrorYlow(i)
                a = eff_data/eff_mc * ((errh_data/eff_data)**2 + (errh_mc/eff_mc)**2)**.5 
                b = eff_data/eff_mc * ((errl_data/eff_data)**2 + (errl_mc/eff_mc)**2)**.5 
                err = max(a,b)
                SFmap.SetBinContent(i+1, eta+1, eff_data/eff_mc)
                SFmap.SetBinError(i+1, eta+1, err)




    ncontours = 999 
    MyPalette = []
    stops = [0.00, 0.50, 1.00]
    red   = [0.00, 1.00, 1.00]
    green = [0.00, 1.00, 0.00]
    blue  = [1.00, 1.00, 0.00]

    st = array('d', stops)
    re = array('d', red)
    gr = array('d', green)
    bl = array('d', blue)

    npoints = len(st)
    FI = r.TColor.CreateGradientColorTable(npoints, st, re, gr, bl, ncontours) 

    nLevels = 999;
    levels = []
    zmin = 0.9
    zmax = 1.1

    for i in range(nLevels):
        levels.append(zmin + (zmax - zmin) / (nLevels - 1) * (i))
    levels = array('d', levels)
 
    SFmap.SetContour(nLevels)

    filename = string.replace(file, '.root', '')
    c1=r.TCanvas("c1","c1",1200,800) 
    SFmap.SetTitle(file)
    SFmap.SetMarkerSize(1.0)
    SFmap.Draw("COLZ")
    r.gStyle.SetPaintTextFormat("4.3f")
    SFmap.GetZaxis().SetRangeUser(zmin,zmax)
   
    SFmap.Draw("TEXT E same")
    c1.Update()

    fout = r.TFile(_folder_out + file, "RECREATE");
    SFmap.Write();
    c1.SaveAs(_folder_out + filename + '.png')
    c1.SaveAs(_folder_out + filename + '.pdf')
    
    fout.Close();



