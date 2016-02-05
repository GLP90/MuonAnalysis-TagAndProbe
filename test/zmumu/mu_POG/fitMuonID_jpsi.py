import FWCore.ParameterSet.Config as cms
import sys, os, shutil
from optparse import OptionParser
### USAGE: cmsRun fitMuonID.py test3 1 mc mc_all
###
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
id_bins = '1'
if len(args) > 2: id_bins = args[2]
print 'The id_bins is', id_bins
scenario = "data_all"
if len(args) > 3: scenario = args[3]
print "Will run scenario ", scenario
sample = 'data'
if len(args) > 4: sample = args[4]
print 'The sample is', sample 

process = cms.Process("TagProbe")
process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

#_*_*_*_*_*_*_*_*_*_*_*_*
#Prepare variables, den, num and fit funct
#_*_*_*_*_*_*_*_*_*_*_*_*

#Set-up the mass range

Template = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
        NumCPU = cms.uint32(1),
    SaveWorkspace = cms.bool(False),


    Variables = cms.PSet(
        weight = cms.vstring("weight","-100","100",""),
        mass = cms.vstring("Tag-muon Mass", "2.8", "3.35", "GeV/c^{2}"),
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
        tkTrackerLay = cms.vstring("tkTrackerLay", "-10","1000",""),
        tkPixelLay = cms.vstring("tkPixelLay", "-10","1000",""),
        ),

    Categories = cms.PSet(
        PF    = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
        Medium   = cms.vstring("Medium Id. Muon", "dummy[pass=1,fail=0]"),
        Tight2012 = cms.vstring("Tight Id. Muon", "dummy[pass=1,fail=0]"),
        TMOST = cms.vstring("TMOneStationTight", "dummy[pass=1,fail=0]"),
        tag_IsoMu20 = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
        Track_HP = cms.vstring("High-Purity muons", "dummy[pass=1,fail=0]"),
    ),

    Expressions = cms.PSet(
        #ID 
        Loose_noIPVar = cms.vstring("Loose_noIPVar", "PF==1", "PF"),
        Medium_noIPVar= cms.vstring("Medium_noIPVar", "Medium==1", "Medium"),
        Tight2012_zIPCutVar = cms.vstring("Tight2012_zIPCut", "Tight2012 == 1 && abs(dzPV) < 0.5", "Tight2012", "dzPV"),
        SoftVar = cms.vstring("SoftVar", "TMOST == 1 && tkTrackerLay > 5 && tkPixelLay > 0 && abs(dzPV) < 20 && abs(dB) < 0.3 && Track_HP == 1", "TMOST","tkTrackerLay", "tkPixelLay", "dzPV", "dB", "Track_HP"),
    ),

    Cuts = cms.PSet(
        #ID
        Loose_noIP = cms.vstring("Loose_noIP", "Loose_noIPVar", "0.5"),
        Medium_noIP= cms.vstring("Medium_noIP", "Medium_noIPVar", "0.5"),
        Tight2012_zIPCut = cms.vstring("Tight2012_zIPCut", "Tight2012_zIPCutVar", "0.5"),
        SoftID = cms.vstring("Soft", "SoftVar", "0.5"),

        #Isolations
        LooseIso4 = cms.vstring("LooseIso4" ,"combRelIsoPF04dBeta", "0.25"),
        TightIso4 = cms.vstring("TightIso4" ,"combRelIsoPF04dBeta", "0.15"),
    ),

                          
    PDFs = cms.PSet(
        gaussPlusExpo = cms.vstring(
            "Gaussian::signal(mass, mean[3.1,3.0,3.2], sigma[0.05,0.02,0.1])",
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

ETA_BINS = cms.PSet(
    pt  = cms.vdouble(0, 100),
    eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
PT_ALLETA_BINS = cms.PSet(
    #Main
    pt     = cms.vdouble(0, 5, 10, 15, 20),
    #For testing bkg function
    #pt     = cms.vdouble(60, 80, 120, 200),
    abseta = cms.vdouble(  0.0, 2.4),
    pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
    #tag selections
    tag_pt = cms.vdouble(21, 500),
    tag_IsoMu20 = cms.vstring("pass"), 
    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
)
PT_ETA_BINS = cms.PSet(
    #Main
    #pt     = cms.vdouble(20, 25, 30, 40, 50, 60, 80, 120, 200),
    pt     = cms.vdouble(0, 5, 10, 15, 20),
    #For testing bkg function
    #pt     = cms.vdouble(60, 80, 120, 200),
    abseta = cms.vdouble( 0., 0.9, 1.2, 2.1, 2.4),
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
            'samples/TnPTree_76X_DYLL_M50_MadGraphMLM_withNVtxWeights_total.root'
            ),
        InputTreeName = cms.string("fitter_tree"),
        InputDirectoryName = cms.string("tpTree"),
        OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
        Efficiencies = cms.PSet(),
        )
if sample == "data":
    process.TnP_MuonID = Template.clone(
        InputFileNames = cms.vstring(
            #'root://eoscms//eos/cms/store/group/phys_tracking/gpetrucc/tnp/76X/tnpZ_MC_DY76_chunk0.root'
            #'samples/TnPTree_76X_RunC_and_D_total.root'
            'samples/TnPTree_76X_RunC.root',
            'samples/TnPTree_76X_RunD_part1.root',
            'samples/TnPTree_76X_RunD_part2.root',
            'samples/TnPTree_76X_RunD_part3.root',
            'samples/TnPTree_76X_RunD_part4.root'
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
if id_bins == '1':
    ID_BINS = [
    (("Loose_noIP"), ("NUM_LooseID_DEN_genTracks_PAR_eta", ETA_BINS)),
    #(("Loose_noIP"), ("NUM_LooseID_DEN_genTracks_PAR_coarse_eta", COARSE_ETA_BINS)),
    #(("Loose_noIP"), ("NUM_LooseID_DEN_genTracks_PAR_vtx_bin1_24", VTX_BINS_ETA24 )),
    (("Loose_noIP"), ("NUM_LooseID_DEN_genTracks_PAR_pt_alleta_bin1", PT_ALLETA_BINS)),
    (("Loose_noIP"), ("NUM_LooseID_DEN_genTracks_PAR_pt_spliteta_bin1", PT_ETA_BINS)),
    ]
#Medium ID
if id_bins == '2':
    ID_BINS = [
    (("Medium_noIP"), ("NUM_MediumID_DEN_genTracks_PAR_eta", ETA_BINS)),
    #(("Medium_noIP"), ("NUM_MediumID_DEN_genTracks_PAR_coarse_eta", COARSE_ETA_BINS)),
    #(("Medium_noIP"), ("NUM_MediumID_DEN_genTracks_PAR_vtx_bin1_24", VTX_BINS_ETA24 )),
    (("Medium_noIP"), ("NUM_MediumID_DEN_genTracks_PAR_pt_alleta_bin1", PT_ALLETA_BINS)),
    (("Medium_noIP"), ("NUM_MediumID_DEN_genTracks_PAR_pt_spliteta_bin1", PT_ETA_BINS)),
    ]
#Tight ID
if id_bins == '3':
    ID_BINS = [
    (("Tight2012_zIPCut"), ("NUM_TightIDandIPCut_DEN_genTracks_PAR_eta", ETA_BINS)),
    #(("Tight2012_zIPCut"), ("NUM_TightID_DEN_genTracks_PAR_coarse_eta", COARSE_ETA_BINS)),
    #(("Tight2012_zIPCut"), ("NUM_TightIDandIPCut_DEN_genTracks_PAR_vtx_bin1_24", VTX_BINS_ETA24 )),
    (("Tight2012_zIPCut"), ("NUM_TightIDandIPCut_DEN_genTracks_PAR_pt_alleta_bin1", PT_ALLETA_BINS)),
    (("Tight2012_zIPCut"), ("NUM_TightIDandIPCut_DEN_genTracks_PAR_pt_spliteta_bin1", PT_ETA_BINS)),
    ]
#SoftID
if id_bins == '4':
    ID_BINS = [
    #(("SoftID"), ("NUM_SoftID_DEN_genTracks_PAR_eta", ETA_BINS)),
    #(("SoftID"), ("NUM_SoftID_DEN_genTracks_PAR_coarse_eta", COARSE_ETA_BINS)),
    #(("SoftID"), ("NUM_SoftID_DEN_genTracks_PAR_vtx_bin1_24", VTX_BINS_ETA24 )),
    #(("SoftID"), ("NUM_SoftID_DEN_genTracks_PAR_pt_alleta_bin1", PT_ALLETA_BINS)),
    #(("SoftID"), ("NUM_SoftID_DEN_genTracks_PAR_pt_spliteta_bin1", PT_ETA_BINS)),
    ]
#Additional studies on Medium ID (in selected eta region)
#Medium ID
if id_bins == '5':
    ID_BINS = [
    #(("Medium_noIP"), ("NUM_MediumID_DEN_genTracks_PAR_phi_loweta", PHI_LOWETA)),
    #(("Medium_noIP"), ("NUM_MediumID_DEN_genTracks_PAR_phi_higheta", PHI_HIGHETA )),
    #(("Medium_noIP"), ("NUM_MediumID_DEN_genTracks_PAR_pt_highabseta", PT_HIGHABSETA)),
    #(("Medium_noIP"), ("NUM_MediumID_DEN_genTracks_PAR_vtx_highabseta", VTX_HIGHABSETA)),
    ]
#_*_*_*_*_*_*_*_*_*_*
#ISOs
#_*_*_*_*_*_*_*_*_*_*
#Loose Iso
if id_bins == '6':
    ID_BINS = [
    (("LooseIso4"), ("NUM_LooseRelIso_DEN_LooseID_PAR_eta", LOOSE_ETA_BINS)),
    #(("LooseIso4"), ("NUM_LooseRelIso_DEN_LooseID_PAR_coarse_eta", LOOSE_COARSE_ETA_BINS)),
    #(("LooseIso4"), ("NUM_LooseRelIso_DEN_LooseID_PAR_vtx_bin1_24", LOOSE_VTX_BINS_ETA24 )),
    (("LooseIso4"), ("NUM_LooseRelIso_DEN_LooseID_PAR_pt_alleta_bin1", LOOSE_PT_ALLETA_BINS)),
    (("LooseIso4"), ("NUM_LooseRelIso_DEN_LooseID_PAR_pt_spliteta_bin1", LOOSE_PT_ETA_BINS)),
    ]
if id_bins == '7':
    ID_BINS = [
    #(("LooseIso4"), ("NUM_LooseRelIso_DEN_MediumID_PAR_eta", MEDIUM_ETA_BINS)),
    #(("LooseIso4"), ("NUM_LooseRelIso_DEN_MediumID_PAR_coarse_eta", MEDIUM_COARSE_ETA_BINS)),
    #(("LooseIso4"), ("NUM_LooseRelIso_DEN_MediumID_PAR_vtx_bin1_24", MEDIUM_VTX_BINS_ETA24 )),
    #(("LooseIso4"), ("NUM_LooseRelIso_DEN_MediumID_PAR_pt_alleta_bin1", MEDIUM_PT_ALLETA_BINS)),
    #(("LooseIso4"), ("NUM_LooseRelIso_DEN_MediumID_PAR_pt_spliteta_bin1", MEDIUM_PT_ETA_BINS)),
    ]
if id_bins == '8':
    ID_BINS = [
    (("LooseIso4"), ("NUM_LooseRelIso_DEN_TightID_PAR_eta", TIGHT_ETA_BINS)),
    #(("LooseIso4"), ("NUM_LooseRelIso_DEN_TightID_PAR_coarse_eta", TIGHT_COARSE_ETA_BINS)),
    #(("LooseIso4"), ("NUM_LooseRelIso_DEN_TightID_PAR_vtx_bin1_24", TIGHT_VTX_BINS_ETA24 )),
    #(("LooseIso4"), ("NUM_LooseRelIso_DEN_TightID_PAR_pt_alleta_bin1", TIGHT_PT_ALLETA_BINS)),
    #(("LooseIso4"), ("NUM_LooseRelIso_DEN_TightID_PAR_pt_spliteta_bin1", TIGHT_PT_ETA_BINS)),
    ]
#Tight Iso
if id_bins == '9':
    ID_BINS = [
    (("TightIso4"), ("NUM_TightRelIso_DEN_TightID_PAR_eta", TIGHT_ETA_BINS)),
    #(("TightIso4"), ("NUM_TightRelIso_DEN_TightID_PAR_coarse_eta", TIGHT_COARSE_ETA_BINS)),
    #(("TightIso4"), ("NUM_TightRelIso_DEN_TightID_PAR_vtx_bin1_24", TIGHT_VTX_BINS_ETA24 )),
    (("TightIso4"), ("NUM_TightRelIso_DEN_TightID_PAR_pt_alleta_bin1", TIGHT_PT_ALLETA_BINS)),
    (("TightIso4"), ("NUM_TightRelIso_DEN_TightID_PAR_pt_spliteta_bin1", TIGHT_PT_ETA_BINS)),
    ]
if id_bins == '10':
    ID_BINS = [
    (("TightIso4"), ("NUM_TightRelIso_DEN_MediumID_PAR_eta", MEDIUM_ETA_BINS)),
    #(("TightIso4"), ("NUM_TightRelIso_DEN_MediumID_PAR_coarse_eta", MEDIUM_COARSE_ETA_BINS)),
    #(("TightIso4"), ("NUM_TightRelIso_DEN_MediumID_PAR_vtx_bin1_24", MEDIUM_VTX_BINS_ETA24 )),
    (("TightIso4"), ("NUM_TightRelIso_DEN_MediumID_PAR_pt_alleta_bin1", MEDIUM_PT_ALLETA_BINS)),
    (("TightIso4"), ("NUM_TightRelIso_DEN_MediumID_PAR_pt_spliteta_bin1", MEDIUM_PT_ETA_BINS)),
    ]

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
    shutil.copyfile(os.getcwd()+'/fitMuonID.py',_output+'/fitMuonID.py')
    shape = cms.vstring("vpvPlusExpo")
    #shape = "vpvPlusCheb"
    if not "Iso" in ID:  #customize only for ID
        if (len(B.pt)==7):  #customize only when the pT have the high pt bins
            shape = cms.vstring("vpvPlusExpo","*pt_bin5*","vpvPlusCheb")
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

