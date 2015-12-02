import FWCore.ParameterSet.Config as cms

#_*_*_*_*_*_*_*_*
#Input parameters
#_*_*_*_*_*_*_*_*

import sys, os
args = sys.argv[1:]
iteration = 1
if len(args) > 1: iteration = args[1]
print "The iteration is", iteration 
id_bins = '1'
if len(args) > 2: 
    id_bins = args[2]
print 'id_bins is', id_bins
scenario = "data_all"
if len(args) > 3: scenario = args[3]
print "Will run scenario ", scenario 
bs = '25ns'
if len(args) > 4: 
    bs = args[4]
print 'the bunch spacing is', bs 
run = '2015D' 
if len(args) > 5: 
    run  = args[5]
print 'run is', run
#for MC
order = 'LO'
if len(args) > 6: 
    if scenario == 'data_all':
        print "@WARINING: no order variable is necessasry for data"
    order = args[6]
print 'order is', order

process = cms.Process("TagProbe")
process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

#_*_*_*_*_*_*_*_*_*_*_*_*
#Preparing the variables
#_*_*_*_*_*_*_*_*_*_*_*_*

_mrange = "70"
if (int(id_bins) > 4) and (int(id_bins) < 19): 
    _mrange = "77"


Template = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
        NumCPU = cms.uint32(1),
    SaveWorkspace = cms.bool(False),

    Variables = cms.PSet(
        weight = cms.vstring("weight","-100","100",""),
        #mass = cms.vstring("Tag-muon Mass", "70", "130", "GeV/c^{2}"),
        mass = cms.vstring("Tag-muon Mass", _mrange, "130", "GeV/c^{2}"),
        pt = cms.vstring("muon p_{T}", "0", "1000", "GeV/c"),
        eta    = cms.vstring("muon #eta", "-2.5", "2.5", ""),
        abseta = cms.vstring("muon |#eta|", "0", "2.5", ""),
        phi    = cms.vstring("muon #phi at vertex", "-3.1416", "3.1416", ""),
        charge = cms.vstring("muon charge", "-2.5", "2.5", ""),
        combRelIsoPF04dBeta = cms.vstring("dBeta rel iso dR 0.4", "-2", "9999999", ""),
        pfCombRelActivitydBCorr = cms.vstring("Rel. Activity", "-2", "9999999", ""),
        pfCombRelMiniIsoEACorr = cms.vstring("EA rel Mini Iso", "-2", "9999999",""),
        PtRel = cms.vstring("PtRel", "-2", "9999999",""),
        PtRatio = cms.vstring("PtRatio", "-2", "9999999",""),
        tag_pt = cms.vstring("Tag p_{T}", "0", "1000", "GeV/c"),
        tag_nVertices   = cms.vstring("Number of vertices", "0", "999", ""),
        tag_abseta = cms.vstring("|eta| of tag muon", "0", "2.5", ""),
        tag_combRelIsoPF04dBeta = cms.vstring("Tag dBeta rel iso dR 0.4", "-2", "9999999", ""),
        dzPV = cms.vstring("dzPV", "-1000", "1000", ""),
        dxyBS = cms.vstring("dxyBS", "-1000", "1000", ""),
        SIP = cms.vstring("SIP", "-1000", "1000", ""),
        pair_probeMultiplicity = cms.vstring("pair_probeMultiplicity", "0","30",""),
        ),

    Categories = cms.PSet(
        PF    = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
        Medium   = cms.vstring("Medium Id. Muon", "dummy[pass=1,fail=0]"),
        tag_IsoMu20 = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
    ),

    Expressions = cms.PSet(
        #IP
        TightIP2DVar = cms.vstring("TightIP2DVar", "abs(dxyBS) < 0.02 && abs(dzPV) < 0.1", "dxyBS", "dzPV"),
        TightIP3DVar = cms.vstring("TightIP3DVar", "abs(SIP) < 4", "SIP"),
        #ID no IP 
        Loose_noIPVar = cms.vstring("Loose_noIPVar", "PF==1", "PF"),
        Medium_noIPVar= cms.vstring("Medium_noIPVar", "Medium==1", "Medium"),
        #Mini Iso
        LooseMiniIsoVar = cms.vstring("LooseMiniIsoVar" ,"pfCombRelMiniIsoEACorr < 0.4", "pfCombRelMiniIsoEACorr"),
        TightMiniIsoVar = cms.vstring("TightMiniIsoVar" ,"pfCombRelMiniIsoEACorr < 0.2", "pfCombRelMiniIsoEACorr"),
        #Multi Iso
        MediumMultiIsoVar= cms.vstring("MediumMultiIsoVar" ,"pfCombRelMiniIsoEACorr < 0.16 && ( PtRel > 7.2 || PtRatio > 0.76 )", "pfCombRelMiniIsoEACorr", "PtRel", "PtRatio"),

        #Stacked requirements

        #Loose + Miniso02
        Loose_plus_MiniIso02Var= cms.vstring("Loose_plus_MiniIso02Var" ,"PF==1 && pfCombRelMiniIsoEACorr < 0.2", "PF", "pfCombRelMiniIsoEACorr"),
        #Loose + Miniso02 + TightIP2D
        Loose_plus_MiniIso02_puls_TightIP2DVar= cms.vstring("Loose_plus_MiniIso02_puls_TightIP2DVar" ,"PF==1 && pfCombRelMiniIsoEACorr < 0.2 && abs(dxyBS) < 0.02 && abs(dzPV) < 0.1", "PF", "pfCombRelMiniIsoEACorr", "dxyBS", "dzPV"),
        #Medium + Miniso02
        Medium_plus_MiniIso02Var= cms.vstring("Medium_plus_MiniIso02Var" ,"Medium==1 && pfCombRelMiniIsoEACorr < 0.2", "Medium", "pfCombRelMiniIsoEACorr"),
        #Loose + Miniso02 + TightIP3D
        Loose_plus_MiniIso02_puls_TightIP3DVar= cms.vstring("Loose_plus_MiniIso02_puls_TightIP3DVar" ,"PF==1 && pfCombRelMiniIsoEACorr < 0.2 && abs(SIP) < 4", "PF", "pfCombRelMiniIsoEACorr", "SIP"),
        #Medium + Miniso02 + TightIP3D
        Medium_plus_MiniIso02_puls_TightIP3DVar= cms.vstring("Medium_plus_MiniIso02_puls_TightIP3DVar" ,"Medium==1 && pfCombRelMiniIsoEACorr < 0.2 && abs(SIP) < 4", "Medium", "pfCombRelMiniIsoEACorr", "SIP"),
        #Medium + Miniso02 + TightIP2D
        Medium_plus_MiniIso02_puls_TightIP2DVar= cms.vstring("Medium_plus_MiniIso02_puls_TightIP2DVar" ,"Medium==1 && pfCombRelMiniIsoEACorr < 0.2 && abs(dxyBS) < 0.02 && abs(dzPV) < 0.1", "Medium", "pfCombRelMiniIsoEACorr", "dxyBS", "dzPV"),
        #Medium + MultiIsoMedium + TightIP2D + TightIP3D
        Medium_plus_MediumMultiIso_plus_TightIP2D_plus_TightIP3DVar= cms.vstring("Medium_plus_MediumMultiIso_plus_TightIP2D_plus_TightIP3DVar" ,"Medium==1 && pfCombRelMiniIsoEACorr < 0.16 && ( PtRel > 7.2 || PtRatio > 0.76 ) && abs(dxyBS) < 0.02 && abs(dzPV) < 0.1 && abs(SIP) < 4", "Medium", "pfCombRelMiniIsoEACorr", "PtRel", "PtRatio", "dxyBS", "dzPV", "SIP"),
        #Loose + MiniIso04 + TightIP2D
        Loose_plus_MiniIso04_puls_TightIP2DVar= cms.vstring("Loose_plus_MiniIso04_puls_TightIP2DVar" ,"PF==1 && pfCombRelMiniIsoEACorr < 0.4 && abs(dxyBS) < 0.02 && abs(dzPV) < 0.1", "PF", "pfCombRelMiniIsoEACorr", "dxyBS", "dzPV"),
    ),

#_*_*_*_*_*
#Numerators
#_*_*_*_*_*

    Cuts = cms.PSet(
        #IP
        TightIP2D = cms.vstring("TightIP2D","TightIP2DVar", "0.5"),
        TightIP3D = cms.vstring("TightIP3D","TightIP3DVar", "0.5"),
        #ID no IP
        Loose_noIP = cms.vstring("Loose_noIP", "Loose_noIPVar", "0.5"),
        Medium_noIP= cms.vstring("Medium_noIP", "Medium_noIPVar", "0.5"),
        #MiniIsolations
        LooseMiniIso = cms.vstring("LooseMiniIso" ,"LooseMiniIsoVar", "0.5"),
        TightMiniIso = cms.vstring("TightMiniIso" ,"TightMiniIsoVar", "0.5"),
        #Multi Iso
        MediumMultiIso= cms.vstring("MediumMultiIso" ,"MediumMultiIsoVar", "0.5"),
        #Loose + Miniso02
        Loose_plus_MiniIso02= cms.vstring("Loose_plus_MiniIso02" ,"Loose_plus_MiniIso02Var", "0.5"),
        #Loose + Miniso02 + TightIP2D
        Loose_plus_MiniIso02_puls_TightIP2D= cms.vstring("Loose_plus_MiniIso02_puls_TightIP2D", "Loose_plus_MiniIso02_puls_TightIP2DVar" , "0.5"),
        #Medium + Miniso02
        Medium_plus_MiniIso02= cms.vstring("Medium_plus_MiniIso02", "Medium_plus_MiniIso02Var", "0.5" ),
        #Loose + Miniso02 + TightIP3D
        Loose_plus_MiniIso02_puls_TightIP3D= cms.vstring("Loose_plus_MiniIso02_puls_TightIP3D", "Loose_plus_MiniIso02_puls_TightIP3DVar", "0.5" ),
        #Medium + Miniso02 + TightIP3D
        Medium_plus_MiniIso02_puls_TightIP3D= cms.vstring("Medium_plus_MiniIso02_puls_TightIP3D", "Medium_plus_MiniIso02_puls_TightIP3DVar", "0.5" ),
        #Medium + Miniso02 + TightIP2D
        Medium_plus_MiniIso02_puls_TightIP2D= cms.vstring("Medium_plus_MiniIso02_puls_TightIP2D", "Medium_plus_MiniIso02_puls_TightIP2DVar", "0.5" ),
        #Medium + MultiIsoMedium + TightIP2D + TightIP3D
        Medium_plus_MediumMultiIso_plus_TightIP2D_plus_TightIP3D= cms.vstring("Medium_plus_MediumMultiIso_plus_TightIP2D_plus_TightIP3D", "Medium_plus_MediumMultiIso_plus_TightIP2D_plus_TightIP3DVar", "0.5" ),
        #Loose + MiniIso04 + TightIP2D
        Loose_plus_MiniIso04_puls_TightIP2D= cms.vstring("Loose_plus_MiniIso04_puls_TightIP2D", "Loose_plus_MiniIso04_puls_TightIP2DVar", "0.5" ),
    ),

#_*_*_*_*_*_*_*_*_*_*_*_*_*
#Functions used for the fit
#_*_*_*_*_*_*_*_*_*_*_*_*_*
                          
    PDFs = cms.PSet(
        voigtPlusExpo = cms.vstring(
            "Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])",
            "Exponential::backgroundPass(mass, lp[0,-5,5])",
            "Exponential::backgroundFail(mass, lf[0,-5,5])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusExpo = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])",
            "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,2,10])",
            "SUM::signal(vFrac[0.8,0,1]*signal1, signal2)",
            "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])",
            "Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusExpoMin70 = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])",
            "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])",
            "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
            "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])",
            "Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])",
            "efficiency[0.9,0.7,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusCheb = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])",
            "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])",
            "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
            "RooChebychev::backgroundPass(mass, {a0[0.25,0,0.5], a1[-0.25,-1,0.1],a2[0.,-0.25,0.25]})",
            "RooChebychev::backgroundFail(mass, {a0[0.25,0,0.5], a1[-0.25,-1,0.1],a2[0.,-0.25,0.25]})",
            "efficiency[0.9,0.7,1]",
            "signalFractionInPassing[0.9]"
            )

    ),

    binnedFit = cms.bool(True),
    binsForFit = cms.uint32(40),
    saveDistributionsPlot = cms.bool(False),

    Efficiencies = cms.PSet(), # will be filled later
)

#_*_*_*_*_*_*_*_*_*_*_*_*
#Denominators and binning
#_*_*_*_*_*_*_*_*_*_*_*_*

#For ID

ETA_BINS_INCLUSIVE_PT = cms.PSet(
    pt  = cms.vdouble(10, 500),
    eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
VTX_BINS_INCLUSIVE_ETA_PT  = cms.PSet(
    pt     = cms.vdouble(10 , 500),
    abseta = cms.vdouble(0.0, 2.4),
    tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
PT_BINS_INCLUSIVE_ETA = cms.PSet(
    pt     = cms.vdouble(10, 20, 25, 30, 40, 50, 60, 80, 120, 200),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
PT_ETA_MAP = cms.PSet(
    pt     = cms.vdouble(10, 20, 25, 30, 40, 50, 60, 120),
    abseta = cms.vdouble( 0.0, 0.9, 1.2, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)

ACTIVITY_ETA_MAP_INCLUSIVE_PT = cms.PSet(
    pfCombRelActivitydBCorr = cms.vdouble(0, 0.02, 0.05, 0.15, 1, 9999),
    pt     = cms.vdouble(10, 500),
    abseta = cms.vdouble( 0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)

ACTIVITY_PT_MAP_INCLUSIVE_ETA = cms.PSet(
    pfCombRelActivitydBCorr = cms.vdouble(0, 0.02, 0.05, 0.15, 1, 9999),
    pt     = cms.vdouble(10, 40, 80, 200),
    abseta = cms.vdouble( 0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)

#For IP,ISO on ID
LOOSE_ETA_BINS_INCLUSIVE_PT = cms.PSet(
    pt  = cms.vdouble(10, 500),
    eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
LOOSE_VTX_BINS_INCLUSIVE_ETA_PT  = cms.PSet(
    pt     = cms.vdouble(10, 500 ),
    abseta = cms.vdouble(  0.0, 2.4),
    tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
LOOSE_PT_BINS_INCLUSIVE_ETA = cms.PSet(
    pt     = cms.vdouble(10, 20, 25, 30, 40, 50, 60, 80, 120, 200),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
LOOSE_PT_ETA_MAP = cms.PSet(
    pt     = cms.vdouble(10, 20, 25, 30, 40, 50, 60, 120),
    abseta = cms.vdouble( 0.0, 0.9, 1.2, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
LOOSE_ACTIVITY_ETA_MAP_INCLUSIVE_PT = cms.PSet(
    pfCombRelActivitydBCorr = cms.vdouble(0, 0.02, 0.05, 0.15, 1, 9999),
    pt     = cms.vdouble(10, 500),
    abseta = cms.vdouble( 0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)

#
LOOSE_ACTIVITY_PT_MAP_INCLUSIVE_ETA = cms.PSet(
    pfCombRelActivitydBCorr = cms.vdouble(0, 0.02, 0.05, 0.15, 1, 9999),
    pt     = cms.vdouble(10, 40, 80, 200),
    abseta = cms.vdouble( 0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)

#MEDIUM
MEDIUM_ETA_BINS_INCLUSIVE_PT = cms.PSet(
    pt  = cms.vdouble(10, 500),
    eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_VTX_BINS_INCLUSIVE_ETA_PT  = cms.PSet(
    pt     = cms.vdouble(10, 500),
    abseta = cms.vdouble(0.0, 2.4),
    tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_PT_BINS_INCLUSIVE_ETA = cms.PSet(
    pt     = cms.vdouble(10, 20, 25, 30, 40, 50, 60, 80, 120, 200),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_PT_ETA_MAP = cms.PSet(
    pt     = cms.vdouble(10, 20, 25, 30, 40, 50, 60, 120),
    abseta = cms.vdouble( 0.0, 0.9, 1.2, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_ACTIVITY_ETA_MAP_INCLUSIVE_PT = cms.PSet(
    pfCombRelActivitydBCorr = cms.vdouble(0, 0.02, 0.05, 0.15, 1, 9999),
    pt     = cms.vdouble(10, 500),
    abseta = cms.vdouble( 0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)

#
MEDIUM_ACTIVITY_PT_MAP_INCLUSIVE_ETA= cms.PSet(
    pfCombRelActivitydBCorr = cms.vdouble(0, 0.02, 0.05, 0.15, 1, 9999),
    pt     = cms.vdouble(10, 40, 80, 200),
    abseta = cms.vdouble( 0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)


#_*_*_*_
#Samples
#_*_*_*_

if scenario == 'data_all':
    if bs == '25ns':
        if run == '2015D':
            process.TnP_MuonID = Template.clone(
                InputFileNames = cms.vstring(
                    #'root://eoscms//eos/cms/store/group/phys_muon/perrin/SUSY/tnp_DATA_25ns_2015D_v3v4_withEAMiniIso_v2.root'      #original file: full size on eos
                    #'root://eoscms//eos/cms/store/group/phys_muon/perrin/SUSY/tnp_DATA_25ns_2015D_v3v4_withEAMiniIso_v2SmallTree.root' #small file with only 5000 events fot test purposes
                    #'root:///afs/cern.ch/work/g/gaperrin/public/Ntuples_for_Jan/tnpZ_mu_POG_Data_25ns_run2015D_v3p2_withEAMiniIso.root'       
                    '/afs/cern.ch/work/j/jhoss/public/151130_TnP_topUp/tnpZ_Data_25ns_run2015C_v3p31.root',
                    '/afs/cern.ch/work/j/jhoss/public/151130_TnP_topUp/tnpZ_Data_25ns_run2015D_v3p2.root',
                    '/afs/cern.ch/work/j/jhoss/public/151130_TnP_topUp/tnpZ_Data_25ns_run2015D_v3p31.root',
                    '/afs/cern.ch/work/j/jhoss/public/151130_TnP_topUp/tnpZ_Data_25ns_run2015D_v3p3.root'
                    ),
                InputTreeName = cms.string("fitter_tree"),
                InputDirectoryName = cms.string("tpTree"),
                OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
                Efficiencies = cms.PSet(),
                )
elif scenario == 'mc_all':
    if bs == '25ns':
        if run == '2015D':
            if order== 'LO':
                process.TnP_MuonID = Template.clone(
                InputFileNames = cms.vstring(
                #'root://eoscms//eos/cms/store/group/phys_muon/perrin/SUSY/tnp_MC_25ns_2015D_LO_SmallTree_withNVtxWeights_withEAMiniIso_v2.root'
                #'root:///afs/cern.ch/work/g/gaperrin/public/Ntuples_for_Jan/tnp_MC_25ns_2015D_LO_SmallTree_withNVtxWeights_withEAMiniIso_v2.root'
                #'root:///afs/cern.ch/work/g/gaperrin/public/Ntuples_for_Jan/tnp_MC_25ns_2015D_LO_withNVtxWeights_withEAMiniIso_v2.root'
                'root:///afs/cern.ch/work/j/jhoss/public/151130_TnP_topUp/tnpZ_MC_25ns_madgraphMLM-pythia8_v3p2_withNVtxWeights.root' #LO sample for top up
                    ),
                InputTreeName = cms.string("fitter_tree"),
                InputDirectoryName = cms.string("tpTree"),
                OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
                Efficiencies = cms.PSet(),
                )
                process.TnP_MuonID.WeightVariable = cms.string("weight")
                process.TnP_MuonID.Variables.weight = cms.vstring("weight","-10","10","")
            elif order == 'NLO':
                process.TnP_MuonID = Template.clone(
                InputFileNames = cms.vstring(
                #'root://eoscms//eos/cms/store/group/phys_muon/perrin/SUSY/tnp_MC_25ns_2015D_NLO_SmallTree_withNVtxWeights_WithWeights_withEAMiniIso_v2.root'
                #'root://eoscms//eos/cms/store/group/phys_muon/perrin/SUSY/tnpZ_MC_25ns_amcatnloFXFX-pythia8_v3_WithWeights.root'
                #'root:///afs/cern.ch/work/j/jhoss/public/tnpZ_MC_25ns_amcatnloFXFX-pythia8_v3_WithWeights.root'    # local NLO sample full size 12e6 events
                #'root:///afs/cern.ch/work/j/jhoss/public/tnpZ_MC_25ns_amcatnloFXFX-pythia8_v3_WithWeightsSmallTree.root'    #local NLO sample with 3e6 events
                #'root:///afs/cern.ch/work/j/jhoss/public/tnpZ_MC_25ns_amcatnloFXFX-pythia8_v3_WithWeightsSmallTree_v2.root'    #local NLO sample with 9e6 events
                '/afs/cern.ch/work/g/gaperrin/public/Ntuples_for_Jan/tnpZ_muPOG_MC_25ns_amcatnloFXFX-pythia8_v3p2_WithWeights_withEAMiniIso.root'
                    ),
                InputTreeName = cms.string("fitter_tree"),
                InputDirectoryName = cms.string("tpTree"),
                OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
                Efficiencies = cms.PSet(),
                )
                process.TnP_MuonID.WeightVariable = cms.string("weight")
                process.TnP_MuonID.Variables.weight = cms.vstring("weight","-10","10","")


#_*_*_*_*_*_*_*_*_*_*_*_*_*_*
#Choose Numerator/Denominator
#_*_*_*_*_*_*_*_*_*_*_*_*_*_*

ID_BINS = []

#_*_
#IDs
#_*_
#Loose ID
if id_bins == '1':
    ID_BINS = [
    #(("Loose_noIP"), ("NUM_LooseID_DENOM_generalTracks_VAR_eta",            ETA_BINS_INCLUSIVE_PT           )),
    #(("Loose_noIP"), ("NUM_LooseID_DENOM_generalTracks_VAR_vtx",            VTX_BINS_INCLUSIVE_ETA_PT       )),
    #(("Loose_noIP"), ("NUM_LooseID_DENOM_generalTracks_VAR_pt",             PT_BINS_INCLUSIVE_ETA           )),
    (("Loose_noIP"), ("NUM_LooseID_DENOM_generalTracks_VAR_map_pt_eta",         PT_ETA_MAP                      )),
    ]
#Medium ID
if id_bins == '2':
    ID_BINS = [
    #(("Medium_noIP"), ("NUM_MediumID_DENOM_generalTracks_VAR_eta",          ETA_BINS_INCLUSIVE_PT           )),
    #(("Medium_noIP"), ("NUM_MediumID_DENOM_generalTracks_VAR_vtx",          VTX_BINS_INCLUSIVE_ETA_PT       )),
    #(("Medium_noIP"), ("NUM_MediumID_DENOM_generalTracks_VAR_pt",           PT_BINS_INCLUSIVE_ETA           )),
    (("Medium_noIP"), ("NUM_MediumID_DENOM_generalTracks_VAR_map_pt_eta",       PT_ETA_MAP                      )),
    ]
#_*_
#IPs
#_*_
if id_bins == '3':
    ID_BINS = [
    #(("TightIP2D"), ("NUM_TightIP2D_DENOM_LooseID_VAR_eta",                 LOOSE_ETA_BINS_INCLUSIVE_PT           )),
    #(("TightIP2D"), ("NUM_TightIP2D_DENOM_LooseID_VAR_vtx",                 LOOSE_VTX_BINS_INCLUSIVE_ETA_PT       )),
    #(("TightIP2D"), ("NUM_TightIP2D_DENOM_LooseID_VAR_pt",                  LOOSE_PT_BINS_INCLUSIVE_ETA           )),
    (("TightIP2D"), ("NUM_TightIP2D_DENOM_LooseID_VAR_map_pt_eta",              LOOSE_PT_ETA_MAP                      )),
    ]                                                                                                                
if id_bins == '4':                                                                                                   
    ID_BINS = [                                                                                                      
    #(("TightIP2D"), ("NUM_TightIP2D_DENOM_MediumID_VAR_eta",                MEDIUM_ETA_BINS_INCLUSIVE_PT           )), 
    #(("TightIP2D"), ("NUM_TightIP2D_DENOM_MediumID_VAR_vtx",                MEDIUM_VTX_BINS_INCLUSIVE_ETA_PT       )),
    #(("TightIP2D"), ("NUM_TightIP2D_DENOM_MediumID_VAR_pt",                 MEDIUM_PT_BINS_INCLUSIVE_ETA           )),
    (("TightIP2D"), ("NUM_TightIP2D_DENOM_MediumID_VAR_map_pt_eta",             MEDIUM_PT_ETA_MAP                      )),
    ]
if id_bins == '5':
    ID_BINS = [
    #(("TightIP3D"), ("NUM_TightIP3D_DENOM_LooseID_VAR_eta",                 LOOSE_ETA_BINS_INCLUSIVE_PT           )),
    #(("TightIP3D"), ("NUM_TightIP3D_DENOM_LooseID_VAR_vtx",                 LOOSE_VTX_BINS_INCLUSIVE_ETA_PT       )),
    #(("TightIP3D"), ("NUM_TightIP3D_DENOM_LooseID_VAR_pt",                  LOOSE_PT_BINS_INCLUSIVE_ETA           )),
    (("TightIP3D"), ("NUM_TightIP3D_DENOM_LooseID_VAR_map_pt_eta",              LOOSE_PT_ETA_MAP                      )),
    ]
if id_bins == '6':
    ID_BINS = [
    #(("TightIP3D"), ("NUM_TightIP3D_DENOM_MediumID_VAR_eta",                MEDIUM_ETA_BINS_INCLUSIVE_PT           )),
    #(("TightIP3D"), ("NUM_TightIP3D_DENOM_MediumID_VAR_vtx",                MEDIUM_VTX_BINS_INCLUSIVE_ETA_PT       )),
    #(("TightIP3D"), ("NUM_TightIP3D_DENOM_MediumID_VAR_pt",                 MEDIUM_PT_BINS_INCLUSIVE_ETA           )),
    (("TightIP3D"), ("NUM_TightIP3D_DENOM_MediumID_VAR_map_pt_eta",             MEDIUM_PT_ETA_MAP                      )),
    ]
#_*_*
#ISOs
#_*_*
#Loose MiniIso
if id_bins == '7':
    ID_BINS = [
    #(("LooseMiniIso"), ("NUM_MiniIsoLoose_DENOM_LooseID_VAR_eta",                   LOOSE_ETA_BINS_INCLUSIVE_PT           )),
    #(("LooseMiniIso"), ("NUM_MiniIsoLoose_DENOM_LooseID_VAR_vtx",                   LOOSE_VTX_BINS_INCLUSIVE_ETA_PT       )),
    #(("LooseMiniIso"), ("NUM_MiniIsoLoose_DENOM_LooseID_VAR_pt",                    LOOSE_PT_BINS_INCLUSIVE_ETA           )),
    (("LooseMiniIso"), ("NUM_MiniIsoLoose_DENOM_LooseID_VAR_map_pt_eta",                LOOSE_PT_ETA_MAP                      )),
    #(("LooseMiniIso"), ("NUM_MiniIsoLoose_DENOM_LooseID_VAR_map_activity_eta",          LOOSE_ACTIVITY_ETA_MAP_INCLUSIVE_PT   )),
    #(("LooseMiniIso"), ("NUM_MiniIsoLoose_DENOM_LooseID_VAR_map_activity_pt",           LOOSE_ACTIVITY_PT_MAP_INCLUSIVE_ETA   )),
    ]
#Tight MiniIso
if id_bins == '8':
    ID_BINS = [
    #(("TightMiniIso"), ("NUM_MiniIsoTight_DENOM_MediumID_VAR_eta",                  MEDIUM_ETA_BINS_INCLUSIVE_PT           )),
    #(("TightMiniIso"), ("NUM_MiniIsoTight_DENOM_MediumID_VAR_vtx",                  MEDIUM_VTX_BINS_INCLUSIVE_ETA_PT       )),
    #(("TightMiniIso"), ("NUM_MiniIsoTight_DENOM_MediumID_VAR_pt",                   MEDIUM_PT_BINS_INCLUSIVE_ETA           )),
    (("TightMiniIso"), ("NUM_MiniIsoTight_DENOM_MediumID_VAR_map_pt_eta",               MEDIUM_PT_ETA_MAP                      )),
    #(("TightMiniIso"), ("NUM_MiniIsoTight_DENOM_MediumID_VAR_map_activity_eta",         MEDIUM_ACTIVITY_ETA_MAP_INCLUSIVE_PT   )),
    #(("TightMiniIso"), ("NUM_MiniIsoTight_DENOM_MediumID_VAR_map_activity_pt",          MEDIUM_ACTIVITY_PT_MAP_INCLUSIVE_ETA   )),
    ]
if id_bins == '9':
    ID_BINS = [
    #(("TightMiniIso"), ("NUM_MiniIsoTight_DENOM_LooseID_VAR_eta",                   LOOSE_ETA_BINS_INCLUSIVE_PT           )), 
    #(("TightMiniIso"), ("NUM_MiniIsoTight_DENOM_LooseID_VAR_vtx",                   LOOSE_VTX_BINS_INCLUSIVE_ETA_PT       )),
    #(("TightMiniIso"), ("NUM_MiniIsoTight_DENOM_LooseID_VAR_pt",                    LOOSE_PT_BINS_INCLUSIVE_ETA           )),
    (("TightMiniIso"), ("NUM_MiniIsoTight_DENOM_LooseID_VAR_map_pt_eta",                LOOSE_PT_ETA_MAP                      )),
    #(("TightMiniIso"), ("NUM_MiniIsoTight_DENOM_LooseID_VAR_map_activity_eta",          LOOSE_ACTIVITY_ETA_MAP_INCLUSIVE_PT   )),
    #(("TightMiniIso"), ("NUM_MiniIsoTight_DENOM_LooseID_VAR_map_activity_pt",           LOOSE_ACTIVITY_PT_MAP_INCLUSIVE_ETA   )),
    ]
#MultiIso
if id_bins == '10':
    ID_BINS = [
    #(("MediumMultiIso"), ("NUM_MultiIsoMedium_DENOM_MediumID_VAR_eta",              MEDIUM_ETA_BINS_INCLUSIVE_PT           )), 
    #(("MediumMultiIso"), ("NUM_MultiIsoMedium_DENOM_MediumID_VAR_vtx",              MEDIUM_VTX_BINS_INCLUSIVE_ETA_PT       )),
    #(("MediumMultiIso"), ("NUM_MultiIsoMedium_DENOM_MediumID_VAR_pt",               MEDIUM_PT_BINS_INCLUSIVE_ETA           )),
    (("MediumMultiIso"), ("NUM_MultiIsoMedium_DENOM_MediumID_VAR_map_pt_eta",           MEDIUM_PT_ETA_MAP                      )),
    #(("MediumMultiIso"), ("NUM_MultiIsoMedium_DENOM_MediumID_VAR_map_activity_eta",     MEDIUM_ACTIVITY_ETA_MAP_INCLUSIVE_PT   )),
    #(("MediumMultiIso"), ("NUM_MultiIsoMedium_DENOM_MediumID_VAR_map_activity_pt",      MEDIUM_ACTIVITY_PT_MAP_INCLUSIVE_ETA   )),
    ]
#Loose+MiniIso02
if id_bins == '11':
    ID_BINS = [
    (("Loose_plus_MiniIso02"), ("NUM_LooseID_plus_MiniIso02_DENOM_generalTracks_VAR_eta",                                           ETA_BINS_INCLUSIVE_PT           )),
    (("Loose_plus_MiniIso02"), ("NUM_LooseID_plus_MiniIso02_DENOM_generalTracks_VAR_vtx",                                           VTX_BINS_INCLUSIVE_ETA_PT       )),
    (("Loose_plus_MiniIso02"), ("NUM_LooseID_plus_MiniIso02_DENOM_generalTracks_VAR_pt",                                            PT_BINS_INCLUSIVE_ETA           )),
    (("Loose_plus_MiniIso02"), ("NUM_LooseID_plus_MiniIso02_DENOM_generalTracks_VAR_map_pt_eta",                                        PT_ETA_MAP                      )),
    (("Loose_plus_MiniIso02"), ("NUM_LooseID_plus_MiniIso02_DENOM_generalTracks_VAR_map_activity_eta",                                  ACTIVITY_ETA_MAP_INCLUSIVE_PT   )),
    (("Loose_plus_MiniIso02"), ("NUM_LooseID_plus_MiniIso02_DENOM_generalTracks_VAR_map_activity_pt",                                   ACTIVITY_PT_MAP_INCLUSIVE_ETA   )),
    ]
#Loose+MiniIso02+TightIP2D
if id_bins == '12':
    ID_BINS = [
    (("Loose_plus_MiniIso02_puls_TightIP2D"), ("NUM_LooseID_plus_MiniIso02_puls_TightIP2D_DENOM_generalTracks_VAR_eta",             ETA_BINS_INCLUSIVE_PT           )),
    (("Loose_plus_MiniIso02_puls_TightIP2D"), ("NUM_LooseID_plus_MiniIso02_puls_TightIP2D_DENOM_generalTracks_VAR_vtx",             VTX_BINS_INCLUSIVE_ETA_PT       )),
    (("Loose_plus_MiniIso02_puls_TightIP2D"), ("NUM_LooseID_plus_MiniIso02_puls_TightIP2D_DENOM_generalTracks_VAR_pt",              PT_BINS_INCLUSIVE_ETA           )),
    (("Loose_plus_MiniIso02_puls_TightIP2D"), ("NUM_LooseID_plus_MiniIso02_puls_TightIP2D_DENOM_generalTracks_VAR_map_pt_eta",          PT_ETA_MAP                      )),
    (("Loose_plus_MiniIso02_puls_TightIP2D"), ("NUM_LooseID_plus_MiniIso02_puls_TightIP2D_DENOM_generalTracks_VAR_map_activity_eta",    ACTIVITY_ETA_MAP_INCLUSIVE_PT   )),
    (("Loose_plus_MiniIso02_puls_TightIP2D"), ("NUM_LooseID_plus_MiniIso02_puls_TightIP2D_DENOM_generalTracks_VAR_map_activity_pt",     ACTIVITY_PT_MAP_INCLUSIVE_ETA   )),
    ]
#Medium+MiniIso02
if id_bins == '13':
    ID_BINS = [
    (("Medium_plus_MiniIso02"), ("NUM_MediumID_plus_MiniIso02_DENOM_generalTracks_VAR_eta",                                         ETA_BINS_INCLUSIVE_PT           )),
    (("Medium_plus_MiniIso02"), ("NUM_MediumID_plus_MiniIso02_DENOM_generalTracks_VAR_vtx",                                         VTX_BINS_INCLUSIVE_ETA_PT       )),
    (("Medium_plus_MiniIso02"), ("NUM_MediumID_plus_MiniIso02_DENOM_generalTracks_VAR_pt",                                          PT_BINS_INCLUSIVE_ETA           )),
    (("Medium_plus_MiniIso02"), ("NUM_MediumID_plus_MiniIso02_DENOM_generalTracks_VAR_map_pt_eta",                                      PT_ETA_MAP                      )),
    (("Medium_plus_MiniIso02"), ("NUM_MediumID_plus_MiniIso02_DENOM_generalTracks_VAR_map_activity_eta",                                ACTIVITY_ETA_MAP_INCLUSIVE_PT   )),
    (("Medium_plus_MiniIso02"), ("NUM_MediumID_plus_MiniIso02_DENOM_generalTracks_VAR_map_activity_pt",                                 ACTIVITY_PT_MAP_INCLUSIVE_ETA   )),
    ]
#Loose+MiniIso02+TightIP3D
if id_bins == '14':
    ID_BINS = [
    (("Loose_plus_MiniIso02_puls_TightIP3D"), ("NUM_LooseID_plus_MiniIso02_puls_TightIP3D_DENOM_generalTracks_VAR_eta",             ETA_BINS_INCLUSIVE_PT           )),
    (("Loose_plus_MiniIso02_puls_TightIP3D"), ("NUM_LooseID_plus_MiniIso02_puls_TightIP3D_DENOM_generalTracks_VAR_vtx",             VTX_BINS_INCLUSIVE_ETA_PT       )),
    (("Loose_plus_MiniIso02_puls_TightIP3D"), ("NUM_LooseID_plus_MiniIso02_puls_TightIP3D_DENOM_generalTracks_VAR_pt",              PT_BINS_INCLUSIVE_ETA           )),
    (("Loose_plus_MiniIso02_puls_TightIP3D"), ("NUM_LooseID_plus_MiniIso02_puls_TightIP3D_DENOM_generalTracks_VAR_map_pt_eta",          PT_ETA_MAP                      )),
    (("Loose_plus_MiniIso02_puls_TightIP3D"), ("NUM_LooseID_plus_MiniIso02_puls_TightIP3D_DENOM_generalTracks_VAR_map_activity_eta",    ACTIVITY_ETA_MAP_INCLUSIVE_PT   )),
    (("Loose_plus_MiniIso02_puls_TightIP3D"), ("NUM_LooseID_plus_MiniIso02_puls_TightIP3D_DENOM_generalTracks_VAR_map_activity_pt",     ACTIVITY_PT_MAP_INCLUSIVE_ETA   )),
    ]
#Medium+MiniIso02+TightIP3D
if id_bins == '15':
    ID_BINS = [
    (("Medium_plus_MiniIso02_puls_TightIP3D"), ("NUM_MediumID_plus_MiniIso02_puls_TightIP3D_DENOM_generalTracks_VAR_eta",           ETA_BINS_INCLUSIVE_PT           )),
    (("Medium_plus_MiniIso02_puls_TightIP3D"), ("NUM_MediumID_plus_MiniIso02_puls_TightIP3D_DENOM_generalTracks_VAR_vtx",           VTX_BINS_INCLUSIVE_ETA_PT       )),
    (("Medium_plus_MiniIso02_puls_TightIP3D"), ("NUM_MediumID_plus_MiniIso02_puls_TightIP3D_DENOM_generalTracks_VAR_pt",            PT_BINS_INCLUSIVE_ETA           )),
    (("Medium_plus_MiniIso02_puls_TightIP3D"), ("NUM_MediumID_plus_MiniIso02_puls_TightIP3D_DENOM_generalTracks_VAR_map_pt_eta",        PT_ETA_MAP                      )),
    (("Medium_plus_MiniIso02_puls_TightIP3D"), ("NUM_MediumID_plus_MiniIso02_puls_TightIP3D_DENOM_generalTracks_VAR_map_activity_eta",  ACTIVITY_ETA_MAP_INCLUSIVE_PT   )),
    (("Medium_plus_MiniIso02_puls_TightIP3D"), ("NUM_MediumID_plus_MiniIso02_puls_TightIP3D_DENOM_generalTracks_VAR_map_activity_pt",   ACTIVITY_PT_MAP_INCLUSIVE_ETA   )),
    ]
#Medium+MiniIso02+TightIP2D
if id_bins == '16':
    ID_BINS = [
    (("Medium_plus_MiniIso02_puls_TightIP2D"), ("NUM_MediumID_plus_MiniIso02_puls_TightIP2D_DENOM_generalTracks_VAR_eta",           ETA_BINS_INCLUSIVE_PT           )),
    (("Medium_plus_MiniIso02_puls_TightIP2D"), ("NUM_MediumID_plus_MiniIso02_puls_TightIP2D_DENOM_generalTracks_VAR_vtx",           VTX_BINS_INCLUSIVE_ETA_PT       )),
    (("Medium_plus_MiniIso02_puls_TightIP2D"), ("NUM_MediumID_plus_MiniIso02_puls_TightIP2D_DENOM_generalTracks_VAR_pt",            PT_BINS_INCLUSIVE_ETA           )),
    (("Medium_plus_MiniIso02_puls_TightIP2D"), ("NUM_MediumID_plus_MiniIso02_puls_TightIP2D_DENOM_generalTracks_VAR_map_pt_eta",        PT_ETA_MAP                      )),
    (("Medium_plus_MiniIso02_puls_TightIP2D"), ("NUM_MediumID_plus_MiniIso02_puls_TightIP2D_DENOM_generalTracks_VAR_map_activity_eta",  ACTIVITY_ETA_MAP_INCLUSIVE_PT   )),
    (("Medium_plus_MiniIso02_puls_TightIP2D"), ("NUM_MediumID_plus_MiniIso02_puls_TightIP2D_DENOM_generalTracks_VAR_map_activity_pt",   ACTIVITY_PT_MAP_INCLUSIVE_ETA   )),
    ]
#Medium+MultiIsoMedium+TightIP2D+TightIP3D
if id_bins == '17':
    ID_BINS = [
    (("Medium_plus_MediumMultiIso_plus_TightIP2D_plus_TightIP3D"), ("NUM_MediumID_plus_MediumMultiIso_plus_TightIP2D_plus_TightIP3D_DENOM_generalTracks_VAR_eta",           ETA_BINS_INCLUSIVE_PT           )),
    (("Medium_plus_MediumMultiIso_plus_TightIP2D_plus_TightIP3D"), ("NUM_MediumID_plus_MediumMultiIso_plus_TightIP2D_plus_TightIP3D_DENOM_generalTracks_VAR_vtx",           VTX_BINS_INCLUSIVE_ETA_PT       )),
    (("Medium_plus_MediumMultiIso_plus_TightIP2D_plus_TightIP3D"), ("NUM_MediumID_plus_MediumMultiIso_plus_TightIP2D_plus_TightIP3D_DENOM_generalTracks_VAR_pt",            PT_BINS_INCLUSIVE_ETA           )),
    (("Medium_plus_MediumMultiIso_plus_TightIP2D_plus_TightIP3D"), ("NUM_MediumID_plus_MediumMultiIso_plus_TightIP2D_plus_TightIP3D_DENOM_generalTracks_VAR_map_pt_eta",        PT_ETA_MAP                      )),
    (("Medium_plus_MediumMultiIso_plus_TightIP2D_plus_TightIP3D"), ("NUM_MediumID_plus_MediumMultiIso_plus_TightIP2D_plus_TightIP3D_DENOM_generalTracks_VAR_map_activity_eta",  ACTIVITY_ETA_MAP_INCLUSIVE_PT   )),
    (("Medium_plus_MediumMultiIso_plus_TightIP2D_plus_TightIP3D"), ("NUM_MediumID_plus_MediumMultiIso_plus_TightIP2D_plus_TightIP3D_DENOM_generalTracks_VAR_map_activity_pt",   ACTIVITY_PT_MAP_INCLUSIVE_ETA   )),
    ]

#Loose+MiniIso04+TightIP2D
if id_bins == '18':
    ID_BINS = [
    (("Loose_plus_MiniIso04_puls_TightIP2D"), ("NUM_LooseID_plus_MiniIso04_puls_TightIP2D_DENOM_generalTracks_VAR_eta",             ETA_BINS_INCLUSIVE_PT           )),
    (("Loose_plus_MiniIso04_puls_TightIP2D"), ("NUM_LooseID_plus_MiniIso04_puls_TightIP2D_DENOM_generalTracks_VAR_vtx",             VTX_BINS_INCLUSIVE_ETA_PT       )),
    (("Loose_plus_MiniIso04_puls_TightIP2D"), ("NUM_LooseID_plus_MiniIso04_puls_TightIP2D_DENOM_generalTracks_VAR_pt",              PT_BINS_INCLUSIVE_ETA           )),
    (("Loose_plus_MiniIso04_puls_TightIP2D"), ("NUM_LooseID_plus_MiniIso04_puls_TightIP2D_DENOM_generalTracks_VAR_map_pt_eta",          PT_ETA_MAP                      )),
    (("Loose_plus_MiniIso04_puls_TightIP2D"), ("NUM_LooseID_plus_MiniIso04_puls_TightIP2D_DENOM_generalTracks_VAR_map_activity_eta",    ACTIVITY_ETA_MAP_INCLUSIVE_PT   )),
    (("Loose_plus_MiniIso04_puls_TightIP2D"), ("NUM_LooseID_plus_MiniIso04_puls_TightIP2D_DENOM_generalTracks_VAR_map_activity_pt",     ACTIVITY_PT_MAP_INCLUSIVE_ETA   )),
    ]





#_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*
#Produce the efficiency .root files
#_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*


for ID, ALLBINS in ID_BINS:
    X = ALLBINS[0]
    B = ALLBINS[1]
    _output = os.getcwd() + '/Efficiency' + iteration
    if not os.path.exists(_output):
        print 'Creating', _output, 'directory where the fits are stored'  
        os.makedirs(_output)
    if scenario == 'data_all':
        _output += '/DATA' + bs + run 
    elif scenario == 'mc_all':
        _output += '/MC' + bs + run + order
    if not os.path.exists(_output):
        os.makedirs(_output)
    module = process.TnP_MuonID.clone(OutputFileName = cms.string(_output + "/TnP_MuonID_%s.root" % (X)))
    shape = cms.vstring("vpvPlusExpo")
    #shape = cms.vstring("vpvPlusCheb")

    if(("Iso" in ID) and (not "plus" in ID)):
        shape = cms.vstring("vpvPlusExpo")
    else:
    #if not "Iso" in ID:  #customize only for ID
        if ALLBINS[0].find('VAR_pt') != -1: 
                shape = cms.vstring("vpvPlusExpo","*pt_bin6*","vpvPlusCheb","*pt_bin7*","vpvPlusCheb","*pt_bin8*","vpvPlusCheb")
        if ALLBINS[0].find('VAR_map_pt_eta') != -1: 
                shape = cms.vstring("vpvPlusExpo","*pt_bin6*","vpvPlusCheb")
    
        #if (len(B.pt)>=8):  #customize only when the pT have the high pt bins
        #    if "Loose_noIP" in ID:
        #        shape = cms.vstring("vpvPlusExpo","*pt_bin5*","vpvPlusCheb","*pt_bin6*","vpvPlusCheb","*pt_bin7*","vpvPlusCheb","*pt_bin8*","vpvPlusCheb")
        #    else:
        #        shape = cms.vstring("vpvPlusExpo","*pt_bin6*","vpvPlusCheb","*pt_bin7*","vpvPlusCheb","*pt_bin8*","vpvPlusCheb")
    DEN = B.clone(); num = ID;
    #compute isolation efficiency 
    if scenario == 'data_all':
        setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
        EfficiencyCategoryAndState = cms.vstring(num,"above"),
        UnbinnedVariables = cms.vstring("mass"),
        BinnedVariables = DEN,
        BinToPDFmap = shape
        ))
        setattr(process, "TnP_MuonID_"+ID+"_"+X, module)        
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))
    elif scenario == 'mc_all':
        setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
        EfficiencyCategoryAndState = cms.vstring(num,"above"),
        UnbinnedVariables = cms.vstring("mass","weight"),
        BinnedVariables = DEN,
        BinToPDFmap = shape
        ))
        setattr(process, "TnP_MuonID_"+ID+"_"+X, module)        
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))

