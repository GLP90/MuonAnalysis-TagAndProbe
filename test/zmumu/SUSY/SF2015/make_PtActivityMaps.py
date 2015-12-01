import ROOT as r
import os
import glob
import sys
from array import *
import numpy as np
import string

debug = True
nActBins = 5

r.gROOT.SetBatch()
r.gStyle.SetOptStat(0)
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
for file in glob.glob("*map_activity_pt*.root"):
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
                    if plot.GetName().startswith("pt_PLOT_pfCombRelActivitydBCorr_bin0_"):
                        canvas = plot.ReadObj()
                        HISTS = canvas.GetListOfPrimitives()
                        for hist in HISTS:
                            print hist
                            if hist.GetName().startswith("hxy_fit_eff"):
                                print "found actbin0"
                                actbin0_mc = hist
                    if plot.GetName().startswith("pt_PLOT_pfCombRelActivitydBCorr_bin1_"):
                        canvas = plot.ReadObj()
                        HISTS = canvas.GetListOfPrimitives()
                        for hist in HISTS:
                            print hist
                            if hist.GetName().startswith("hxy_fit_eff"):
                                print "found actbin1"
                                actbin1_mc = hist
                    if plot.GetName().startswith("pt_PLOT_pfCombRelActivitydBCorr_bin2_"):
                        canvas = plot.ReadObj()
                        HISTS = canvas.GetListOfPrimitives()
                        for hist in HISTS:
                            print hist
                            if hist.GetName().startswith("hxy_fit_eff"):
                                print "found actbin2"
                                actbin2_mc = hist
                    if plot.GetName().startswith("pt_PLOT_pfCombRelActivitydBCorr_bin3_"):
                        canvas = plot.ReadObj()
                        HISTS = canvas.GetListOfPrimitives()
                        for hist in HISTS:
                            print hist
                            if hist.GetName().startswith("hxy_fit_eff"):
                                print "found actbin3"
                                actbin3_mc = hist
                    if plot.GetName().startswith("pt_PLOT_pfCombRelActivitydBCorr_bin4_"):
                        canvas = plot.ReadObj()
                        HISTS = canvas.GetListOfPrimitives()
                        for hist in HISTS:
                            print hist
                            if hist.GetName().startswith("hxy_fit_eff"):
                                print "found actbin4"
                                actbin4_mc = hist


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
                    if plot.GetName().startswith("pt_PLOT_pfCombRelActivitydBCorr_bin0_"):
                        canvas = plot.ReadObj()
                        HISTS = canvas.GetListOfPrimitives()
                        for hist in HISTS:
                            print hist
                            if hist.GetName().startswith("hxy_fit_eff"):
                                print "found actbin0"
                                actbin0_data = hist
                    if plot.GetName().startswith("pt_PLOT_pfCombRelActivitydBCorr_bin1_"):
                        canvas = plot.ReadObj()
                        HISTS = canvas.GetListOfPrimitives()
                        for hist in HISTS:
                            print hist
                            if hist.GetName().startswith("hxy_fit_eff"):
                                print "found actbin1"
                                actbin1_data = hist
                    if plot.GetName().startswith("pt_PLOT_pfCombRelActivitydBCorr_bin2_"):
                        canvas = plot.ReadObj()
                        HISTS = canvas.GetListOfPrimitives()
                        for hist in HISTS:
                            print hist
                            if hist.GetName().startswith("hxy_fit_eff"):
                                print "found actbin2"
                                actbin2_data = hist
                    if plot.GetName().startswith("pt_PLOT_pfCombRelActivitydBCorr_bin3_"):
                        canvas = plot.ReadObj()
                        HISTS = canvas.GetListOfPrimitives()
                        for hist in HISTS:
                            print hist
                            if hist.GetName().startswith("hxy_fit_eff"):
                                print "found actbin3"
                                actbin3_data = hist
                    if plot.GetName().startswith("pt_PLOT_pfCombRelActivitydBCorr_bin4_"):
                        canvas = plot.ReadObj()
                        HISTS = canvas.GetListOfPrimitives()
                        for hist in HISTS:
                            print hist
                            if hist.GetName().startswith("hxy_fit_eff"):
                                print "found actbin4"
                                actbin4_data = hist

    c1=r.TCanvas("c1","c1",1200,800) 
    p1 = r.TPad("p1","p1",0.01,0.01,0.99,0.99);
    p1.Draw();
    p1.cd();
    p1.SetLogy()

    Map = r.TH2F()
    Map = p1.DrawFrame(10,0.001,200,10)
    xbins = np.array([10.,40.,80.,200.])
    ybins = np.array([0.001, 0.02, 0.05, 0.15, 1., 10.])
    p1.Update()


    SFmap = r.TH2F("SFmap", file, 3, xbins, 5, ybins)

    pt_data = 0
    eff_data = 0
    pt_data = r.Double(pt_data)
    eff_data = r.Double(eff_data)
 
    pt_mc = 0
    eff_mc = 0
    pt_mc = r.Double(pt_mc)
    eff_mc = r.Double(eff_mc)
 
    for act in range(nActBins):
        for i in range(actbin0_data.GetN()):
            if act==0:
                actbin0_data.GetPoint(i, pt_data, eff_data)
                errh_data = actbin0_data.GetErrorYhigh(i)
                errl_data = actbin0_data.GetErrorYlow(i)
                actbin0_mc.GetPoint(i, pt_mc, eff_mc)
                errh_mc = actbin0_mc.GetErrorYhigh(i)
                errl_mc = actbin0_mc.GetErrorYlow(i)
                a = eff_data/eff_mc * ((errh_data/eff_data)**2 + (errh_mc/eff_mc)**2)**.5 
                b = eff_data/eff_mc * ((errl_data/eff_data)**2 + (errl_mc/eff_mc)**2)**.5 
                err = max(a,b)
                SFmap.SetBinContent(i+1, act+1, eff_data/eff_mc)
                SFmap.SetBinError(i+1, act+1, err)
            if act==1:
                actbin1_data.GetPoint(i, pt_data, eff_data)
                errh_data = actbin1_data.GetErrorYhigh(i)
                errl_data = actbin1_data.GetErrorYlow(i)
                actbin1_mc.GetPoint(i, pt_mc, eff_mc)
                errh_mc = actbin1_mc.GetErrorYhigh(i)
                errl_mc = actbin1_mc.GetErrorYlow(i)
                a = eff_data/eff_mc * ((errh_data/eff_data)**2 + (errh_mc/eff_mc)**2)**.5 
                b = eff_data/eff_mc * ((errl_data/eff_data)**2 + (errl_mc/eff_mc)**2)**.5 
                err = max(a,b)
                SFmap.SetBinContent(i+1, act+1, eff_data/eff_mc)
                SFmap.SetBinError(i+1, act+1, err)
            if act==2:
                actbin1_data.GetPoint(i, pt_data, eff_data)
                errh_data = actbin2_data.GetErrorYhigh(i)
                errl_data = actbin2_data.GetErrorYlow(i)
                actbin2_mc.GetPoint(i, pt_mc, eff_mc)
                errh_mc = actbin2_mc.GetErrorYhigh(i)
                errl_mc = actbin2_mc.GetErrorYlow(i)
                a = eff_data/eff_mc * ((errh_data/eff_data)**2 + (errh_mc/eff_mc)**2)**.5 
                b = eff_data/eff_mc * ((errl_data/eff_data)**2 + (errl_mc/eff_mc)**2)**.5 
                err = max(a,b)
                SFmap.SetBinContent(i+1, act+1, eff_data/eff_mc)
                SFmap.SetBinError(i+1, act+1, err)
            if act==3:
                actbin3_data.GetPoint(i, pt_data, eff_data)
                errh_data = actbin3_data.GetErrorYhigh(i)
                errl_data = actbin3_data.GetErrorYlow(i)
                actbin3_mc.GetPoint(i, pt_mc, eff_mc)
                errh_mc = actbin3_mc.GetErrorYhigh(i)
                errl_mc = actbin3_mc.GetErrorYlow(i)
                a = eff_data/eff_mc * ((errh_data/eff_data)**2 + (errh_mc/eff_mc)**2)**.5 
                b = eff_data/eff_mc * ((errl_data/eff_data)**2 + (errl_mc/eff_mc)**2)**.5 
                err = max(a,b)
                SFmap.SetBinContent(i+1, act+1, eff_data/eff_mc)
                SFmap.SetBinError(i+1, act+1, err)
            if act==4:
                actbin4_data.GetPoint(i, pt_data, eff_data)
                errh_data = actbin4_data.GetErrorYhigh(i)
                errl_data = actbin4_data.GetErrorYlow(i)
                actbin4_mc.GetPoint(i, pt_mc, eff_mc)
                errh_mc = actbin4_mc.GetErrorYhigh(i)
                errl_mc = actbin4_mc.GetErrorYlow(i)
                a = eff_data/eff_mc * ((errh_data/eff_data)**2 + (errh_mc/eff_mc)**2)**.5 
                b = eff_data/eff_mc * ((errl_data/eff_data)**2 + (errl_mc/eff_mc)**2)**.5 
                err = max(a,b)
                SFmap.SetBinContent(i+1, act+1, eff_data/eff_mc)
                SFmap.SetBinError(i+1, act+1, err)


 
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
    SFmap.SetTitle(file)
    SFmap.SetMarkerSize(1.0)
    SFmap.Draw("COLZ")
    SFmap.GetXaxis().SetTitle("muon p_{T} (GeV/c)") 
    SFmap.GetXaxis().SetTitleOffset(1.2) 
    SFmap.GetYaxis().SetTitle("Rel. Activity") 
    c1.Update()
    r.gStyle.SetPaintTextFormat("4.3f")
    SFmap.GetZaxis().SetRangeUser(zmin,zmax)
   
    SFmap.Draw("TEXT E same")
    c1.Update()

    fout = r.TFile(_folder_out + file, "RECREATE");
    SFmap.Write();
    c1.SaveAs(_folder_out + filename + '.png')
    c1.SaveAs(_folder_out + filename + '.pdf')
    
    fout.Close();



