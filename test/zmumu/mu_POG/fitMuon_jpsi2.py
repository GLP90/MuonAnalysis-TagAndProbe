import FWCore.ParameterSet.Config as cms
import sys, os, shutil
from optparse import OptionParser
### USAGE: cmsRun fitMuon_jpsi2.py TEST gentracks tight data_all data 
###_den: tight, loose, medium, soft
###
###
###

#_*_*_*_*_*_
#Read Inputs
#_*_*_*_*_*_

args = sys.argv[1:]
iteration = ''
if len(args) > 1: iteration = args[1]
print "The iteration is", iteration
_den = 'tight'
if len(args) > 2: _den = args[2]
print 'The _den is', _den
_num = 'tight'
if len(args) > 3: _num = args[3]
print 'The _num is', _num
scenario = "data_all"
if len(args) > 4: scenario = args[4]
print "Will run scenario ", scenario
sample = 'data'
if len(args) > 5: sample = args[5]
print 'The sample is', sample 

process = cms.Process("TagProbe")
process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

if not _den in ['gentracks', 'loose', 'medium', 'tight', 'soft']: 
    print '@ERROR: _num should be \'loos\', \'medium\', \'tight\' of \'soft\'. You used', _den, '.Abort'
    sys.exit()
if not _num in ['loose', 'tight']: 
    print '@ERROR: _num should be \'noiso\', \'loos\' or \'tight\'. You used', _num, '.Abort'
    sys.exit()

#_*_*_*_*_*_*_*_*_*_*_*_*
#Prepare variables, den, num and fit funct
#_*_*_*_*_*_*_*_*_*_*_*_*

#Set-up the mass range
#_mrange = "70"
#if not _num == 'noiso': 
#    _mrange = "77"
#print '_mrange is', _mrange


Template = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
        NumCPU = cms.uint32(1),
    SaveWorkspace = cms.bool(False),


    Variables = cms.PSet(
        #essential for all den/num
        weight = cms.vstring("weight","-100","100",""),
        #mass = cms.vstring("Tag-muon Mass", _mrange, "130", "GeV/c^{2}"),
        mass = cms.vstring("Tag-muon Mass", "2.9", "3.3", "GeV/c^{2}"), #2.8-3.35
        #variables for track only DEN
        pt = cms.vstring("muon p_{T}", "0", "1000", "GeV/c"),
        eta    = cms.vstring("muon #eta", "-2.5", "2.5", ""),
        abseta = cms.vstring("muon |#eta|", "0", "2.5", ""),
        pair_probeMultiplicity = cms.vstring("pair_probeMultiplicity", "0","30",""),
        pair_drM1   = cms.vstring("#Delta R(Station 1)", "-99999", "999999", "rad"),
        #variables for tightID
        dzPV = cms.vstring("dzPV", "-1000", "1000", ""),
        #for Iso
        combRelIsoPF04dBeta = cms.vstring("dBeta rel iso dR 0.4", "-2", "9999999", ""),
        #tag selection
        tag_combRelIsoPF04dBeta = cms.vstring("Tag dBeta rel iso dR 0.4", "-2", "9999999", ""),
        tag_pt = cms.vstring("Tag p_{T}", "0", "1000", "GeV/c"),
        ),

    Categories = cms.PSet(
        PF    = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
        Tight2012 = cms.vstring("Tight Id. Muon", "dummy[pass=1,fail=0]"),
        #tag selection
        tag_IsoMu20 = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
	# 2015 triggers
        tag_Mu7p5_MU = cms.vstring("ProbeTrigger_Track0", "dummy[pass=1,fail=0]"),
        Mu7p5_Track2_Jpsi_TK = cms.vstring("ProbeTrigger_Track0", "dummy[pass=1,fail=0]"),
        tag_Mu7p5_Track2_Jpsi_MU = cms.vstring("ProbeTrigger_Track0", "dummy[pass=1,fail=0]"),
        Mu7p5_Track3p5_Jpsi_TK = cms.vstring("ProbeTrigger_Track0", "dummy[pass=1,fail=0]"),
        tag_Mu7p5_Track3p5_Jpsi_MU = cms.vstring("ProbeTrigger_Track0", "dummy[pass=1,fail=0]"),
        Mu7p5_Track7_Jpsi_TK = cms.vstring("ProbeTrigger_Track0", "dummy[pass=1,fail=0]"),
        tag_Mu7p5_Track7_Jpsi_MU = cms.vstring("ProbeTrigger_Track0", "dummy[pass=1,fail=0]"),
        #
        Mu7p5_L2Mu2_Jpsi_L2 = cms.vstring("ProbeTrigger_Track0", "dummy[pass=1,fail=0]"),
        tag_Mu7p5_L2Mu2_Jpsi_MU = cms.vstring("ProbeTrigger_Track0", "dummy[pass=1,fail=0]"),
        Mu7p5_L2Mu2_L2 = cms.vstring("ProbeTrigger_Track0", "dummy[pass=1,fail=0]"),
    ),

    Expressions = cms.PSet(
        #ID 
        Loose_noIPVar = cms.vstring("Loose_noIPVar", "PF==1", "PF"),
        Tight2012_zIPCutVar = cms.vstring("Tight2012_zIPCut", "Tight2012 == 1 && abs(dzPV) < 0.5", "Tight2012", "dzPV"),
    ),

    Cuts = cms.PSet(
        #ID
        Loose_noIP = cms.vstring("Loose_noIP", "Loose_noIPVar", "0.5"),
        Tight2012_zIPCut = cms.vstring("Tight2012_zIPCut", "Tight2012_zIPCutVar", "0.5"),
        #Isolations
        LooseIso4 = cms.vstring("LooseIso4" ,"combRelIsoPF04dBeta", "0.25"),
        TightIso4 = cms.vstring("TightIso4" ,"combRelIsoPF04dBeta", "0.15"),
    ),

                          
    PDFs = cms.PSet(
        signalPlusBkg = cms.vstring(
            "CBShape::signal(mass, mean[3.1,3.0,3.2], sigma[0.05,0.02,0.06], alpha[3., 0.5, 5.], n[1, 0.1, 100.])",
            #"Chebychev::backgroundPass(mass, {cPass[0,-0.5,0.5], cPass2[0,-0.5,0.5]})",
            #"Chebychev::backgroundFail(mass, {cFail[0,-0.5,0.5], cFail2[0,-0.5,0.5]})",
            #"Gaussian::signal(mass, mean[3.1,3.0,3.2], sigma[0.05,0.02,0.1])",
            "Exponential::backgroundPass(mass, lp[0,-5,5])",
            "Exponential::backgroundFail(mass, lf[0,-5,5])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        )
    ),

    binnedFit = cms.bool(True),
    binsForFit = cms.uint32(40),
    saveDistributionsPlot = cms.bool(False),

    Efficiencies = cms.PSet(), # will be filled later
)

#_*_*_*_*_*_*_*_*_*_*_*_*
#Denominators and Binning
#_*_*_*_*_*_*_*_*_*_*_*_*
#For ID

#pT_binning = cms.vdouble(2.0, 2.5, 3.0, 3.5, 4.0, 4.75, 5.5, 7.5, 10.0, 20.0, 40.0)
pT_binning = cms.vdouble(7.5, 10.0, 15.0, 20.0)
pT_coarse_binning = cms.vdouble(0,40)

eta_binning = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4),
abseta_binning = cms.vdouble(0.0, 0.9, 1.2, 2.1, 2.4)

PT_ALLETA_BINS = cms.PSet(
    #Main
    pt     = cms.vdouble(20, 25, 30, 40, 50, 60, 80, 120, 200),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    #tag_pt = cms.vdouble(21, 500),
    #tag_IsoMu20 = cms.vstring("pass"), 
    #tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
PT_ETA_BINS = cms.PSet(
    #Main
    #pt     = cms.vdouble(20, 25, 30, 40, 50, 60, 120),
    pt     = pT_binning,
    Mu7p5_Track7_Jpsi_TK = cms.string("pass"),
    #For testing bkg function
    #pt     = cms.vdouble(60, 80, 120, 200),
    #abseta = cms.vdouble( 0., 0.9, 1.2, 2.1, 2.4),
    abseta = abseta_binning,
    #tag
    tag_Mu7p5_Track7_Jpsi_MU = cms.string("pass"),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    pair_drM1 = cms.vdouble(0.5,10),
    #tag selections
    #tag_pt = cms.vdouble(21, 500),
    #tag_IsoMu20 = cms.vstring("pass"), 
    #tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
    
)
PT_HIGHABSETA = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 50, 60, 80, 120, 200),
    abseta = cms.vdouble(2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)

#For IP on ISO 
LOOSE_ETA_BINS = cms.PSet(
    pt  = cms.vdouble(20, 500),
    eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
LOOSE_COARSE_ETA_BINS = cms.PSet(
    #Main
    pt     = cms.vdouble(20, 500),
    abseta = cms.vdouble(0.0, 0.9, 1.2, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
LOOSE_PT_ALLETA_BINS = cms.PSet(
    pt     = cms.vdouble(20, 25, 30, 40, 50, 60, 80, 120, 200),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
LOOSE_PT_ETA_BINS = cms.PSet(
    #pt     = cms.vdouble(20, 25, 30, 40, 50, 60, 80, 120, 200),
    pt     = cms.vdouble(20, 25, 30, 40, 50, 60, 120),
    abseta = cms.vdouble( 0., 0.9, 1.2, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
    
)
#MEDIUM
MEDIUM_ETA_BINS = cms.PSet(
    pt  = cms.vdouble(20, 500),
    eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_COARSE_ETA_BINS = cms.PSet(
    #Main
    pt     = cms.vdouble(20, 500),
    abseta = cms.vdouble(0.0, 0.9, 1.2, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_PT_ALLETA_BINS = cms.PSet(
    pt     = cms.vdouble(20, 25, 30, 40, 50, 60, 80, 120, 200),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_PT_ETA_BINS = cms.PSet(
    #pt     = cms.vdouble(20, 25, 30, 40, 50, 60, 80, 120, 200),
    pt     = cms.vdouble(20, 25, 30, 40, 50, 60, 120),
    abseta = cms.vdouble( 0., 0.9, 1.2, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
    
)
#TIGHT
TIGHT_ETA_BINS = cms.PSet(
    pt  = cms.vdouble(20, 500),
    eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Tight2012 = cms.vstring("pass"), 
    dzPV = cms.vdouble(-0.5, 0.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
TIGHT_COARSE_ETA_BINS = cms.PSet(
    #Main
    pt     = cms.vdouble(20, 500),
    abseta = cms.vdouble(0.0, 0.9, 1.2, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Tight2012 = cms.vstring("pass"), 
    dzPV = cms.vdouble(-0.5, 0.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
TIGHT_PT_ALLETA_BINS = cms.PSet(
    pt     = cms.vdouble(20, 25, 30, 40, 50, 60, 80, 120, 200),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Tight2012 = cms.vstring("pass"), 
    dzPV = cms.vdouble(-0.5, 0.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
TIGHT_PT_ETA_BINS = cms.PSet(
    #pt     = cms.vdouble(20, 25, 30, 40, 50, 60, 80, 120, 200),
    pt     = cms.vdouble(20, 25, 30, 40, 50, 60, 120),
    abseta = cms.vdouble( 0., 0.9, 1.2, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Tight2012 = cms.vstring("pass"), 
    dzPV = cms.vdouble(-0.5, 0.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
    
)

if sample == "mc":
    process.TnP_MuonID = Template.clone(
        InputFileNames = cms.vstring(
            #'samples/TnPTree_76X_DYLL_M50_MadGraphMLM_withNVtxWeights_total.root'
            '/afs/cern.ch/work/g/gaperrin/private/TnP/TnP76/CMSSW_7_6_3_patch2/src/MuonAnalysis/TagAndProbe/test/zmumu/mu_POG/samples/tnpJPsi_MC_JPsiPt8_full.root'
            ),
        InputTreeName = cms.string("fitter_tree"),
        InputDirectoryName = cms.string("tpTree"),
        OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
        Efficiencies = cms.PSet(),
        )
if sample == "data":
    process.TnP_MuonID = Template.clone(
        InputFileNames = cms.vstring(
            '/afs/cern.ch/work/g/gaperrin/private/TnP/TnP76/CMSSW_7_6_3_patch2/src/MuonAnalysis/TagAndProbe/test/zmumu/mu_POG/samples/tnpJPsi_MC_JPsiPt8_full_withNVtxWeights.root'
            ),
        InputTreeName = cms.string("fitter_tree"),
        InputDirectoryName = cms.string("tpTree"),
        OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
        Efficiencies = cms.PSet(),
        )

if scenario == "mc_all":
    print "Including the weight for MC"
    process.TnP_MuonID.WeightVariable = cms.string("weight")
    process.TnP_MuonID.Variables.weight = cms.vstring("weight","0","10","")
    

ID_BINS = []

#_*_*_*_*_*_*_*_*_*_*
#IDs/Den pair
#_*_*_*_*_*_*_*_*_*_*

#Loose ID
if _den == 'gentracks' and _num == 'loose':
    ID_BINS = [
    #(("Loose_noIP"), ("NUM_LooseID_DEN_genTracks_PAR_eta", ETA_BINS)),
    #(("Loose_noIP"), ("NUM_LooseID_DEN_genTracks_PAR_pt_alleta_bin1", PT_ALLETA_BINS)),
    (("Loose_noIP"), ("NUM_LooseID_DEN_genTracks_PAR_pt_spliteta_bin1", PT_ETA_BINS)),
    ]
#Medium ID
elif _den == 'gentracks' and _num == 'medium':
    ID_BINS = [
    (("Medium_noIP"), ("NUM_MediumID_DEN_genTracks_PAR_eta", ETA_BINS)),
    (("Medium_noIP"), ("NUM_MediumID_DEN_genTracks_PAR_pt_alleta_bin1", PT_ALLETA_BINS)),
    (("Medium_noIP"), ("NUM_MediumID_DEN_genTracks_PAR_pt_spliteta_bin1", PT_ETA_BINS)),
    ]
#Tight ID
elif _den == 'gentracks' and _num == 'tight':
    ID_BINS = [
    #(("Tight2012_zIPCut"), ("NUM_TightIDandIPCut_DEN_genTracks_PAR_eta", ETA_BINS)),
    #(("Tight2012_zIPCut"), ("NUM_TightIDandIPCut_DEN_genTracks_PAR_pt_alleta_bin1", PT_ALLETA_BINS)),
    (("Tight2012_zIPCut"), ("NUM_TightIDandIPCut_DEN_genTracks_PAR_pt_spliteta_bin1", PT_ETA_BINS)),
    ]
#SoftID
elif _den == 'gentracks' and _num == 'soft':
    ID_BINS = [
    (("SoftID"), ("NUM_SoftID_DEN_genTracks_PAR_eta", ETA_BINS)),
    (("SoftID"), ("NUM_SoftID_DEN_genTracks_PAR_pt_alleta_bin1", PT_ALLETA_BINS)),
    (("SoftID"), ("NUM_SoftID_DEN_genTracks_PAR_pt_spliteta_bin1", PT_ETA_BINS)),
    ]

#_*_*_*_*_*_*_*_*_*_*
#ISOs
#_*_*_*_*_*_*_*_*_*_*
#Loose Iso
elif _den == 'loose' and _num == 'loose':
    ID_BINS = [
    (("LooseIso4"), ("NUM_LooseRelIso_DEN_LooseID_PAR_eta", LOOSE_ETA_BINS)),
    (("LooseIso4"), ("NUM_LooseRelIso_DEN_LooseID_PAR_pt_alleta_bin1", LOOSE_PT_ALLETA_BINS)),
    (("LooseIso4"), ("NUM_LooseRelIso_DEN_LooseID_PAR_pt_spliteta_bin1", LOOSE_PT_ETA_BINS)),
    ]
elif _den == 'medium' and _num == 'loose':
    ID_BINS = [
    (("LooseIso4"), ("NUM_LooseRelIso_DEN_MediumID_PAR_eta", MEDIUM_ETA_BINS)),
    (("LooseIso4"), ("NUM_LooseRelIso_DEN_MediumID_PAR_pt_alleta_bin1", MEDIUM_PT_ALLETA_BINS)),
    (("LooseIso4"), ("NUM_LooseRelIso_DEN_MediumID_PAR_pt_spliteta_bin1", MEDIUM_PT_ETA_BINS)),
    ]
elif _den == 'tight' and _num == 'loose':
    ID_BINS = [
    (("LooseIso4"), ("NUM_LooseRelIso_DEN_TightID_PAR_eta", TIGHT_ETA_BINS)),
    (("LooseIso4"), ("NUM_LooseRelIso_DEN_TightID_PAR_pt_alleta_bin1", TIGHT_PT_ALLETA_BINS)),
    (("LooseIso4"), ("NUM_LooseRelIso_DEN_TightID_PAR_pt_spliteta_bin1", TIGHT_PT_ETA_BINS)),
    ]
#Tight Iso
elif _den == 'tight' and _num == 'tight':
    ID_BINS = [
    (("TightIso4"), ("NUM_TightRelIso_DEN_TightID_PAR_eta", TIGHT_ETA_BINS)),
    (("TightIso4"), ("NUM_TightRelIso_DEN_TightID_PAR_pt_alleta_bin1", TIGHT_PT_ALLETA_BINS)),
    (("TightIso4"), ("NUM_TightRelIso_DEN_TightID_PAR_pt_spliteta_bin1", TIGHT_PT_ETA_BINS)),
    ]
elif _den == 'medium' and _num == 'tight':
    ID_BINS = [
    (("TightIso4"), ("NUM_TightRelIso_DEN_MediumID_PAR_eta", MEDIUM_ETA_BINS)),
    (("TightIso4"), ("NUM_TightRelIso_DEN_MediumID_PAR_pt_alleta_bin1", MEDIUM_PT_ALLETA_BINS)),
    (("TightIso4"), ("NUM_TightRelIso_DEN_MediumID_PAR_pt_spliteta_bin1", MEDIUM_PT_ETA_BINS)),
    ]
else:
    print "@ERROR: no combination for _den", _den, "and _num", _num, '. Abort.'
    sys.exit()


#_*_*_*_*_*_*_*_*_*_*_*
#Launch fit production
#_*_*_*_*_*_*_*_*_*_*_*

for ID, ALLBINS in ID_BINS:
    X = ALLBINS[0]
    B = ALLBINS[1]
    _output = os.getcwd() + '/Efficiency' + iteration
    if not os.path.exists(_output):
        print 'Creating', '/Efficiency' + iteration,', the directory where the fits are stored.'  
        os.makedirs(_output)
    if scenario == 'data_all':
        _output += '/DATA' + '_' + sample
    elif scenario == 'mc_all':
        _output += '/MC' + '_' + sample
    if not os.path.exists(_output):
        os.makedirs(_output)
    module = process.TnP_MuonID.clone(OutputFileName = cms.string(_output + "/TnP_MC_%s.root" % (X)))
    #save the fitconfig in the plot directory
    shutil.copyfile(os.getcwd()+'/fitMuon_jpsi2.py',_output+'/fitMuon_jpsi2.py')
    shape = cms.vstring("signalPlusBkg")

    DEN = B.clone(); num = ID;

    #compute isolation efficiency 
    if scenario == 'data_all':
        if num.find("Iso4") != -1: 
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num,"below"),
                UnbinnedVariables = cms.vstring("mass"),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        else:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num,"above"),
                UnbinnedVariables = cms.vstring("mass"),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        setattr(process, "TnP_MuonID_"+ID+"_"+X, module)        
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))
    elif scenario == 'mc_all':
        if num.find("Iso4") != -1: 
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num,"below"),
                UnbinnedVariables = cms.vstring("mass","weight"),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        else:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num,"above"),
                UnbinnedVariables = cms.vstring("mass","weight"),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        setattr(process, "TnP_MuonID_"+ID+"_"+X, module)        
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))

