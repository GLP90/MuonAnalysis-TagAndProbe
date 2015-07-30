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
if len(args) > 0: scenario = args[0]
print "Will run scenario ", scenario 

process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')

process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

Template = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    NumCPU = cms.uint32(1),
    SaveWorkspace = cms.bool(False),

    Variables = cms.PSet(
        mass = cms.vstring("Tag-muon Mass", "70", "130", "GeV/c^{2}"),
        pt = cms.vstring("muon p_{T}", "0", "1000", "GeV/c"),
        eta    = cms.vstring("muon #eta", "-2.5", "2.5", ""),
        abseta = cms.vstring("muon |#eta|", "0", "2.5", ""),
        phi    = cms.vstring("muon #phi at vertex", "-3.1416", "3.1416", ""),
        charge = cms.vstring("muon charge", "-2.5", "2.5", ""),
        combRelIsoPF04dBeta = cms.vstring("dBeta rel iso dR 0.4", "-2", "9999999", ""),
        tag_pt = cms.vstring("Tag p_{T}", "0", "1000", "GeV/c"),
        tag_nVertices   = cms.vstring("Number of vertices", "0", "999", ""),
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
        #Variables for Tight2012
        GlbPT  = cms.vstring("Global Muon Prompt Tight')", "dummy[pass=1,fail=0]"),


    ),

    Expressions = cms.PSet(
        #LooseVar = cms.vstring("LooseVar", "PF==1 && (Glb==1 || TM==1) ", "PF", "Glb", "TM"),
        Loose_noIPVar = cms.vstring("LooseVar", "PF==1 && (Glb==1 || TM==1) ", "PF", "Glb", "TM"),
        Medium_noIPVar= cms.vstring("Medium_noIPVar", "Medium==1", "Medium"),
        Tight_noIPVar = cms.vstring("Tight_noIPVar", "PF==1 && numberOfMatchedStations>1 && GlbPT==1 && tkTrackerLay>5 && tkValidPixelHits>0", "PF", "numberOfMatchedStations", "GlbPT", "tkTrackerLay", "tkValidPixelHits"),
    ),

    Cuts = cms.PSet(
        #Loose = cms.vstring("Loose", "LooseVar", "0.5"),
        #noIP ids
        Loose_noIP = cms.vstring("Loose_noIP", "Loose_noIPVar", "0.5"),
        Medium_noIP = cms.vstring("Medium_noIP", "Medium_noIPVar", "0.5"),
        Tight_noIP = cms.vstring("Tightid_noIP", "Tight_noIPVar", "0.5"),
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

PT_ETA_BINS = cms.PSet(
    #pt     = cms.vdouble(  10, 20, 25, 30, 35, 40, 50, 60, 90, 140, 300, 500 ),
    pt     = cms.vdouble(20,50,500 ),
    #abseta = cms.vdouble(  0.0, 0.9, 1.2, 2.1, 2.4),
    abseta = cms.vdouble(  0.0, 0.9),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
)
ETA_BINS = cms.PSet(
    pt  = cms.vdouble(20,500),
    eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.6, -0.3, -0.2, 0.2, 0.3, 0.6, 0.9, 1.2, 1.6, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
)
VTX_BINS  = cms.PSet(
    pt     = cms.vdouble(  20, 500 ),
    abseta = cms.vdouble(  0.0, 2.1),
    tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
)

OVERALL_ABSETA = cms.PSet(
    pt  = cms.vdouble(20,500),
    #abseta = cms.vdouble(0.0, 0.9, 1.2, 2.1, 2.4),
    abseta = cms.vdouble(1.2, 2.1),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
)

process.TnP_MuonID = Template.clone(
    InputFileNames = cms.vstring(
        'root://eoscms//eos/cms/store/group/phys_muon/TagAndProbe/TnP_trees_aod747_goldenJSON.root',
                                 ),
    InputTreeName = cms.string("fitter_tree"),
    InputDirectoryName = cms.string("tpTree"),
    OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
    Efficiencies = cms.PSet(),
)

#IDS = ["Tightid_noIP"]#Has to be the same as the name of the Cut
IDS = [ "Loose_noIP", "Medium_noIP", "Tight_noIP"]#Has to be the same as the name of the Cut
#ALLBINS = [("pt_abseta",PT_ETA_BINS)]
#ALLBINS= [("eta", ETA_BINS), ("pt", PT_ETA_BINS), ("vtx",VTX_BINS)]
ALLBINS= [("eta", ETA_BINS)]
#ALLBINS= [("vtx",VTX_BINS)]
#ALLBINS= [("overall_abseta",OVERALL_ABSETA)]

if len(args) > 1 and args[1] not in IDS: IDS += [ args[1] ]
for ID in IDS:
    if len(args) > 1 and ID != args[1]: continue
    for X,B in ALLBINS:
        if len(args) > 2 and X not in args[2:]: continue
        module = process.TnP_MuonID.clone(OutputFileName = cms.string("TnP_MuonID_%s_%s_%s.root" % (scenario, ID, X)))
        shape = "vpvPlusExpo"
        #change the shape and the range as a function of the selection and the variable
        if "eta" in X and not "abseta" in X: shape = "voigtPlusExpo"
        if "pt_abseta" in X: shape = "voigtPlusExpo"
        if X.find("pt_abseta") != -1: module.Variables.mass[1]="77";#change the invariant mass range
        if X.find("overall") != -1: module.binsForFit = 120 #change the bins for fit
        DEN = B.clone(); num = ID;
        if "24" in ID and hasattr(DEN,'pt') and "pt" not in X: DEN.pt[0] = 25 #change pt range
        #Implement reliso
        if "_from_" in ID:
            parts = ID.split("_from_")
            num = parts[0]
            den = parts[1]
            if den.find("Medium") != -1: 
                setattr(DEN, parts[1], cms.vstring("pass"))
            else:
                setattr(DEN, parts[1], cms.vstring("above"))

        #compute isolation efficiency
        if num.find("Iso4") != -1: 
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num,"below"),
                UnbinnedVariables = cms.vstring("mass"),
                BinnedVariables = DEN,
                BinToPDFmap = cms.vstring(shape)
            ))
        #Compute isolation for id
        else:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num,"above"),
                UnbinnedVariables = cms.vstring("mass"),
                BinnedVariables = DEN,
                BinToPDFmap = cms.vstring(shape)
            ))
        setattr(process, "TnP_MuonID_"+ID+"_"+X, module)        
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))

