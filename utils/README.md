# Samples from the grid

## Search for sample on DAS
You need a valid proxy (`voms-proxy-init`)
```
dasgoclient -query='/TTJets_SingleLeptFromT_Tune*/RunIIFall17*/NANOAODSIM'
```
The first part specifies the process (ttbar+jets with leptonic decay of the top quark (not the top anti-quark).
The second part is the production campaign. We're using MC for RunII (2015-2018), and the Fall17 campaign is what's used for 2017.
The last part is the data tier, we use simulated NanoAOD.
The command yields a list of samples:
```
/TTJets_SingleLeptFromT_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PUFall17Fast_Nano1June2019_lhe_102X_mc2017_realistic_v7-v1/NANOAODSIM
/TTJets_SingleLeptFromT_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv6-PUFall17Fast_Nano25Oct2019_lhe_102X_mc2017_realistic_v7-v1/NANOAODSIM
/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM
/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM
/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM
/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_ext_102X_mc2017_realistic_v7-v1/NANOAODSIM
/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PUMoriond17_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM
/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PUMoriond17_94X_mcRun2_asymptotic_v2_ext1-v1/NANOAODSIM
```
We want to use the latest NanoAOD version (v6), and compare FullSim and FastSim.
Therefore, the samples of interest are:
```
/TTJets_SingleLeptFromT_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv6-PUFall17Fast_Nano25Oct2019_lhe_102X_mc2017_realistic_v7-v1/NANOAODSIM
/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_ext_102X_mc2017_realistic_v7-v1/NANOAODSIM
```

If we want to know more about the samples, you can e.g. do
```
dasgoclient -query='summary dataset=/TTJets_SingleLeptFromT_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv6-PUFall17Fast_Nano25Oct2019_lhe_102X_mc2017_realistic_v7-v1/NANOAODSIM'
dasgoclient -query='file dataset=/TTJets_SingleLeptFromT_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv6-PUFall17Fast_Nano25Oct2019_lhe_102X_mc2017_realistic_v7-v1/NANOAODSIM'
dasgoclient -query='site dataset=/TTJets_SingleLeptFromT_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv6-PUFall17Fast_Nano25Oct2019_lhe_102X_mc2017_realistic_v7-v1/NANOAODSIM'
```
The `site` option is currently broken (May 2020).

We can copy them to the local storage (hadoop) with the `print_download_commands.sh` script.
Add the samples you want to copy, and then run
```
./print_download_commands.sh > commands.txt; ./parallel --nice 10 --jobs 10 --bar --joblog joblog.txt < commands.txt
```
