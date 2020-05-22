import os

import glob

from RootTools.core.standard import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

# modules
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *

nbSkim = 'Max$(GenPart_mass*(abs(GenPart_pdgId)==1000024))==850&&Max$(GenPart_mass*(abs(GenPart_pdgId)==1000022))==1'

#sampleFiles = glob.glob('WH_skim_v3.root')
#outputFile =  'WH_skim_v3_JEC.root'
#p = PostProcessor('./', glob.glob('/hadoop/cms/store/user/dspitzba/nanoAOD/SMS-TChiWH_WToLNu_HToBB_TuneCP2_13TeV-madgraphMLM-pythia8__RunIIFall17NanoAODv6-PUFall17Fast_Nano25Oct2019_102X_mc2017_realistic_v7-v1/*.root'), cut=nbSkim, haddFileName='WH_skim_v3.root')

'''
FastSim 2016
'''
#skim = '(1)'
#sampleFiles = glob.glob('/hadoop/cms/store/user/dspitzba/nanoAOD/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISummer16NanoAODv4-PUSummer16v3Fast_Nano14Dec2018_lhe_102X_mcRun2_asymptotic_v6-v1/*.root')
#outputFile = '/hadoop/cms/store/user/dspitzba/WH_studies/ttdilep_JEC_2016.root'
#
## corrector for FatJets
#JMECorrector = createJMECorrector(isMC=True, dataYear='2016', jesUncert="Total", jetType = "AK8PFPuppi", isFastSim=True)
## corrector for AK4 jets and MET
#METCorrector = createJMECorrector(isMC=True, dataYear='2016', jesUncert="Total", jetType = "AK4PFchs", isFastSim=True)
#
#modules = [
#    JMECorrector(),
#    METCorrector()
#    ]



'''
FastSim 2017
'''

skim = '(1)'
sampleFiles = glob.glob('/hadoop/cms/store/user/dspitzba/nanoAOD/TTJets_DiLept_TuneCP2_13TeV-madgraphMLM-pythia8__RunIIFall17NanoAODv4-PUFall17Fast_Nano14Dec2018_lhe_102X_mc2017_realistic_v6-v1/*.root')
outputFile = '/hadoop/cms/store/user/dspitzba/WH_studies/ttdilep_JEC.root'

# corrector for FatJets
JMECorrector = createJMECorrector(isMC=True, dataYear='2017', jesUncert="Total", jetType = "AK8PFPuppi", isFastSim=True)
# corrector for AK4 jets and MET
METCorrector = createJMECorrector(isMC=True, dataYear='2017', jesUncert="Total", jetType = "AK4PFchs", isFastSim=True)

modules = [
    JMECorrector(),
    METCorrector()
    ]


'''
FullSim 2017 signal
'''
#skim = '(1)'
#sampleFiles = glob.glob('/hadoop/cms/store/user/dspitzba/nanoAOD/SMS_TChiWH_WToLNu_HToBB_mChargino850_mLSP1_TuneCP5_13TeV-madgraphMLM-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/*.root')
#outputFile = 'WH_FullSim_JEC.root'
#
## corrector for FatJets
#JMECorrector = createJMECorrector(isMC=True, dataYear='2017', jesUncert="Total", jetType = "AK8PFPuppi", isFastSim=False)
## no need to recorrect AK4 jets and MET for FullSim
#
#modules = [
#    JMECorrector()
#    ]
#

p = PostProcessor('./', sampleFiles, modules=modules, haddFileName=outputFile)
p.run()
