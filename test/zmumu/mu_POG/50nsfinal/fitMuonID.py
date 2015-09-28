import FWCore.ParameterSet.Config as cms
### USAGE:
###    cmsRun fitMuonID.py <scenario> [ <id> [ <binning1> ... <binningN> ] ]
###
### scenarios:
###   - data_all (default)  
###   - signal_mc

import sys, os
args = sys.argv[1:]
scenario = "data_all"
if len(args) > 1: scenario = args[1]
print "Will run scenario ", scenario 
bs = '50ns'
if len(args) > 2: 
    bs = args[2]
print 'the bunch spacing is', bs 
run = '2015B' 
if len(args) > 3: 
    run  = args[3]
print 'run is', run
id_bins = '1'
if len(args) > 4: 
    id_bins = args[4]
print 'id_bins is', 
id_bins
#for MC
order = 'LO'
if len(args) > 5: 
    if scenario == 'data_all':
        print "@WARINING: no order variable is necessasry for data"
    order = args[5]
print 'order is', order

#scenario = "mc_all"
'''
#scenario = "mc_all"
if len(args) > 0: scenario = args[0]
print "Will run scenario ", scenario 
sample = "LO"
#sample = "NLO"
#sample = "25ns"
#sample = "50nsC"
#sample = "50nsB"
if len(args) > 1: 
    sample = args[1]
print 'sample is', sample 
id_bins = '1'
if len(args) > 2: 
    id_bins = args[2]
print 'id_bins is', id_bins
'''


process = cms.Process("TagProbe")
process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

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
        Loose_noIPVar = cms.vstring("Loose_noIPVar", "PF==1", "PF"),
        Medium_noIPVar= cms.vstring("Medium_noIPVar", "Medium==1", "Medium"),
        Tight2012_zIPCutVar = cms.vstring("Tight2012_zIPCut", "Tight2012 == 1 && abs(dzPV) < 0.5", "Tight2012", "dzPV"),
    ),

    Cuts = cms.PSet(
        #IP
        Loose_noIP = cms.vstring("Loose_noIP", "Loose_noIPVar", "0.5"),
        Medium_noIP= cms.vstring("Medium_noIP", "Medium_noIPVar", "0.5"),
        Tight2012_zIPCut = cms.vstring("Tight2012_zIPCut", "Tight2012_zIPCutVar", "0.5"),
        #Isolations
        LooseIso4 = cms.vstring("LooseIso4" ,"combRelIsoPF04dBeta", "0.25"),
        TightIso4 = cms.vstring("TightIso4" ,"combRelIsoPF04dBeta", "0.15"),
    ),

                          
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
#Denominators and Binning
#_*_*_*_*_*_*_*_*_*_*_*_*
#For ID
ETA_BINS = cms.PSet(
    pt  = cms.vdouble(20, 500),
    eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
VTX_BINS_ETA24  = cms.PSet(
    pt     = cms.vdouble( 20, 500 ),
    abseta = cms.vdouble(  0.0, 2.4),
    tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
PT_ALLETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 50, 60, 80),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
PT_ALLETA_BINS2 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 55, 80),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
PT_ETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 50, 60, 80),
    abseta = cms.vdouble(  0.0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
    
)
PT_ETA_BINS2 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 55, 80),
    abseta = cms.vdouble(  0.0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)

#For IP on ID
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
LOOSE_VTX_BINS_ETA24  = cms.PSet(
    pt     = cms.vdouble( 20, 500 ),
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
    pt     = cms.vdouble(20, 30, 40, 50, 60, 80),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
LOOSE_PT_ALLETA_BINS2 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 55, 80),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
LOOSE_PT_ETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 50, 60, 80),
    abseta = cms.vdouble(  0.0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
    
)
LOOSE_PT_ETA_BINS2 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 55, 80),
    abseta = cms.vdouble(  0.0, 1.2, 2.4),
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
MEDIUM_VTX_BINS_ETA24  = cms.PSet(
    pt     = cms.vdouble( 20, 500 ),
    abseta = cms.vdouble(  0.0, 2.4),
    tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_PT_ALLETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 50, 60, 80),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_PT_ALLETA_BINS2 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 55, 80),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_PT_ETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 50, 60, 80),
    abseta = cms.vdouble(  0.0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
    
)
MEDIUM_PT_ETA_BINS2 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 55, 80),
    abseta = cms.vdouble(  0.0, 1.2, 2.4),
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
TIGHT_VTX_BINS_ETA24  = cms.PSet(
    pt     = cms.vdouble( 20, 500 ),
    abseta = cms.vdouble(  0.0, 2.4),
    tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Tight2012 = cms.vstring("pass"), 
    dzPV = cms.vdouble(-0.5, 0.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
TIGHT_PT_ALLETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 50, 60, 80),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Tight2012 = cms.vstring("pass"), 
    dzPV = cms.vdouble(-0.5, 0.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
TIGHT_PT_ALLETA_BINS2 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 55, 80),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Tight2012 = cms.vstring("pass"), 
    dzPV = cms.vdouble(-0.5, 0.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
TIGHT_PT_ETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 50, 60, 80),
    abseta = cms.vdouble(  0.0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Tight2012 = cms.vstring("pass"), 
    dzPV = cms.vdouble(-0.5, 0.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
    
)
TIGHT_PT_ETA_BINS2 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 55, 80),
    abseta = cms.vdouble(  0.0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Tight2012 = cms.vstring("pass"), 
    dzPV = cms.vdouble(-0.5, 0.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)

if scenario == 'data_all':
    if bs == '25ns':
        if run == '2015C':
            process.TnP_MuonID = Template.clone(
                InputFileNames = cms.vstring(
                    'root://eoscms//eos/cms/store/group/phys_muon/TagAndProbe/TnP_trees_aod747_25ns_goldenJSON_246908-255031_withFixes.root',
                    ),
                InputTreeName = cms.string("fitter_tree"),
                InputDirectoryName = cms.string("tpTree"),
                OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
                Efficiencies = cms.PSet(),
                )
        
    elif bs == '50ns':
        if run == '2015B':
            process.TnP_MuonID = Template.clone(
                InputFileNames = cms.vstring(
                    'root://eoscms//eos/cms/store/group/phys_muon/TagAndProbe/TnP_trees_aod747_goldenJSON_246908-251883_HLT_IsoMu20.root',
                    ),
                InputTreeName = cms.string("fitter_tree"),
                InputDirectoryName = cms.string("tpTree"),
                OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
                Efficiencies = cms.PSet(),
                )
        elif run == '2015C':
            process.TnP_MuonID = Template.clone(
                InputFileNames = cms.vstring(
                    'root://eoscms//eos/cms/store/group/phys_muon/TagAndProbe/TnP_trees_aod747_50ns_goldenJSON_254833.root',
                    ),
                InputTreeName = cms.string("fitter_tree"),
                InputDirectoryName = cms.string("tpTree"),
                OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
                Efficiencies = cms.PSet(),
                )
elif scenario == 'mc_all':
    if bs == '50ns':
        if run == '2015B':
                if order== 'LO':
                    process.TnP_MuonID = Template.clone(
                    InputFileNames = cms.vstring(
                        'root://eoscms//eos/cms/store/group/phys_muon/perrin/v3/SmallTree_TnP_trees_aod747_DY_LOmadgraph_50ns_withFixes_withNVtxWeights_2015B.root'
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
                    'root://eoscms//eos/cms/store/group/phys_muon/perrin/v3/SmallTree_TnP_trees_aod747_DY_amcatnlo_50ns_withFixes_withNVtxWeights_WithWeights_2015B.root'
                        ),
                    InputTreeName = cms.string("fitter_tree"),
                    InputDirectoryName = cms.string("tpTree"),
                    OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
                    Efficiencies = cms.PSet(),
                    )
                    process.TnP_MuonID.WeightVariable = cms.string("weight")
                    process.TnP_MuonID.Variables.weight = cms.vstring("weight","0","10","")
        elif run == '2015C':
                if order== 'LO':
                    process.TnP_MuonID = Template.clone(
                    InputFileNames = cms.vstring(
                        'root://eoscms//eos/cms/store/group/phys_muon/perrin/v3/SmallTree_TnP_trees_aod747_DY_LOmadgraph_50ns_withFixes_withNVtxWeights_2015C.root'
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
                    'root://eoscms//eos/cms/store/group/phys_muon/perrin/v3/SmallTree_TnP_trees_aod747_DY_amcatnlo_50ns_withFixes_withNVtxWeights_WithWeights_2015C.root'
                        ),
                    InputTreeName = cms.string("fitter_tree"),
                    InputDirectoryName = cms.string("tpTree"),
                    OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
                    Efficiencies = cms.PSet(),
                    )
                    process.TnP_MuonID.WeightVariable = cms.string("weight")
                    process.TnP_MuonID.Variables.weight = cms.vstring("weight","0","10","")

ID_BINS = []

#_*_*_*_*_*_*_*_*_*_*
#IDs
#_*_*_*_*_*_*_*_*_*_*
#Loose ID
if id_bins == '1':
    ID_BINS = [
    (("Loose_noIP"), ("eta", ETA_BINS)),
    (("Loose_noIP"), ("vtx_bin1_24", VTX_BINS_ETA24 )),
    (("Loose_noIP"), ("pt_alleta_bin1", PT_ALLETA_BINS1)),
    (("Loose_noIP"), ("pt_alleta_bin2", PT_ALLETA_BINS2)),
    (("Loose_noIP"), ("pt_spliteta_bin1", PT_ETA_BINS1)),
    (("Loose_noIP"), ("pt_spliteta_bin2", PT_ETA_BINS2))
    ]
#Medium ID
if id_bins == '2':
    ID_BINS = [
    (("Medium_noIP"), ("eta", ETA_BINS)),
    (("Medium_noIP"), ("vtx_bin1_24", VTX_BINS_ETA24 )),
    (("Medium_noIP"), ("pt_alleta_bin1", PT_ALLETA_BINS1)),
    (("Medium_noIP"), ("pt_alleta_bin2", PT_ALLETA_BINS2)),
    (("Medium_noIP"), ("pt_spliteta_bin1", PT_ETA_BINS1)),
    (("Medium_noIP"), ("pt_spliteta_bin2", PT_ETA_BINS2))
    ]
#Tight ID
if id_bins == '3':
    ID_BINS = [
    (("Tight2012_zIPCut"), ("eta", ETA_BINS)),
    (("Tight2012_zIPCut"), ("vtx_bin1_24", VTX_BINS_ETA24 )),
    (("Tight2012_zIPCut"), ("pt_alleta_bin1", PT_ALLETA_BINS1)),
    (("Tight2012_zIPCut"), ("pt_alleta_bin2", PT_ALLETA_BINS2)),
    (("Tight2012_zIPCut"), ("pt_spliteta_bin1", PT_ETA_BINS1)),
    (("Tight2012_zIPCut"), ("pt_spliteta_bin2", PT_ETA_BINS2))
    ]
#_*_*_*_*_*_*_*_*_*_*
#ISOs
#_*_*_*_*_*_*_*_*_*_*
#Loose Iso
if id_bins == '4':
    ID_BINS = [
    (("LooseIso4"), ("loose_eta", LOOSE_ETA_BINS)),
    (("LooseIso4"), ("loose_vtx_bin1_24", LOOSE_VTX_BINS_ETA24 )),
    (("LooseIso4"), ("loose_pt_alleta_bin1", LOOSE_PT_ALLETA_BINS1)),
    (("LooseIso4"), ("loose_pt_alleta_bin2", LOOSE_PT_ALLETA_BINS2)),
    (("LooseIso4"), ("loose_pt_spliteta_bin1", LOOSE_PT_ETA_BINS1)),
    (("LooseIso4"), ("loose_pt_spliteta_bin2", LOOSE_PT_ETA_BINS2))
    ]
if id_bins == '5':
    ID_BINS = [
    (("LooseIso4"), ("medium_eta", MEDIUM_ETA_BINS)),
    (("LooseIso4"), ("medium_vtx_bin1_24", MEDIUM_VTX_BINS_ETA24 )),
    (("LooseIso4"), ("medium_pt_alleta_bin1", MEDIUM_PT_ALLETA_BINS1)),
    (("LooseIso4"), ("medium_pt_alleta_bin2", MEDIUM_PT_ALLETA_BINS2)),
    (("LooseIso4"), ("medium_pt_spliteta_bin1", MEDIUM_PT_ETA_BINS1)),
    (("LooseIso4"), ("medium_pt_spliteta_bin2", MEDIUM_PT_ETA_BINS2))
    ]
if id_bins == '6':
    ID_BINS = [
    (("LooseIso4"), ("tightip_eta", TIGHT_ETA_BINS)),
    (("LooseIso4"), ("tightip_vtx_bin1_24", TIGHT_VTX_BINS_ETA24 )),
    (("LooseIso4"), ("tightip_pt_alleta_bin1", TIGHT_PT_ALLETA_BINS1)),
    (("LooseIso4"), ("tightip_pt_alleta_bin2", TIGHT_PT_ALLETA_BINS2)),
    (("LooseIso4"), ("tightip_pt_spliteta_bin1", TIGHT_PT_ETA_BINS1)),
    (("LooseIso4"), ("tightip_pt_spliteta_bin2", TIGHT_PT_ETA_BINS2))
    ]
#Tight Iso
if id_bins == '7':
    ID_BINS = [
    (("TightIso4"), ("tightip_eta", TIGHT_ETA_BINS)),
    (("TightIso4"), ("tightip_vtx_bin1_24", TIGHT_VTX_BINS_ETA24 )),
    (("TightIso4"), ("tightip_pt_alleta_bin1", TIGHT_PT_ALLETA_BINS1)),
    (("TightIso4"), ("tightip_pt_alleta_bin2", TIGHT_PT_ALLETA_BINS2)),
    (("TightIso4"), ("tightip_pt_spliteta_bin1", TIGHT_PT_ETA_BINS1)),
    (("TightIso4"), ("tightip_pt_spliteta_bin2", TIGHT_PT_ETA_BINS2))
    ]

for ID, ALLBINS in ID_BINS:
    X = ALLBINS[0]
    B = ALLBINS[1]
    _output = os.getcwd() + '/Efficiency2'
    if not os.path.exists(_output):
        print 'Creating Efficiency directory where the fits are stored'  
        os.makedirs(_output)
    if scenario == 'data_all':
        _output += '/DATA' + bs + run + 'eff'
    elif scenario == 'mc_all':
        _output += '/MC' + bs + run + order
    if not os.path.exists(_output):
        os.makedirs(_output)
    module = process.TnP_MuonID.clone(OutputFileName = cms.string(_output + "/TnP_MuonID_%s_%s.root" % (ID, X)))
    shape = "vpvPlusExpo"
    DEN = B.clone(); num = ID;

    #compute isolation efficiency 
    if scenario == 'data_all':
        if num.find("Iso4") != -1: 
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num,"below"),
                UnbinnedVariables = cms.vstring("mass"),
                BinnedVariables = DEN,
                BinToPDFmap = cms.vstring(shape)
                ))
        else:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num,"above"),
                UnbinnedVariables = cms.vstring("mass"),
                BinnedVariables = DEN,
                BinToPDFmap = cms.vstring(shape)
                ))
        setattr(process, "TnP_MuonID_"+ID+"_"+X, module)        
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))
    elif scenario == 'mc_all':
        if num.find("Iso4") != -1: 
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num,"below"),
                UnbinnedVariables = cms.vstring("mass","weight"),
                BinnedVariables = DEN,
                BinToPDFmap = cms.vstring(shape)
                ))
        else:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num,"above"),
                UnbinnedVariables = cms.vstring("mass","weight"),
                BinnedVariables = DEN,
                BinToPDFmap = cms.vstring(shape)
                ))
        setattr(process, "TnP_MuonID_"+ID+"_"+X, module)        
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))

