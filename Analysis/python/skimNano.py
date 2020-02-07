import os

from RootTools.core.standard import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

WH_18 = Sample.fromDirectory('WH_18', '/hadoop/cms/store/user/dspitzba/nanoAOD/SMS-TChiWH_WToLNu_HToBB_TuneCP2_13TeV-madgraphMLM-pythia8__RunIIAutumn18NanoAODv6-PUFall18Fast_Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/',  'Events')

s = (800,1)
cut = "Max$(GenPart_mass*(abs(GenPart_pdgId)==1000024))=="+str(s[0])+"&&Max$(GenPart_mass*(abs(GenPart_pdgId)==1000022))=="+str(s[1])
## or just use
cut = "GenModel_TChiWH_WToLNu_HToBB_800_1"

#p = PostProcessor('./',tmp.files, outputbranchsel='keep_and_drop.txt', branchsel='keep_and_drop.txt', cut=nbSkim, haddFileName=tmp.name+'_v3.root', prefetch=True)
p = PostProcessor('./',WH_18.files, cut=cut, haddFileName=WH_18.name+'_v3.root')
#p.run()


#WH_18 = Sample.fromFiles('WH_18', ['./WH_18_v3.root'],  'Events')
WH_18 = Sample.fromDirectory('WH_had_750_1', ['/hadoop/cms/store/user/mibryson/WH_hadronic/WH_had_750_1/nanoAOD/'],  'Events')
WH_18 = Sample.fromDirectory('WH_had_500_150', ['/hadoop/cms/store/user/mibryson/WH_hadronic/WH_had_500_150/nanoAOD/'],  'Events')

from objectSelection           import WHObjects

#p = PostProcessor('./',WH_18.files, haddFileName=WH_18.name+'_v3_ext.root', modules=[WHObjects()])
p = PostProcessor('./',WH_18.files, haddFileName=WH_18.name+'_v1.root')

p.run()

