#This configuration is to perform produciton on DATA
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

#!!
#!!Change to run on other samples
#!!
#config.General.requestName = 'DATA_50ns'
#config.General.workArea = 'crab_tnp_2015B_PRreference'
#config.General.requestName = 'DATA_25ns'
#config.General.workArea = 'crab_tnp_2015D_25ns'
config.General.requestName = 'MCLO'
config.General.workArea = 'crab_tnp_MC_25ns'
#!!
#!!DataSet
#!!
#DATA
#2015B
#config.Data.inputDataset = '/SingleMuon/Run2015B-PromptReco-v1/AOD'
#2015B 50ns (new calorimeter conditions)
#config.Data.inputDataset = '/SingleMuon/CMSSW_7_4_11_patch1-Run2015B_PRreference_74X_dataRun2_Prompt_v3-v1/RECO'
#config.Data.inputDataset = '/SingleMuon/CMSSW_7_4_11_patch1-Run2015B_HLTreference_74X_dataRun2_HLT_v1-v1/RECO'
#2015C
#config.Data.inputDataset = '/SingleMuon/Run2015C-PromptReco-v1/AOD'
#2015C 50 ns (new calorimeter conditions) Run 254790
#config.Data.inputDataset = '/SingleMuon/CMSSW_7_4_11_patch1-Run2015C_PRreference_74X_dataRun2_Prompt_v3-v1/RECO'
#config.Data.inputDataset = '/SingleMuon/CMSSW_7_4_11_patch1-Run2015C_HLTreference_74X_dataRun2_HLT_v1-v1/RECO'
#2015D
#config.Data.inputDataset = '/SingleMuon/Run2015D-PromptReco-v3/AOD'
#MC
#25ns LO
config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM'
#25ns NLO
#config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/AODSIM'
#!!
#!!JSON
#!!
#25ns 
#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-256869_13TeV_PromptReco_Collisions15_25ns_JSON.txt'
#50ns
#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-255031_13TeV_PromptReco_Collisions15_50ns_JSON_v2.txt'
#!!
#!!RunRange
#!!
#config.Data.runRange = '246908-251884'
#!!
#!!config file
#!!
#config.JobType.psetName = 'tp_from_aod_Data.py'
config.JobType.psetName = 'tp_from_aod_MC.py'

config.General.transferOutputs = True
config.General.transferLogs = False
config.JobType.pluginName = 'Analysis'
python_file_list = []
f = open('input', 'r')
for line in f:
    python_file_list.append(line.strip('\n'))

config.JobType.inputFiles = python_file_list
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 50
config.Data.outLFNDirBase = '/store/user/%s/' % getUsernameFromSiteDB()
config.Data.publication = True
config.Data.publishDataName = 'crab_tnp_production_mc_25ns_LO'
config.Site.storageSite = 'T2_CH_CSCS'

