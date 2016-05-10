from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()
config.General.requestName = 'AODSIM_25ns'
config.General.workArea = 'crab_mcgen'
config.General.transferOutputs = True
config.General.transferLogs = False
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'tp_from_aod_MC.py'
python_file_list = []
f = open('input', 'r')
for line in f:
    python_file_list.append(line.strip('\n'))

config.JobType.inputFiles = python_file_list
config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16DR80-PUSpring16_80X_mcRun2_asymptotic_2016_v3_ext1-v1/AODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 100 
config.Data.outLFNDirBase = '/store/user/%s/' % getUsernameFromSiteDB()
config.Data.publication = True
#config.Data.publishDataName = 'crab_tnp_production_MC'
config.Data.outputDatasetTag = 'crab_tnp_production_MC'
config.Site.storageSite = 'T2_CH_CSCS'

