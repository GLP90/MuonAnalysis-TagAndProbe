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
        TightVar = cms.vstring("TightVar", "PF==1 && numberOfMatchedStations>1 && GlbPT==1 && tkTrackerLay>5 && tkValidPixelHits>0 && IPLooseVar==1", "PF", "numberOfMatchedStations", "GlbPT", "tkTrackerLay", "tkValidPixelHits", "IPLooseVar"),
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

PT_ETA_BINS = cms.PSet(
    #pt     = cms.vdouble(  10, 20, 25, 30, 35, 40, 50, 60, 90, 140, 300, 500 ),
    pt     = cms.vdouble(20, 30, 40, 50, 60, 70, 80, 90, 100),
    abseta = cms.vdouble(  0.0, 1.2, 2.4),
    #abseta = cms.vdouble(  0.0, 0.9),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_abseta = cms.vdouble(0, 2.1),
    tag_IsoMu20 = cms.vstring("pass"),
)
ETA_BINS = cms.PSet(
    pt  = cms.vdouble(20,500),
    #eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.6, -0.3, -0.2, 0.2, 0.3, 0.6, 0.9, 1.2, 1.6, 2.1, 2.4),
    eta = cms.vdouble(-2.4, -2.1, -1.8, -1.5, -1.2, -0.9, -0.6, -0.3, 0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_abseta = cms.vdouble(0, 2.1),
    tag_IsoMu20 = cms.vstring("pass"),
)
VTX_BINS  = cms.PSet(
    pt     = cms.vdouble(  20, 500 ),
    abseta = cms.vdouble(  0.0, 2.1),
    tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(25, 500),
    tag_abseta = cms.vdouble(0, 2.1),
    tag_IsoMu20 = cms.vstring("pass"),
)

OVERALL_ABSETA = cms.PSet(
        pt  = cms.vdouble(20,500),
        #abseta = cms.vdouble(0.0, 0.9, 1.2, 2.1, 2.4),
        abseta = cms.vdouble(1.2, 2.1),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),
        )

    #_*_*_*_*_*_*_*_*_*_*_*_*_*
    #Denominators for Rel. Iso
    #_*_*_*_*_*_*_*_*_*_*_*_*_*


LOOSE_noIP_PT_ETA_BINS = cms.PSet(
        PF = cms.vstring("pass"),

        pt     = cms.vdouble(20, 30, 40, 50, 60, 70, 80, 90, 100),
        abseta = cms.vdouble(  0.0, 1.2, 2.4),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),
        )

LOOSE_noIP_ETA_BINS= cms.PSet(
        PF = cms.vstring("pass"),

        pt  = cms.vdouble(20,500),
        eta = cms.vdouble(-2.4, -2.1, -1.8, -1.5, -1.2, -0.9, -0.6, -0.3, 0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),
        )

LOOSE_noIP_VTX_BINS = cms.PSet(
        PF = cms.vstring("pass"),

        pt     = cms.vdouble(  20, 500 ),
        abseta = cms.vdouble(  0.0, 2.1),
        tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),
        )


MEDIUM_noIP_PT_ETA_BINS = cms.PSet(
        Medium = cms.vstring("pass"),

        pt     = cms.vdouble(20, 30, 40, 50, 60, 70, 80, 90, 100),
        abseta = cms.vdouble(  0.0, 1.2, 2.4),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),
        )

MEDIUM_noIP_ETA_BINS = cms.PSet(
        Medium = cms.vstring("pass"),

        pt  = cms.vdouble(20,500),
        eta = cms.vdouble(-2.4, -2.1, -1.8, -1.5, -1.2, -0.9, -0.6, -0.3, 0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),
        )

MEDIUM_noIP_VTX_BINS = cms.PSet(
        Medium = cms.vstring("pass"),

        pt     = cms.vdouble(  20, 500 ),
        abseta = cms.vdouble(  0.0, 2.1),
        tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),
        )

TIGHT_noIP_PT_ETA_BINS = cms.PSet(
        PF = cms.vstring("pass"),
        numberOfMatchedStations = cms.vdouble(1, 99),
        GlbPT = cms.vstring("pass"),
        tkTrackerLay = cms.vdouble(5, 99),
        tkValidPixelHits = cms.vdouble(0, 99),

        pt     = cms.vdouble(20, 30, 40, 50, 60, 70, 80, 90, 100),
        abseta = cms.vdouble(  0.0, 1.2, 2.4),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),

        #dB = cms.vdouble(-0.2, 0.2),
        #dzPV = cms.vdouble(-0.5, 0.5),
        )

TIGHT_noIP_ETA_BINS = cms.PSet(
        PF = cms.vstring("pass"),
        numberOfMatchedStations = cms.vdouble(1, 99),
        GlbPT = cms.vstring("pass"),
        tkTrackerLay = cms.vdouble(5, 99),
        tkValidPixelHits = cms.vdouble(0, 99),

        pt  = cms.vdouble(20,500),
        eta = cms.vdouble(-2.4, -2.1, -1.8, -1.5, -1.2, -0.9, -0.6, -0.3, 0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),

        #dB = cms.vdouble(-0.2, 0.2),
        #dzPV = cms.vdouble(-0.5, 0.5),
        )

TIGHT_noIP_VTX_BINS = cms.PSet(
        PF = cms.vstring("pass"),
        numberOfMatchedStations = cms.vdouble(1, 99),
        GlbPT = cms.vstring("pass"),
        tkTrackerLay = cms.vdouble(5, 99),
        tkValidPixelHits = cms.vdouble(0, 99),

        pt     = cms.vdouble(  20, 500 ),
        abseta = cms.vdouble(  0.0, 2.1),
        tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),

        #dB = cms.vdouble(-0.2, 0.2),
        #dzPV = cms.vdouble(-0.5, 0.5),
        )

LOOSE_PT_ETA_BINS = cms.PSet(
        PF = cms.vstring("pass"),

        pt     = cms.vdouble(20, 30, 40, 50, 60, 70, 80, 90, 100),
        abseta = cms.vdouble(  0.0, 1.2, 2.4),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),

        dxyBS= cms.vdouble(-0.2, 0.2),
        dzPV = cms.vdouble(-0.5, 0.5),
        )

LOOSE_ETA_BINS= cms.PSet(
        PF = cms.vstring("pass"),

        pt  = cms.vdouble(20,500),
        eta = cms.vdouble(-2.4, -2.1, -1.8, -1.5, -1.2, -0.9, -0.6, -0.3, 0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),

        dxyBS= cms.vdouble(-0.2, 0.2),
        dzPV = cms.vdouble(-0.5, 0.5),
        )

LOOSE_VTX_BINS = cms.PSet(
        PF = cms.vstring("pass"),

        pt     = cms.vdouble(  20, 500 ),
        abseta = cms.vdouble(  0.0, 2.1),
        tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),

        dxyBS= cms.vdouble(-0.2, 0.2),
        dzPV = cms.vdouble(-0.5, 0.5),
        )


MEDIUM_PT_ETA_BINS = cms.PSet(
        Medium = cms.vstring("pass"),

        pt     = cms.vdouble(20, 30, 40, 50, 60, 70, 80, 90, 100),
        abseta = cms.vdouble(  0.0, 1.2, 2.4),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),

        dxyBS= cms.vdouble(-0.2, 0.2),
        dzPV = cms.vdouble(-0.5, 0.5),
        )

MEDIUM_ETA_BINS = cms.PSet(
        Medium = cms.vstring("pass"),

        pt  = cms.vdouble(20,500),
        eta = cms.vdouble(-2.4, -2.1, -1.8, -1.5, -1.2, -0.9, -0.6, -0.3, 0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),

        dxyBS= cms.vdouble(-0.2, 0.2),
        dzPV = cms.vdouble(-0.5, 0.5),
        )

MEDIUM_VTX_BINS = cms.PSet(
        Medium = cms.vstring("pass"),

        pt     = cms.vdouble(  20, 500 ),
        abseta = cms.vdouble(  0.0, 2.1),
        tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),

        dxyBS= cms.vdouble(-0.2, 0.2),
        dzPV = cms.vdouble(-0.5, 0.5),
        )

TIGHT_PT_ETA_BINS = cms.PSet(
        PF = cms.vstring("pass"),
        numberOfMatchedStations = cms.vdouble(1, 99),
        GlbPT = cms.vstring("pass"),
        tkTrackerLay = cms.vdouble(5, 99),
        tkValidPixelHits = cms.vdouble(0, 99),

        pt     = cms.vdouble(20, 30, 40, 50, 60, 70, 80, 90, 100),
        abseta = cms.vdouble(  0.0, 1.2, 2.4),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),

        dxyBS= cms.vdouble(-0.2, 0.2),
        dzPV = cms.vdouble(-0.5, 0.5),
        )

TIGHT_ETA_BINS = cms.PSet(
        PF = cms.vstring("pass"),
        numberOfMatchedStations = cms.vdouble(1, 99),
        GlbPT = cms.vstring("pass"),
        tkTrackerLay = cms.vdouble(5, 99),
        tkValidPixelHits = cms.vdouble(0, 99),

        pt  = cms.vdouble(20,500),
        eta = cms.vdouble(-2.4, -2.1, -1.8, -1.5, -1.2, -0.9, -0.6, -0.3, 0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),

        dxyBS= cms.vdouble(-0.2, 0.2),
        dzPV = cms.vdouble(-0.5, 0.5),
        )

TIGHT_VTX_BINS = cms.PSet(
        PF = cms.vstring("pass"),
        numberOfMatchedStations = cms.vdouble(1, 99),
        GlbPT = cms.vstring("pass"),
        tkTrackerLay = cms.vdouble(5, 99),
        tkValidPixelHits = cms.vdouble(0, 99),

        pt     = cms.vdouble(  20, 500 ),
        abseta = cms.vdouble(  0.0, 2.1),
        tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),

        dxyBS= cms.vdouble(-0.2, 0.2),
        dzPV = cms.vdouble(-0.5, 0.5),
        )

TIGHT_TIGHTIP_PT_ETA_BINS = cms.PSet(
        PF = cms.vstring("pass"),
        numberOfMatchedStations = cms.vdouble(1, 99),
        GlbPT = cms.vstring("pass"),
        tkTrackerLay = cms.vdouble(5, 99),
        tkValidPixelHits = cms.vdouble(0, 99),

        pt     = cms.vdouble(20, 30, 40, 50, 60, 70, 80, 90, 100),
        abseta = cms.vdouble(  0.0, 1.2, 2.4),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),

        dxyBS= cms.vdouble(-0.02, 0.02),
        dzPV = cms.vdouble(-0.1, 0.1),
        )

TIGHT_TIGHTIP_ETA_BINS = cms.PSet(
        PF = cms.vstring("pass"),
        numberOfMatchedStations = cms.vdouble(1, 99),
        GlbPT = cms.vstring("pass"),
        tkTrackerLay = cms.vdouble(5, 99),
        tkValidPixelHits = cms.vdouble(0, 99),

        pt  = cms.vdouble(20,500),
        eta = cms.vdouble(-2.4, -2.1, -1.8, -1.5, -1.2, -0.9, -0.6, -0.3, 0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),

        dxyBS= cms.vdouble(-0.02, 0.02),
        dzPV = cms.vdouble(-0.1, 0.1),
        )

TIGHT_TIGHTIP_VTX_BINS = cms.PSet(
        PF = cms.vstring("pass"),
        numberOfMatchedStations = cms.vdouble(1, 99),
        GlbPT = cms.vstring("pass"),
        tkTrackerLay = cms.vdouble(5, 99),
        tkValidPixelHits = cms.vdouble(0, 99),

        pt     = cms.vdouble(  20, 500 ),
        abseta = cms.vdouble(  0.0, 2.1),
        tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        #tag selections
        tag_pt = cms.vdouble(25, 500),
        tag_abseta = cms.vdouble(0, 2.1),
        tag_IsoMu20 = cms.vstring("pass"),

        dxyBS= cms.vdouble(-0.02, 0.02),
        dzPV = cms.vdouble(-0.1, 0.1),
        )

process.TnP_MuonID = Template.clone(
        InputFileNames = cms.vstring(
            'root://eoscms//eos/cms/store/group/phys_muon/perrin/SF50ns/TnP_trees/SmallTnP_trees_aod747_DY_withNVtxWeights.root',
            ),
        InputTreeName = cms.string("fitter_tree"),
        InputDirectoryName = cms.string("tpTree"),
        OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
        Efficiencies = cms.PSet(),
        )


if scenario == 'mc_all':
    process.TnP_MuonID.WeightVariable = cms.string("weight")
    process.TnP_MuonID.Variables.weight = cms.vstring("weight","0","10","")

#IDS

#Identifications
#IDS = ["Loose_noIP", "Medium_noIP", "Tight_noIP"]
#IDS = ["Loose_IP", "Medium_IP","Tight_IP","Tight_tightIP"]#Has to be the same as the name of the Cut
#Isolations
IDS = ["LooseIso4"]
#IDS = ["TightIso4"]

#BIN

#Identifications
#ALLBINS= [("eta", ETA_BINS), ("pt", PT_ETA_BINS), ("vtx",VTX_BINS)]

#Isolations
ALLBINS= [("LooseId_noIP_eta", LOOSE_noIP_ETA_BINS), ("LooseId_noIP_pt",LOOSE_noIP_PT_ETA_BINS), ("LooseId_noIP_vtx",LOOSE_noIP_VTX_BINS)]
#ALLBINS= [("MediumId_noIP_eta", MEDIUM_noIP_ETA_BINS), ("MediumId_noIP_pt", MEDIUM_noIP_PT_ETA_BINS), ("MediumId_noIP_vtx",MEDIUM_noIP_VTX_BINS)]
#ALLBINS= [("TightId_noIP_eta",TIGHT_noIP_ETA_BINS), ("TightId_noIP_pt", TIGHT_noIP_PT_ETA_BINS), ("TightId_noIP_vtx",TIGHT_noIP_VTX_BINS)]

#Isolation for ID+IP
#ALLBINS= [("LooseId_eta", LOOSE_ETA_BINS), ("LooseId_pt",LOOSE_PT_ETA_BINS), ("LooseId_vtx",LOOSE_VTX_BINS)]
#ALLBINS= [("MediumId_eta", MEDIUM_ETA_BINS), ("MediumId_pt", MEDIUM_PT_ETA_BINS), ("MediumId_vtx",MEDIUM_VTX_BINS)]
#ALLBINS= [("TightId_eta", TIGHT_ETA_BINS), ("TightId_pt", TIGHT_PT_ETA_BINS), ("TightId_vtx",TIGHT_VTX_BINS)]

#Isolation for ID+tightIP
#ALLBINS= [("TightId_tightIP_eta", TIGHT_TIGHTIP_ETA_BINS), ("TightId_tightIP_pt", TIGHT_TIGHTIP_PT_ETA_BINS), ("TightId_tightIP_vtx", TIGHT_TIGHTIP_VTX_BINS)]

if len(args) > 1 and args[1] not in IDS: IDS += [ args[1] ]
for ID in IDS:
    if len(args) > 1 and ID != args[1]: continue
    for X,B in ALLBINS:
        if len(args) > 2 and X not in args[2:]: continue
        if scenario == 'data_all': module = process.TnP_MuonID.clone(OutputFileName = cms.string("DATAeff4/TnP_MuonID_%s_%s_%s.root" % (scenario, ID, X)))
        elif scenario == 'mc_all': module = process.TnP_MuonID.clone(OutputFileName = cms.string("MCeff4/TnP_MuonID_%s_%s_%s.root" % (scenario, ID, X)))
        shape = "vpvPlusExpo"
        #change the shape and the range as a function of the selection and the variable
        if "eta" in X and not "abseta" in X: shape = "voigtPlusExpo"
        if "pt_abseta" in X: shape = "voigtPlusExpo"
        if X.find("pt_abseta") != -1: module.Variables.mass[1]="77";#change the invariant mass range
        if X.find("overall") != -1: module.binsForFit = 120 #change the bins for fit
        DEN = B.clone(); num = ID;
        if "24" in ID and hasattr(DEN,'pt') and "pt" not in X: DEN.pt[0] = 25 #change pt range
        #Implement reliso
        #if "_from_" in ID:
            #parts = ID.split("_from_")
            #num = parts[0]
            #setattr(DEN, parts[1], cms.vstring("above"))

        #compute isolation efficiency 
        if scenario == 'data_all'
            if num.find("Iso4") != -1: 
                setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                    EfficiencyCategoryAndState = cms.vstring(num,"below"),
                    UnbinnedVariables = cms.vstring("weight"),
                    BinnedVariables = DEN,
                    BinToPDFmap = cms.vstring(shape)
                ))
            #Compute id efficiency
            else:
                setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                    EfficiencyCategoryAndState = cms.vstring(num,"above"),
                    UnbinnedVariables = cms.vstring("weight"),
                    BinnedVariables = DEN,
                    BinToPDFmap = cms.vstring(shape)
                ))
        elif scenario == 'mc_all'
            if num.find("Iso4") != -1: 
                setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                    EfficiencyCategoryAndState = cms.vstring(num,"below"),
                    UnbinnedVariables = cms.vstring("mass","weight"),
                    BinnedVariables = DEN,
                    BinToPDFmap = cms.vstring(shape)
                ))
            #Compute id efficiency
            else:
                setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                    EfficiencyCategoryAndState = cms.vstring(num,"above"),
                    UnbinnedVariables = cms.vstring("mass","weight"),
                    BinnedVariables = DEN,
                    BinToPDFmap = cms.vstring(shape)
                ))
        setattr(process, "TnP_MuonID_"+ID+"_"+X, module)        
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))

