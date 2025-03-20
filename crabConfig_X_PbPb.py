from CRABClient.UserUtilities import config
config = config()

config.General.transferOutputs = True
config.General.workArea = 'crab_projects'
config.JobType.pluginName = 'Analysis'
config.JobType.maxMemoryMB = 2500
config.JobType.numCores = 1
config.JobType.pyCfgParams = ['noprint']

######################################################################################################################################################
###################################       TO BE HANDLED AUTOMATICALY BY large_crabTask_submission_handler.py       ###################################
######################################################################################################################################################

config.JobType.psetName = 'forest_miniAOD_run3_MC_wBfinder.py'
config.Data.inputDataset = '/MC_PbPb_X3872/hmarques-prompt_X3872_to_Jpsi_Rho_phat5_miniAOD-80a77cd862f44822931af5f8ae2b9b98/USER'
config.General.requestName = 'MC_PbPb_prompt_X3872_to_Jpsi_Rho_phat5_Bfinder'
config.Data.outputDatasetTag = 'prompt_X3872_to_Jpsi_Rho_phat5_Bfinder'

######################################################################################################################################################
###################################       TO BE HANDLED AUTOMATICALY BY large_crabTask_submission_handler.py       ###################################
######################################################################################################################################################

config.Data.inputDBS = 'phys03'
config.Data.unitsPerJob = 1 
config.Data.totalUnits = -1
config.Data.splitting = 'FileBased'
config.Data.publication = True

config.Site.storageSite = "T2_US_Vanderbilt"