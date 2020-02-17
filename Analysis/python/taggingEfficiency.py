#!/usr/bin/env python
import os, sys
import ROOT
import array
import json

ROOT.PyConfig.IgnoreCommandLineOptions = True

from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from RootTools.core.standard import *

## Define QCD samples

QCD_100to200 = Sample.fromDirectory("QCD_100to200", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT100to200_TuneCP5_13TeV-madgraph-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/", "Events", xSection=123.)
QCD_1500to2000 = Sample.fromDirectory("QCD_1500to2000", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/", "Events", xSection=123.)

samples = [QCD_100to200]

for s in samples:
    s.normalization = s.getYieldFromDraw("(1)", "genWeight")
    s.weight = lambda sample, event: event.genWeight*sample.xSection*1000/sample.normalziation




## Do the nanoAOD-tools stuff
class TriggerAnalysis(Module):
    def __init__(self, btagWP=0.4, htagWP=0.8):
        self.writeHistFile = True
        self.btagWP = btagWP
        self.htagWP = htagWP

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)

        pt_thresholds           = range(0,30,2)+range(30,50,5)+range(50,210,10)
        eta_thresholds          = [x/10. for x in range(-25,26,1) ]
        pt_thresholds_coarse    = range(10,30,10)+range(30,135,15)+range(135,335,50)
        pt_thresholds_veryCoarse = [20,30,40] + range(50,200,50)+[250]
        eta_thresholds_coarse   = [x/10. for x in range(-25,26,5) ]

        # 1D hists
        self.h_nFatJets         = ROOT.TH1F("nFatJets",         "", 5, -0.5, 4.5)
        self.h_nFatJets_withB   = ROOT.TH1F("nFatJets_withB",   "", 5, -0.5, 4.5)
        self.h_nFatJets_Htagged = ROOT.TH1F("nFatJets_Htagged", "", 5, -0.5, 4.5)

        for o in [self.h_nFatJets, self.h_nFatJets_withB, self.h_nFatJets_Htagged]:
            self.addObject(o)

    def analyze(self, event):
        electrons   = Collection(event, "Electron")
        muons       = Collection(event, "Muon")
        jets        = Collection(event, "Jet")
        subjets     = Collection(event, "SubJet")
        fatjets     = Collection(event, "FatJet")

        nFatJets = len(fatjets)
        nFatJets_withB = 0
        nFatJets_Htagged = 0
        for fatjet in fatjets:
            subJet1_bScore = -1
            subJet2_bScore = -1
            id1 = fatjet.subJetIdx1
            id2 = fatjet.subJetIdx2

            if id1>=0:
                subJet1_bScore = subjets[id1].btagDeepB
            if id2>=0:
                subJet2_bScore = subjets[id2].btagDeepB

            if subJet1_bScore>self.btagWP or subJet2_bScore>self.btagWP:
                nFatJets_withB += 1

            if fatjet.deepTag_H>self.htagWP: nFatJets_Htagged += 1

        self.h_nFatJets.Fill(nFatJets)
        self.h_nFatJets_withB.Fill(nFatJets_withB)
        self.h_nFatJets_Htagged.Fill(nFatJets_Htagged)

        return True

    def endJob(self):
        pass
        #self.eff    = ROOT.TEfficiency(self.h_pt1_passEvents, self.h_pt1_totalEvents)
        #self.addObject(self.eff)


preselection = '(1)'
files = QCD_1500to2000.files[:1]

p=PostProcessor(".", files, cut=preselection,branchsel=None,modules=[TriggerAnalysis()],noOut=True,histFileName="histOut.root",histDirName="plots")

print "Run"

p.run()

