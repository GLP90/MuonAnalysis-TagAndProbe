from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()
config.General.requestName = 'AODSIM_50ns_noweights'
config.General.workArea = 'crab_tnp_mcgen1'
config.General.transferOutputs = True
config.General.transferLogs = False
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/afs/cern.ch/work/g/gaperrin/private/CMSSW_7_4_7/src/MuonAnalysis/TagAndProbe/test/zmumu/tp_from_aod_MC.py'
python_file_list = []
f = open('input', 'r')
for line in f:
    python_file_list.append(line.strip('\n'))

config.JobType.inputFiles = python_file_list
config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 50
config.Data.outLFNDirBase = '/store/user/%s/' % getUsernameFromSiteDB()
config.Data.publication = True
config.Data.publishDataName = 'crab_tnp_production_MC'
config.Site.storageSite = 'T2_CH_CSCS'

