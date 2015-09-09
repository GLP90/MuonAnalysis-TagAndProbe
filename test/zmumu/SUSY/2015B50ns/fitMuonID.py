import FWCore.ParameterSet.Config as cms
### USAGE:
###    cmsRun fitMuonID.py <scenario> [ <id> [ <binning1> ... <binningN> ] ]
###
### scenarios:
###   - data_all (default)  
###   - signal_mc

import sys, os
args = sys.argv[1:]
if (sys.argv[0] == "cmsRun"): args =sys.argv[2:]
scenario = "data_all"
#scenario = "mc_all"
if len(args) > 0: scenario = args[0]
print "Will run scenario ", scenario 
mc_sample = "LO"
#mc_sample = "NLO"
if len(args) > 1: 
    mc_sample = args[1]
    print 'The MC sample is', mc_sample 
id_bins = '1'
if len(args) > 2: 
    id_bins = args[2]
    print 'id_bins is', id_bins


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
        Medium   = cms.vstring("Medium Id. Muon", "dummy[pass=1,fail=0]"),
        PF    = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
        tag_IsoMu24_eta2p1 = cms.vstring("tag trigger", "dummy[pass=1,fail=0]")
    ),

    Expressions = cms.PSet(
        #IP Cuts
        LooseIP2DVar = cms.vstring("LooseIP2DVar", "abs(dxyBS)<0.2 && abs(dzPV)<0.5", "dxyBS", "dzPV"),
        TightIP2DVar = cms.vstring("TightIP2DVar", "abs(dxyBS)<0.05 && abs(dzPV)<0.1", "dxyBS", "dzPV"),
        TightIP3DVar = cms.vstring("TightIP3DVar", "abs(SIP)<4" , "SIP"),
    ),

    Cuts = cms.PSet(
        #IP Cuts
        LooseIP2D = cms.vstring("LooseIP2D", "LooseIP2DVar", "0.5"),
        TightIP2D = cms.vstring("TightIP2D", "TightIP2DVar", "0.5"),
        TightIP3D = cms.vstring("TightIP3D", "TightIP3DVar", "0.5"),
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
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu24_eta2p1 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
VTX_BINS_ETA24  = cms.PSet(
    pt     = cms.vdouble( 20, 500 ),
    abseta = cms.vdouble(  0.0, 2.4),
    tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu24_eta2p1 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
PT_ALLETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 50, 60, 80),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu24_eta2p1 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
PT_ALLETA_BINS2 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 55, 80),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu24_eta2p1 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
PT_ETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 50, 60, 80),
    abseta = cms.vdouble(  0.0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu24_eta2p1 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
    
)
PT_ETA_BINS2 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 55, 80),
    abseta = cms.vdouble(  0.0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu24_eta2p1 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)

#For IP on ID
LOOSE_ETA_BINS = cms.PSet(
    pt  = cms.vdouble(20, 500),
    eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu24_eta2p1 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
LOOSE_VTX_BINS_ETA24  = cms.PSet(
    pt     = cms.vdouble( 20, 500 ),
    abseta = cms.vdouble(  0.0, 2.4),
    tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu24_eta2p1 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
LOOSE_PT_ALLETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 50, 60, 80),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu24_eta2p1 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
LOOSE_PT_ALLETA_BINS2 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 55, 80),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu24_eta2p1 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
LOOSE_PT_ETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 50, 60, 80),
    abseta = cms.vdouble(  0.0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu24_eta2p1 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
    
)
LOOSE_PT_ETA_BINS2 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 55, 80),
    abseta = cms.vdouble(  0.0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    PF = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu24_eta2p1 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_ETA_BINS = cms.PSet(
    pt  = cms.vdouble(20, 500),
    eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu24_eta2p1 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_VTX_BINS_ETA24  = cms.PSet(
    pt     = cms.vdouble( 20, 500 ),
    abseta = cms.vdouble(  0.0, 2.4),
    tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu24_eta2p1 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_PT_ALLETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 50, 60, 80),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu24_eta2p1 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_PT_ALLETA_BINS2 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 55, 80),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu24_eta2p1 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
MEDIUM_PT_ETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 50, 60, 80),
    abseta = cms.vdouble(  0.0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu24_eta2p1 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
    
)
MEDIUM_PT_ETA_BINS2 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 55, 80),
    abseta = cms.vdouble(  0.0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    Medium = cms.vstring("pass"), 
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu24_eta2p1 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)

if scenario == 'data_all':
    process.TnP_MuonID = Template.clone(
        InputFileNames = cms.vstring(
            'root://eoscms//eos/cms/store/group/phys_muon/TagAndProbe/TnP_trees_aod747_goldenJSON.root',
            ),
        InputTreeName = cms.string("fitter_tree"),
        InputDirectoryName = cms.string("tpTree"),
        OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
        Efficiencies = cms.PSet(),
        )
elif scenario == 'mc_all':
    if mc_sample == 'LO':
        process.TnP_MuonID = Template.clone(
            InputFileNames = cms.vstring(
                'root://eoscms//eos/cms/store/group/phys_muon/perrin/SF50ns/TnP_trees/SmallTree_TnP_trees_aod747_DY_LOmadgraph_withNVtxWeights.root',
                ),
            InputTreeName = cms.string("fitter_tree"),
            InputDirectoryName = cms.string("tpTree"),
            OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
            Efficiencies = cms.PSet(),
            )
    elif mc_sample == 'NLO':
        process.TnP_MuonID = Template.clone(
            InputFileNames = cms.vstring(
                'root://eoscms//eos/cms/store/group/phys_muon/perrin/SF50ns/TnP_trees/SmallTnP_trees_aod747_DY_withNVtxWeights.root',
                ),
            InputTreeName = cms.string("fitter_tree"),
            InputDirectoryName = cms.string("tpTree"),
            OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
            Efficiencies = cms.PSet(),
            )
    process.TnP_MuonID.WeightVariable = cms.string("weight")
    process.TnP_MuonID.Variables.weight = cms.vstring("weight","0","10","")

ID_BINS = []

#Loose ID
if id_bins == '1':
    ID_BINS = [
    (("PF"), ("eta", ETA_BINS)),
    (("PF"), ("vtx_bin1_24", VTX_BINS_ETA24 )),
    (("PF"), ("pt_alleta_bin1", PT_ALLETA_BINS1)),
    (("PF"), ("pt_alleta_bin2", PT_ALLETA_BINS2)),
    (("PF"), ("pt_spliteta_bin1", PT_ETA_BINS1)),
    (("PF"), ("pt_spliteta_bin2", PT_ETA_BINS2))
    ]
#Medium ID
if id_bins == '2':
    ID_BINS = [
    (("Medium"), ("eta", ETA_BINS)),
    (("Medium"), ("vtx_bin1_24", VTX_BINS_ETA24 )),
    (("Medium"), ("pt_alleta_bin1", PT_ALLETA_BINS1)),
    (("Medium"), ("pt_alleta_bin2", PT_ALLETA_BINS2)),
    (("Medium"), ("pt_spliteta_bin1", PT_ETA_BINS1)),
    (("Medium"), ("pt_spliteta_bin2", PT_ETA_BINS2))
    ]
#Loose IP 2D
if id_bins == '3':
    ID_BINS = [
    (("LooseIP2D"), ("loose_eta", LOOSE_ETA_BINS)),
    (("LooseIP2D"), ("loose_vtx_bin1_24", LOOSE_VTX_BINS_ETA24 )),
    (("LooseIP2D"), ("loose_pt_alleta_bin1", LOOSE_PT_ALLETA_BINS1)),
    (("LooseIP2D"), ("loose_pt_alleta_bin2", LOOSE_PT_ALLETA_BINS2)),
    (("LooseIP2D"), ("loose_pt_spliteta_bin1", LOOSE_PT_ETA_BINS1)),
    (("LooseIP2D"), ("loose_pt_spliteta_bin2", LOOSE_PT_ETA_BINS2))
    ]
if id_bins == '4':
    ID_BINS = [
    (("LooseIP2D"), ("medium_eta", MEDIUM_ETA_BINS)),
    (("LooseIP2D"), ("medium_vtx_bin1_24", MEDIUM_VTX_BINS_ETA24 )),
    (("LooseIP2D"), ("medium_pt_alleta_bin1", MEDIUM_PT_ALLETA_BINS1)),
    (("LooseIP2D"), ("medium_pt_alleta_bin2", MEDIUM_PT_ALLETA_BINS2)),
    (("LooseIP2D"), ("medium_pt_spliteta_bin1", MEDIUM_PT_ETA_BINS1)),
    (("LooseIP2D"), ("medium_pt_spliteta_bin2", MEDIUM_PT_ETA_BINS2))
    ]
#Tight IP 2D
if id_bins == '5':
    ID_BINS = [
    (("TightIP2D"), ("medium_eta", MEDIUM_ETA_BINS)),
    (("TightIP2D"), ("medium_vtx_bin1_24", MEDIUM_VTX_BINS_ETA24 )),
    (("TightIP2D"), ("medium_pt_alleta_bin1", MEDIUM_PT_ALLETA_BINS1)),
    (("TightIP2D"), ("medium_pt_alleta_bin2", MEDIUM_PT_ALLETA_BINS2)),
    (("TightIP2D"), ("medium_pt_spliteta_bin1", MEDIUM_PT_ETA_BINS1)),
    (("TightIP2D"), ("medium_pt_spliteta_bin2", MEDIUM_PT_ETA_BINS2))
    ]
#Tight IP 3D
if id_bins == '6':
    ID_BINS = [
    (("TightIP3D"), ("medium_eta", MEDIUM_ETA_BINS)),
    (("TightIP3D"), ("medium_vtx_bin1_24", MEDIUM_VTX_BINS_ETA24 )),
    (("TightIP3D"), ("medium_pt_alleta_bin1", MEDIUM_PT_ALLETA_BINS1)),
    (("TightIP3D"), ("medium_pt_alleta_bin2", MEDIUM_PT_ALLETA_BINS2)),
    (("TightIP3D"), ("medium_pt_spliteta_bin1", MEDIUM_PT_ETA_BINS1)),
    (("TightIP3D"), ("medium_pt_spliteta_bin2", MEDIUM_PT_ETA_BINS2))
    ]

for ID, ALLBINS in ID_BINS:
    X = ALLBINS[0]
    B = ALLBINS[1]
    _output = os.getcwd() + '/Efficiency1'
    if not os.path.exists(_output):
        print 'Creating Efficiency directory where the fits are stored'  
        os.makedirs(_output)
    if scenario == 'data_all':
        _output += '/DATAeff'
    elif scenario == 'mc_all':
        if mc_sample == 'LO': 
             _output += '/MCLOeff'
        elif mc_sample == 'NLO': 
             _output += '/MCNLOeff'
    if not os.path.exists(_output):
        os.makedirs(_output)
    module = process.TnP_MuonID.clone(OutputFileName = cms.string(_output + "/TnP_MuonID_%s_%s.root" % (ID, X)))
    shape = "vpvPlusExpo"
    DEN = B.clone(); num = ID;

    #compute isolation efficiency 
    if scenario == 'data_all':
        if num.find("Medium") != -1 or num.find("PF") != -1:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num,"pass"),
                UnbinnedVariables = cms.vstring("mass"),
                BinnedVariables = DEN,
                BinToPDFmap = cms.vstring(shape)
                ))
        elif num.find("IP") != -1:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num,"above"),
                UnbinnedVariables = cms.vstring("mass"),
                BinnedVariables = DEN,
                BinToPDFmap = cms.vstring(shape)
                ))
        setattr(process, "TnP_MuonID_"+ID+"_"+X, module)        
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))
    elif scenario == 'mc_all':
        if num.find("Medium") != -1 or num.find("PF") != -1:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num,"pass"),
                UnbinnedVariables = cms.vstring("mass","weight"),
                BinnedVariables = DEN,
                BinToPDFmap = cms.vstring(shape)
                ))
        elif num.find("IP") != -1:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num,"above"),
                UnbinnedVariables = cms.vstring("mass","weight"),
                BinnedVariables = DEN,
                BinToPDFmap = cms.vstring(shape)
                ))
        setattr(process, "TnP_MuonID_"+ID+"_"+X, module)        
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))

