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

Template = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
        NumCPU = cms.uint32(1),
    SaveWorkspace = cms.bool(False),

    Variables = cms.PSet(
        weight = cms.vstring("weight","0","10",""),
        mass = cms.vstring("Tag-muon Mass", "70", "130", "GeV/c^{2}"),
        pt = cms.vstring("muon p_{T}", "0", "1000", "GeV/c"),
        eta    = cms.vstring("muon #eta", "-2.5", "2.5", ""),
        abseta = cms.vstring("muon |#eta|", "0", "2.5", ""),
        phi    = cms.vstring("muon #phi at vertex", "-3.1416", "3.1416", ""),
        charge = cms.vstring("muon charge", "-2.5", "2.5", ""),
        combRelIsoPF04dBeta = cms.vstring("dBeta rel iso dR 0.4", "-2", "9999999", ""),
        pfCombRelActivitydBCorr = cms.vstring("Rel. Activity", "-2", "40", ""),
        pfCombRelMiniIsoEACorr = cms.vstring("EA rel Mini Iso", "-2", "9999999",""),
        PtRel = cms.vstring("PtRel", "-2", "9999999",""),
        PtRatio = cms.vstring("PtRatio", "-2", "9999999",""),
        tag_pt = cms.vstring("Tag p_{T}", "0", "1000", "GeV/c"),
        tag_nVertices   = cms.vstring("Number of vertices", "0", "999", ""),
        tag_abseta = cms.vstring("|eta| of tag muon", "0", "2.5", ""),
        tag_combRelIsoPF04dBeta = cms.vstring("Tag dBeta rel iso dR 0.4", "-2", "9999999", ""),
        dB = cms.vstring("dB", "-1000", "1000", ""),
        dzPV = cms.vstring("dzPV", "-1000", "1000", ""),
        dxyBS = cms.vstring("dxyBS", "-1000", "1000", ""),
        SIP = cms.vstring("SIP", "-1000", "1000", ""),
        pair_probeMultiplicity = cms.vstring("pair_probeMultiplicity", "0","30",""),
        ),

    Categories = cms.PSet(
        PF    = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
        Medium   = cms.vstring("Medium Id. Muon", "dummy[pass=1,fail=0]"),
        Tight2012 = cms.vstring("Tight Id. Muon", "dummy[pass=1,fail=0]"),
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
        MediumMultiIsoVar= cms.vstring("MediumMultIsoVar" ,"pfCombRelMiniIsoEACorr < 0.16 && ( PtRel > 7.2 || PtRatio > 0.76 )", "pfCombRelMiniIsoEACorr", "PtRel", "PtRatio"),
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
        Tight2012_zIPCut = cms.vstring("Tight2012_zIPCut", "Tight2012_zIPCutVar", "0.5"),
        #MiniIsolations
        LooseMiniIso = cms.vstring("LooseMiniIso" ,"LooseMiniIsoVar", "0.5"),
        TightMiniIso = cms.vstring("TightMiniIso" ,"TightMiniIsoVar", "0.5"),
        #Multi Iso
        MediumMultiIso= cms.vstring("MediumMultiIso" ,"MediumMultiIsoVar", "0.5"),
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

ETA_BINS = cms.PSet(
    pt  = cms.vdouble(10, 500),
    eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
VTX_BINS_ETA24  = cms.PSet(
    pt     = cms.vdouble(10 , 500),
    abseta = cms.vdouble(  0.0, 2.4),
    tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
PT_ALLETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(10, 20, 30, 40, 50, 60, 80, 120, 200),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
PT_ETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(10, 20, 30, 40, 50, 60, 80, 120, 200),
    abseta = cms.vdouble( 0.0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
#For IP,ISO on ID
LOOSE_ETA_BINS = cms.PSet(
    pt  = cms.vdouble(10, 500),
    eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
LOOSE_VTX_BINS_ETA24  = cms.PSet(
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
LOOSE_PT_ALLETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(10, 20, 30, 40, 50, 60, 80, 120, 200),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
LOOSE_PT_ETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(10, 20, 30, 40, 50, 60, 80, 120, 200),
    abseta = cms.vdouble(  0.0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
LOOSE_PT_ACTIVITY_BARREL = cms.PSet(
    pfCombRelActivitydBCorr = cms.vdouble(0, 0.02, 0.05, 0.15, 1),
    pt     = cms.vdouble(10, 500),
    abseta = cms.vdouble( 0, 1.2),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
LOOSE_PT_ACTIVITY_ENDCAP = cms.PSet(
    pfCombRelActivitydBCorr = cms.vdouble(0, 0.02, 0.05, 0.15, 1),
    pt     = cms.vdouble(10, 500),
    abseta = cms.vdouble( 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
#
LOOSE_PT_ACTIVITY_PTLOW = cms.PSet(
    pfCombRelActivitydBCorr = cms.vdouble(0, 0.02, 0.05, 0.15, 1),
    pt     = cms.vdouble(10, 40),
    abseta = cms.vdouble( 0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
LOOSE_PT_ACTIVITY_PTMED= cms.PSet(
    pfCombRelActivitydBCorr = cms.vdouble(0, 0.02, 0.05, 0.15, 1),
    pt     = cms.vdouble(40, 80),
    abseta = cms.vdouble( 0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
LOOSE_PT_ACTIVITY_PTHIGH= cms.PSet(
    pfCombRelActivitydBCorr = cms.vdouble(0, 0.02, 0.05, 0.15, 1),
    pt     = cms.vdouble(80, 200),
    abseta = cms.vdouble( 0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
#MEDIUM
MEDIUM_ETA_BINS = cms.PSet(
    pt  = cms.vdouble(10, 500),
    eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_VTX_BINS_ETA24  = cms.PSet(
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
MEDIUM_PT_ALLETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(10, 20, 30, 40, 50, 60, 80, 120, 200),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_PT_ETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(10, 20, 30, 40, 50, 60, 80, 120, 200),
    abseta = cms.vdouble(  0.0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_PT_ACTIVITY_BARREL = cms.PSet(
    pfCombRelActivitydBCorr = cms.vdouble(0, 0.02, 0.05, 0.15, 1),
    pt     = cms.vdouble(10, 500),
    abseta = cms.vdouble( 0, 1.2),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_PT_ACTIVITY_ENDCAP = cms.PSet(
    pfCombRelActivitydBCorr = cms.vdouble(0, 0.02, 0.05, 0.15, 1),
    pt     = cms.vdouble(10, 500),
    abseta = cms.vdouble( 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
#
MEDIUM_PT_ACTIVITY_PTLOW= cms.PSet(
    pfCombRelActivitydBCorr = cms.vdouble(0, 0.02, 0.05, 0.15, 1),
    pt     = cms.vdouble(10, 40),
    abseta = cms.vdouble( 0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_PT_ACTIVITY_PTMED= cms.PSet(
    pfCombRelActivitydBCorr = cms.vdouble(0, 0.02, 0.05, 0.15, 1),
    pt     = cms.vdouble(40, 80),
    abseta = cms.vdouble( 0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_PT_ACTIVITY_PTHIGH= cms.PSet(
    pfCombRelActivitydBCorr = cms.vdouble(0, 0.02, 0.05, 0.15, 1),
    pt     = cms.vdouble(80, 200),
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
                    'root://eoscms//eos/cms/store/group/phys_muon/perrin/SUSY/tnp_DATA_25ns_2015D_v3v4_withEAMiniIso_v2.root'
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
                'root://eoscms//eos/cms/store/group/phys_muon/perrin/SUSY/tnp_MC_25ns_2015D_LO_SmallTree_withNVtxWeights_withEAMiniIso_v2.root'
                    ),
                InputTreeName = cms.string("fitter_tree"),
                InputDirectoryName = cms.string("tpTree"),
                OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
                Efficiencies = cms.PSet(),
                )
                process.TnP_MuonID.WeightVariable = cms.string("weight")
                process.TnP_MuonID.Variables.weight = cms.vstring("weight","0","10","")
            elif order == 'NLO':
                process.TnP_MuonID = Template.clone(
                InputFileNames = cms.vstring(
                'root://eoscms//eos/cms/store/group/phys_muon/perrin/SUSY/tnp_MC_25ns_2015D_NLO_SmallTree_withNVtxWeights_WithWeights_withEAMiniIso_v2.root'
                    ),
                InputTreeName = cms.string("fitter_tree"),
                InputDirectoryName = cms.string("tpTree"),
                OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
                Efficiencies = cms.PSet(),
                )
                process.TnP_MuonID.WeightVariable = cms.string("weight")
                process.TnP_MuonID.Variables.weight = cms.vstring("weight","0","10","")


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
    (("Loose_noIP"), ("eta", ETA_BINS)),
    (("Loose_noIP"), ("vtx_bin1_24", VTX_BINS_ETA24 )),
    (("Loose_noIP"), ("pt_alleta_bin1", PT_ALLETA_BINS1)),
    (("Loose_noIP"), ("pt_spliteta_bin1", PT_ETA_BINS1)),
    ]
#Medium ID
if id_bins == '2':
    ID_BINS = [
    (("Medium_noIP"), ("eta", ETA_BINS)),
    (("Medium_noIP"), ("vtx_bin1_24", VTX_BINS_ETA24 )),
    (("Medium_noIP"), ("pt_alleta_bin1", PT_ALLETA_BINS1)),
    (("Medium_noIP"), ("pt_spliteta_bin1", PT_ETA_BINS1)),
    ]
#_*_
#IPs
#_*_
if id_bins == '3':
    ID_BINS = [
    (("TightIP2D"), ("loose_eta", LOOSE_ETA_BINS)),
    (("TightIP2D"), ("loose_vtx_bin1_24", LOOSE_VTX_BINS_ETA24 )),
    (("TightIP2D"), ("loose_pt_alleta_bin1", LOOSE_PT_ALLETA_BINS1)),
    (("TightIP2D"), ("loose_pt_spliteta_bin1", LOOSE_PT_ETA_BINS1)),
    ]
if id_bins == '4':
    ID_BINS = [
    (("TightIP2D"), ("medium_eta", MEDIUM_ETA_BINS)),
    (("TightIP2D"), ("medium_vtx_bin1_24", MEDIUM_VTX_BINS_ETA24 )),
    (("TightIP2D"), ("medium_pt_alleta_bin1", MEDIUM_PT_ALLETA_BINS1)),
    (("TightIP2D"), ("medium_pt_spliteta_bin1", MEDIUM_PT_ETA_BINS1)),
    ]
if id_bins == '5':
    ID_BINS = [
    (("TightIP3D"), ("loose_eta", LOOSE_ETA_BINS)),
    (("TightIP3D"), ("loose_vtx_bin1_24", LOOSE_VTX_BINS_ETA24 )),
    (("TightIP3D"), ("loose_pt_alleta_bin1", LOOSE_PT_ALLETA_BINS1)),
    (("TightIP3D"), ("loose_pt_spliteta_bin1", LOOSE_PT_ETA_BINS1)),
    ]
if id_bins == '6':
    ID_BINS = [
    (("TightIP3D"), ("medium_eta", MEDIUM_ETA_BINS)),
    (("TightIP3D"), ("medium_vtx_bin1_24", MEDIUM_VTX_BINS_ETA24 )),
    (("TightIP3D"), ("medium_pt_alleta_bin1", MEDIUM_PT_ALLETA_BINS1)),
    (("TightIP3D"), ("medium_pt_spliteta_bin1", MEDIUM_PT_ETA_BINS1)),
    ]
#_*_*
#ISOs
#_*_*
#Loose MiniIso
if id_bins == '7':
    ID_BINS = [
    (("LooseMiniIso"), ("loose_eta", LOOSE_ETA_BINS)),
    (("LooseMiniIso"), ("loose_vtx_bin1_24", LOOSE_VTX_BINS_ETA24 )),
    (("LooseMiniIso"), ("loose_pt_alleta_bin1", LOOSE_PT_ALLETA_BINS1)),
    (("LooseMiniIso"), ("loose_pt_spliteta_bin1", LOOSE_PT_ETA_BINS1)),
    (("LooseMiniIso"), ("loose_pt_activity_barrel", LOOSE_PT_ACTIVITY_BARREL)),
    (("LooseMiniIso"), ("loose_pt_activity_endcap", LOOSE_PT_ACTIVITY_ENDCAP)),
    (("LooseMiniIso"), ("loose_pt_activity_lowpt", LOOSE_PT_ACTIVITY_PTLOW)),
    (("LooseMiniIso"), ("loose_pt_activity_medpt", LOOSE_PT_ACTIVITY_PTMED)),
    (("LooseMiniIso"), ("loose_pt_activity_highpt", LOOSE_PT_ACTIVITY_PTHIGH)),
    ]
#Tight MiniIso
if id_bins == '8':
    ID_BINS = [
    (("TightMiniIso"), ("medium_eta", MEDIUM_ETA_BINS)),
    (("TightMiniIso"), ("medium_vtx_bin1_24", MEDIUM_VTX_BINS_ETA24 )),
    (("TightMiniIso"), ("medium_pt_alleta_bin1", MEDIUM_PT_ALLETA_BINS1)),
    (("TightMiniIso"), ("medium_pt_spliteta_bin1", MEDIUM_PT_ETA_BINS1)),
    (("TightMiniIso"), ("medium_pt_activity_barrel", MEDIUM_PT_ACTIVITY_BARREL)),
    (("TightMiniIso"), ("medium_pt_activity_endcap", MEDIUM_PT_ACTIVITY_ENDCAP)),
    (("TightMiniIso"), ("medium_pt_activity_lowpt", MEDIUM_PT_ACTIVITY_PTLOW)),
    (("TightMiniIso"), ("medium_pt_activity_medpt", MEDIUM_PT_ACTIVITY_PTMED)),
    (("TightMiniIso"), ("medium_pt_activity_highpt", MEDIUM_PT_ACTIVITY_PTHIGH)),
    ]
if id_bins == '9':
    ID_BINS = [
    (("TightMiniIso"), ("loose_eta", LOOSE_ETA_BINS)),
    (("TightMiniIso"), ("loose_vtx_bin1_24", LOOSE_VTX_BINS_ETA24 )),
    (("TightMiniIso"), ("loose_pt_alleta_bin1", LOOSE_PT_ALLETA_BINS1)),
    (("TightMiniIso"), ("loose_pt_spliteta_bin1", LOOSE_PT_ETA_BINS1)),
    (("TightMiniIso"), ("loose_pt_activity_barrel", LOOSE_PT_ACTIVITY_BARREL)),
    (("TightMiniIso"), ("loose_pt_activity_endcap", LOOSE_PT_ACTIVITY_ENDCAP)),
    (("TightMiniIso"), ("loose_pt_activity_lowpt", LOOSE_PT_ACTIVITY_PTLOW)),
    (("TightMiniIso"), ("loose_pt_activity_medpt", LOOSE_PT_ACTIVITY_PTMED)),
    (("TightMiniIso"), ("loose_pt_activity_highpt", LOOSE_PT_ACTIVITY_PTHIGH)),
    ]
#MultiIso
if id_bins == '10':
    ID_BINS = [
    (("MediumMultiIso"), ("medium_eta", MEDIUM_ETA_BINS)),
    (("MediumMultiIso"), ("medium_vtx_bin1_24", MEDIUM_VTX_BINS_ETA24 )),
    (("MediumMultiIso"), ("medium_pt_alleta_bin1", MEDIUM_PT_ALLETA_BINS1)),
    (("MediumMultiIso"), ("medium_pt_spliteta_bin1", MEDIUM_PT_ETA_BINS1)),
    (("MediumMultiIso"), ("medium_pt_activity_barrel", MEDIUM_PT_ACTIVITY_BARREL)),
    (("MediumMultiIso"), ("medium_pt_activity_endcap", MEDIUM_PT_ACTIVITY_ENDCAP)),
    (("MediumMultiIso"), ("medium_pt_activity_lowpt", MEDIUM_PT_ACTIVITY_PTLOW)),
    (("MediumMultiIso"), ("medium_pt_activity_medpt", MEDIUM_PT_ACTIVITY_PTMED)),
    (("MediumMultiIso"), ("medium_pt_activity_highpt", MEDIUM_PT_ACTIVITY_PTHIGH)),
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
    module = process.TnP_MuonID.clone(OutputFileName = cms.string(_output + "/TnP_MuonID_%s_%s.root" % (ID, X)))
    shape = "vpvPlusExpo"
    DEN = B.clone(); num = ID;

    #compute isolation efficiency 
    if scenario == 'data_all':
        setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
        EfficiencyCategoryAndState = cms.vstring(num,"above"),
        UnbinnedVariables = cms.vstring("mass"),
        BinnedVariables = DEN,
        BinToPDFmap = cms.vstring(shape)
        ))
        setattr(process, "TnP_MuonID_"+ID+"_"+X, module)        
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))
    elif scenario == 'mc_all':
        setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
        EfficiencyCategoryAndState = cms.vstring(num,"above"),
        UnbinnedVariables = cms.vstring("mass","weight"),
        BinnedVariables = DEN,
        BinToPDFmap = cms.vstring(shape)
        ))
        setattr(process, "TnP_MuonID_"+ID+"_"+X, module)        
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))

