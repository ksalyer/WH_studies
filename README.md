# WH_studies

Recipe:
```
cmsrel CMSSW_10_2_9
cd CMSSW_10_2_9/src/
cmsenv
git cms-init

git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools

git clone https://github.com/HephyAnalysisSW/RootTools.git
cd $CMSSW_BASE/src

git clone --recursive https://github.com/danbarto/WH_studies.git
cd $CMSSW_BASE/src

scram b -j 8
```
