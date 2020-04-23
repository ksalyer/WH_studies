#!/usr/bin/env bash

function print_commands {
    dsname=$1
    nicename=$(echo $dsname | cut -d '/' -f2-3 | sed 's|\/|__|g')
    files=$(./dis_client.py -t files -d "$dsname | grep name")
    for f in $files ; do
        tailname=$(echo $f | rev | cut -d '/' -f1 | rev)
        echo xrdcp root://cmsxrootd.fnal.gov/$f root://redirector.t2.ucsd.edu//store/user/dspitzba/nanoAOD/$nicename/$tailname
    done
}

# ./print_download_commands.sh > commands.txt; ./parallel --nice 10 --jobs 10 --bar --joblog joblog.txt < commands.txt

#print_commands /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7_ext1-v1/NANOAODSIM
print_commands /TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv4-PUSummer16v3Fast_Nano14Dec2018_lhe_102X_mcRun2_asymptotic_v6-v1/NANOAODSIM
