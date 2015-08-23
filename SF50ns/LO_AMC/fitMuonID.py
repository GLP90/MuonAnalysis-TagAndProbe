import FWCore.ParameterSet.Config as cms
### USAGE:
###    cmsRun fitMuonID.py <scenario> [ <id> [ <binning1> ... <binningN> ] ]
###
### scenarios:
###   - data_all (default)  
###   - signal_mc

import sys
args = sys.argv[1:]
if (sys.argv[0] == "cmsRun"): args =sys.argv[2:]
scenario = "data_all"
#scenario = "mc_all"
if len(args) > 0: scenario = args[0]
print "Will run scenario ", scenario 
if len(args) > 1: 
    numerator = args[1]
    print 'The numerator is ', numerator


process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')

process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )


Template = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
        NumCPU = cms.uint32(1),
    SaveWorkspace = cms.bool(False),

    Variables = cms.PSet(
        #Added MC weight
        weight = cms.vstring("weight","0","10",""),
        #
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
        pair_probeMultiplicity = cms.vstring("pair_probeMultiplicity", "0","30",""),
        #Variables for Tight2012
        numberOfMatchedStations = cms.vstring("matched stations","-1", "50",""),
        tkTrackerLay = cms.vstring("track.hitPattern.trackerLayersWithMeasurement","-1", "50",""),
        tkValidPixelHits = cms.vstring("track.hitPattern.numberOfValidPixelHits","-1", "50",""),

        ),

    Categories = cms.PSet(
        Glb   = cms.vstring("Global", "dummy[pass=1,fail=0]"),
        PF    = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
        TM    = cms.vstring("Tracker Muon", "dummy[pass=1,fail=0]"),
        Medium   = cms.vstring("Medium Id. Muon", "dummy[pass=1,fail=0]"),
        Tight2012 = cms.vstring("Tight Id. Muon", "dummy[pass=1,fail=0]"),
        #Variables for Tight2012
        GlbPT  = cms.vstring("Global Muon Prompt Tight')", "dummy[pass=1,fail=0]"),
        tag_IsoMu20 = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),


    ),

    Expressions = cms.PSet(
        #IP Cuts
        IPLooseVar = cms.vstring("IPLooseVar", "abs(dxyBS)<0.2 && abs(dzPV)<0.5", "dxyBS", "dzPV"),
        IPTightVar = cms.vstring("IPTightVar", "abs(dxyBS)<0.02 && abs(dzPV)<0.1", "dxyBS", "dzPV"),
        #ID Cuts
        Loose_noIPVar = cms.vstring("LooseVar", "PF==1 && (Glb==1 || TM==1) ", "PF", "Glb", "TM"),
        Medium_noIPVar= cms.vstring("Medium_noIPVar", "Medium==1", "Medium"),
        Tight_noIPVar = cms.vstring("Tight_noIPVar", "PF==1 && numberOfMatchedStations>1 && GlbPT==1 && tkTrackerLay>5 && tkValidPixelHits>0", "PF", "numberOfMatchedStations", "GlbPT", "tkTrackerLay", "tkValidPixelHits"),
        #IP+ID Cuts
        LooseVar = cms.vstring("LooseVar", "PF==1 && (Glb==1 || TM==1) && IPLooseVar==1", "PF", "Glb", "TM","IPLooseVar"),
        MediumVar= cms.vstring("MediumVar", "Medium==1 && IPLooseVar==1", "Medium", "IPLooseVar"),
        TightVar = cms.vstring("TightVar", "PF==1 && numberOfMatchedStations>1 && GlbPT==1 && tkTrackerLay>5 && tkValidPixelHits>0 && abs(dB) < 0.2 && abs(dzPV) < 0.5", "PF", "numberOfMatchedStations", "GlbPT", "tkTrackerLay", "tkValidPixelHits", "dB", "dzPV"),
        Tight_tightIPVar = cms.vstring("Tight_tightIPVar", "PF==1 && numberOfMatchedStations>1 && GlbPT==1 && tkTrackerLay>5 && tkValidPixelHits>0 && IPTightVar==1", "PF", "numberOfMatchedStations", "GlbPT", "tkTrackerLay", "tkValidPixelHits", "IPTightVar"),
    ),

    Cuts = cms.PSet(
        #noIP ids
        Loose_noIP = cms.vstring("Loose_noIP", "Loose_noIPVar", "0.5"),
        Medium_noIP = cms.vstring("Medium_noIP", "Medium_noIPVar", "0.5"),
        Tight_noIP = cms.vstring("Tightid_noIP", "Tight_noIPVar", "0.5"),
        #IP ID Cuts
        Loose_IP = cms.vstring("Loose_IP", "LooseVar", "0.5"),
        Medium_IP = cms.vstring("Medium_IP", "MediumVar", "0.5"),
        Tight_IP = cms.vstring("Tight_IP", "TightVar", "0.5"),
        Tight_tightIP = cms.vstring("Tight_tightIP", "Tight_tightIPVar", "0.5"),
        #Isolations
        LooseIso4 = cms.vstring("LooseIso4" ,"combRelIsoPF04dBeta", "0.2"),
        TightIso4 = cms.vstring("TightIso4" ,"combRelIsoPF04dBeta", "0.12"),
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

#changed the trigger here
#TRIGGER = cms.PSet(tag_Mu20 = cms.vstring("pass"))

    #_*_*_*_*_*_*_*_*_*_*_*_*
    #Denominators and Binning
    #_*_*_*_*_*_*_*_*_*_*_*_*

ETA_BINS = cms.PSet(
    pt  = cms.vdouble(22,500),
    eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu20 = cms.vstring("pass"),
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)


VTX_BINS1_ETA21  = cms.PSet(
    pt     = cms.vdouble(  22, 500 ),
    abseta = cms.vdouble(  0.0, 2.1),
    tag_nVertices = cms.vdouble(4.5, 9.5, 14.5, 19.5, 24.5),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu20 = cms.vstring("pass"),
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)

VTX_BINS1_ETA24  = cms.PSet(
    pt     = cms.vdouble(  22, 500 ),
    abseta = cms.vdouble(  0.0, 2.4),
    tag_nVertices = cms.vdouble(4.5, 9.5, 14.5, 19.5, 24.5),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu20 = cms.vstring("pass"),
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)

VTX_BINS2_ETA21  = cms.PSet(
    pt     = cms.vdouble(  22, 500 ),
    abseta = cms.vdouble(  0.0, 2.1),
    tag_nVertices = cms.vdouble(4.5, 8.5, 12.5, 16.5, 20.5, 24.5),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu20 = cms.vstring("pass"),
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)

VTX_BINS2_ETA24  = cms.PSet(
    pt     = cms.vdouble(  22, 500 ),
    abseta = cms.vdouble(  0.0, 2.4),
    tag_nVertices = cms.vdouble(4.5, 8.5, 12.5, 16.5, 20.5, 24.5),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu20 = cms.vstring("pass"),
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)

PT_ALLETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 50, 60, 80),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu20 = cms.vstring("pass"),
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)

PT_ALLETA_BINS2 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 55, 80),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu20 = cms.vstring("pass"),
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)

PT_ETA_BINS1 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 50, 60, 80),
    abseta = cms.vdouble(  0.0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu20 = cms.vstring("pass"),
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
    
)

PT_ETA_BINS2 = cms.PSet(
    pt     = cms.vdouble(20, 30, 40, 55, 80),
    abseta = cms.vdouble(  0.0, 1.2, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_IsoMu20 = cms.vstring("pass"),
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


IDS = ["Loose_noIP"]#Has to be the same as the name of the Cut
ALLBINS= [("vtx_bin1_21", VTX_BINS1_ETA21), ("vtx_bin1_24", VTX_BINS1_ETA24), ("vtx_bin2_21", VTX_BINS2_ETA21), ("vtx_bin2_24", VTX_BINS2_ETA24)]

for ID in IDS:
    for X,B in ALLBINS:
        if scenario == 'data_all': module = process.TnP_MuonID.clone(OutputFileName = cms.string("DATAeff_app2/TnP_MuonID_%s_%s.root" % (ID, X)))
        elif scenario == 'mc_all': module = process.TnP_MuonID.clone(OutputFileName = cms.string("MCeff_app2/TnP_MuonID_%s_%s.root" % (ID, X)))
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
                #Compute id efficiency
            elif num.find("Tight2012") != -1:
                setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                    EfficiencyCategoryAndState = cms.vstring(num,"pass"),
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
                    BinnedVariables = DEN,
                    BinToPDFmap = cms.vstring(shape)
                    ))
                #Compute id efficiency
            elif num.find("Tight2012") != -1:
                setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                    EfficiencyCategoryAndState = cms.vstring(num,"pass"),
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
    
