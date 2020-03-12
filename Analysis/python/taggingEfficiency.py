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

def fixUncertainties(teff, heff, x_binning, y_binning):
    for x in x_binning:
        for y in y_binning:
            x_bin = heff.GetXaxis().FindBin(x)
            y_bin = heff.GetYaxis().FindBin(y)
            n_bin = teff.FindFixBin(x,y)
            err   = (teff.GetEfficiencyErrorUp(n_bin) + teff.GetEfficiencyErrorLow(n_bin) ) / 2.
            heff.SetBinError(x_bin, y_bin, err)
    return heff

def writeObjToFile(fname, obj, update=False):
    gDir = ROOT.gDirectory.GetName()
    if update:
        f = ROOT.TFile(fname, 'UPDATE')
    else:
        f = ROOT.TFile(fname, 'recreate')
    objw = obj.Clone()
    objw.Write()
    f.Close()
    ROOT.gDirectory.cd(gDir+':/')
    return

## Define QCD samples
S16_QCD_500to700    = Sample.fromDirectory("S16_QCD_500to700", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/", "Events", xSection=123.)
S16_QCD_700to1000   = Sample.fromDirectory("S16_QCD_700to1000", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/", "Events", xSection=123.)
S16_QCD_1000to1500  = Sample.fromDirectory("S16_QCD_1000to1500", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/", "Events", xSection=123.)
S16_QCD_2000toInf   = Sample.fromDirectory("S16_QCD_2000toInf", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/", "Events", xSection=123.)

F17_QCD_100to200    = Sample.fromDirectory("F17_QCD_100to200", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT100to200_TuneCP5_13TeV-madgraph-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/", "Events", xSection=123.)
F17_QCD_200to300    = Sample.fromDirectory("F17_QCD_200to300", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT200to300_TuneCP5_13TeV-madgraph-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/", "Events", xSection=123.)
F17_QCD_300to500    = Sample.fromDirectory("F17_QCD_300to500", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT300to500_TuneCP5_13TeV-madgraph-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/", "Events", xSection=123.)
F17_QCD_500to700    = Sample.fromDirectory("F17_QCD_500to700", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT500to700_TuneCP5_13TeV-madgraph-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/", "Events", xSection=123.)
F17_QCD_700to1000   = Sample.fromDirectory("F17_QCD_700to1000", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/", "Events", xSection=123.)
F17_QCD_1000to1500  = Sample.fromDirectory("F17_QCD_1000to1500", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/", "Events", xSection=123.)
F17_QCD_1500to2000  = Sample.fromDirectory("F17_QCD_1500to2000", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/", "Events", xSection=123.)
F17_QCD_2000toInf   = Sample.fromDirectory("F17_QCD_2000toInf", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/", "Events", xSection=123.)

A18_QCD_100to200    = Sample.fromDirectory("A18_QCD_100to200", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT100to200_TuneCP5_13TeV-madgraph-pythia8__RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/", "Events", xSection=123.)
A18_QCD_200to300    = Sample.fromDirectory("A18_QCD_200to300", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT200to300_TuneCP5_13TeV-madgraph-pythia8__RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/", "Events", xSection=123.)
A18_QCD_300to500    = Sample.fromDirectory("A18_QCD_300to500", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT300to500_TuneCP5_13TeV-madgraph-pythia8__RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/", "Events", xSection=123.)
A18_QCD_500to700    = Sample.fromDirectory("A18_QCD_500to700", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT500to700_TuneCP5_13TeV-madgraph-pythia8__RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/", "Events", xSection=123.)
A18_QCD_700to1000   = Sample.fromDirectory("A18_QCD_700to1000", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8__RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/", "Events", xSection=123.)
A18_QCD_1000to1500  = Sample.fromDirectory("A18_QCD_1000to1500", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8__RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/", "Events", xSection=123.)
A18_QCD_1500to2000  = Sample.fromDirectory("A18_QCD_1500to2000", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8__RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/", "Events", xSection=123.)
A18_QCD_2000toInf   = Sample.fromDirectory("A18_QCD_2000toInf", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8__RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/", "Events", xSection=123.)


TTJetsHad = Sample.fromDirectory("TTJetsHad", "/hadoop/cms/store/user/dspitzba/nanoAOD/TTToHadronic_TuneCP5_13TeV-powheg-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_new_pmx_102X_mc2017_realistic_v7-v2/", "Events", xSection=123.)


#for s in samples:
#    s.normalization = s.getYieldFromDraw("(1)", "genWeight")
#    s.weight = lambda sample, event: event.genWeight*sample.xSection*1000/sample.normalziation

S16_QCD = Sample.combine("S16_QCD_combined", [S16_QCD_500to700,S16_QCD_700to1000,S16_QCD_1000to1500,S16_QCD_2000toInf])
F17_QCD = Sample.combine("F17_QCD_combined", [F17_QCD_100to200,F17_QCD_200to300,F17_QCD_300to500,F17_QCD_500to700,F17_QCD_700to1000,F17_QCD_1000to1500,F17_QCD_1500to2000,F17_QCD_2000toInf])
A18_QCD = Sample.combine("A18_QCD_combined", [A18_QCD_100to200,A18_QCD_200to300,A18_QCD_300to500,A18_QCD_500to700,A18_QCD_700to1000,A18_QCD_1000to1500,A18_QCD_1500to2000,A18_QCD_2000toInf])

sample = F17_QCD

## Do the nanoAOD-tools stuff
class TriggerAnalysis(Module):
    def __init__(self, btagWP=0.4941, htagWP=0.8):
        self.writeHistFile = True
        self.btagWP = btagWP
        self.htagWP = htagWP

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)

        pt_thresholds           = [150,200,250,300,400,500,750,1200]
        mass_thresholds         = [0,30,60,90,110,130,150,200,250,400]
        mass_thresholds_coarse  = [0,50,90,115,135,160,200,250,400]

        # 1D hists
        self.h_nFatJets         = ROOT.TH1F("nFatJets",         "", 5, -0.5, 4.5)
        self.h_nFatJets_withB   = ROOT.TH1F("nFatJets_withB",   "", 5, -0.5, 4.5)
        self.h_nFatJets_Htagged = ROOT.TH1F("nFatJets_Htagged", "", 5, -0.5, 4.5)

        # 2D hists
        self.h_pt_mass_pass_2b  = ROOT.TH2D("pt_mass_pass_2b","",  len(pt_thresholds)-1, array.array('d',pt_thresholds), len(mass_thresholds_coarse)-1, array.array('d',mass_thresholds_coarse))
        self.h_pt_mass_total_2b = ROOT.TH2D("pt_mass_total_2b","", len(pt_thresholds)-1, array.array('d',pt_thresholds), len(mass_thresholds_coarse)-1, array.array('d',mass_thresholds_coarse))
        self.h_pt_mass_pass_1b  = ROOT.TH2D("pt_mass_pass_1b","",  len(pt_thresholds)-1, array.array('d',pt_thresholds), len(mass_thresholds_coarse)-1, array.array('d',mass_thresholds_coarse))
        self.h_pt_mass_total_1b = ROOT.TH2D("pt_mass_total_1b","", len(pt_thresholds)-1, array.array('d',pt_thresholds), len(mass_thresholds_coarse)-1, array.array('d',mass_thresholds_coarse))
        self.h_pt_mass_pass_0b  = ROOT.TH2D("pt_mass_pass_0b","",  len(pt_thresholds)-1, array.array('d',pt_thresholds), len(mass_thresholds_coarse)-1, array.array('d',mass_thresholds_coarse))
        self.h_pt_mass_total_0b = ROOT.TH2D("pt_mass_total_0b","", len(pt_thresholds)-1, array.array('d',pt_thresholds), len(mass_thresholds_coarse)-1, array.array('d',mass_thresholds_coarse))
        self.h_pt_massSD_pass  = ROOT.TH2D("pt_massSD_pass","",  len(pt_thresholds)-1, array.array('d',pt_thresholds), len(mass_thresholds)-1, array.array('d',mass_thresholds))
        self.h_pt_massSD_total = ROOT.TH2D("pt_massSD_total","", len(pt_thresholds)-1, array.array('d',pt_thresholds), len(mass_thresholds)-1, array.array('d',mass_thresholds))
        self.h_pt_massSD_coarse_pass  = ROOT.TH2D("pt_massSD_coarse_pass","",  len(pt_thresholds)-1, array.array('d',pt_thresholds), len(mass_thresholds_coarse)-1, array.array('d',mass_thresholds_coarse))
        self.h_pt_massSD_coarse_total = ROOT.TH2D("pt_massSD_coarse_total","", len(pt_thresholds)-1, array.array('d',pt_thresholds), len(mass_thresholds_coarse)-1, array.array('d',mass_thresholds_coarse))


        for o in [self.h_nFatJets, self.h_nFatJets_withB, self.h_nFatJets_Htagged]:
            self.addObject(o)

        for o in [self.h_pt_mass_pass_2b,self.h_pt_mass_total_2b,self.h_pt_massSD_pass,self.h_pt_massSD_total,self.h_pt_massSD_coarse_pass,self.h_pt_massSD_coarse_total, self.h_pt_mass_pass_1b, self.h_pt_mass_total_1b, self.h_pt_mass_pass_0b, self.h_pt_mass_total_0b]:
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
                #subJet1_bScore = ( abs(subjets[id1].hadronFlavour)==5 ) # will be one if jet is a true b
            if id2>=0:
                subJet2_bScore = subjets[id2].btagDeepB
                #subJet2_bScore = ( abs(subjets[id2].hadronFlavour)==5 )

            if subJet1_bScore>self.btagWP and subJet2_bScore>self.btagWP:
                nFatJets_withB += 1
                self.h_pt_mass_total_2b.Fill(fatjet.pt, fatjet.mass)
                self.h_pt_massSD_total.Fill(fatjet.pt, fatjet.msoftdrop)
                self.h_pt_massSD_coarse_total.Fill(fatjet.pt, fatjet.msoftdrop)

                if fatjet.deepTag_H>self.htagWP:
                    nFatJets_Htagged += 1
                    self.h_pt_mass_pass_2b.Fill(fatjet.pt, fatjet.mass)
                    self.h_pt_massSD_pass.Fill(fatjet.pt, fatjet.msoftdrop)
                    self.h_pt_massSD_coarse_pass.Fill(fatjet.pt, fatjet.msoftdrop)
            elif (subJet1_bScore>self.btagWP + subJet2_bScore>self.btagWP) == 1:
                self.h_pt_mass_total_1b.Fill(fatjet.pt, fatjet.mass)
                if fatjet.deepTag_H>self.htagWP:
                    self.h_pt_mass_pass_1b.Fill(fatjet.pt, fatjet.mass)
            else:
                self.h_pt_mass_total_0b.Fill(fatjet.pt, fatjet.mass)
                if fatjet.deepTag_H>self.htagWP:
                    self.h_pt_mass_pass_0b.Fill(fatjet.pt, fatjet.mass)
                

        bjets = []
        for jet in jets:
            if jet.pt>30 and abs(jet.eta)<2.4 and jet.jetId>0 and jet.btagDeepB > self.btagWP:
                bjets.append(jet)

        # very crude
        nBTag = len(bjets)
        b1 = ROOT.TLorentzVector()
        b2 = ROOT.TLorentzVector()
        mbb = 0
        if nBTag>1:
            b1.SetPtEtaPhiM(bjets[0].pt, bjets[0].eta, bjets[0].phi, 0)
            b2.SetPtEtaPhiM(bjets[1].pt, bjets[1].eta, bjets[1].phi, 0)

            mbb = (b1+b2).M()

        if mbb>90 and mbb<150:
            self.h_nFatJets.Fill(nFatJets)
            self.h_nFatJets_withB.Fill(nFatJets_withB)
            self.h_nFatJets_Htagged.Fill(nFatJets_Htagged)

        #self.h_nFatJets.Fill(nFatJets)
        #self.h_nFatJets_withB.Fill(nFatJets_withB)
        #self.h_nFatJets_Htagged.Fill(nFatJets_Htagged)

        return True

    def endJob(self):
        pass
        #self.eff    = ROOT.TEfficiency(self.h_pt1_passEvents, self.h_pt1_totalEvents)
        #self.addObject(self.eff)


preselection = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_jetId>0&&Jet_btagDeepB>0.4941)>1'
files = sample.files

p=PostProcessor(".", files, cut=preselection,branchsel=None,modules=[TriggerAnalysis()],noOut=True,histFileName="histOut.root",histDirName="plots")

print "Run"

p.run()

h0 = p.histFile.Get("nFatJets")
h1 = p.histFile.Get("nFatJets_withB")
h2 = p.histFile.Get("nFatJets_Htagged")

#print "Tagging efficiency", (h2.GetBinContent(2)+2*h2.GetBinContent(3)+3*h2.GetBinContent(4)+4*h2.GetBinContent(5))/(h1.GetBinContent(2)+2*h1.GetBinContent(3)+3*h1.GetBinContent(4)+4*h1.GetBinContent(5))


## plotting
outFile = p.histFile

pt_thresholds           = [150,200,250,300,400,500,750,1200]
mass_thresholds         = [0,30,60,90,110,130,150,200,250,400]
mass_thresholds_coarse  = [0,45,90,150,200,250,400]
plot_path = '.'

# for usage with the current babies
h_pt_mass_pass_2b  = outFile.Get('pt_mass_pass_2b')
h_pt_mass_total_2b = outFile.Get('pt_mass_total_2b')
h_pt_mass_pass_1b  = outFile.Get('pt_mass_pass_1b')
h_pt_mass_total_1b = outFile.Get('pt_mass_total_1b')
h_pt_mass_pass_0b  = outFile.Get('pt_mass_pass_0b')
h_pt_mass_total_0b = outFile.Get('pt_mass_total_0b')

h_pt_massSD_pass  = outFile.Get('pt_massSD_pass')
h_pt_massSD_total = outFile.Get('pt_massSD_total')
h_pt_massSD_coarse_pass  = outFile.Get('pt_massSD_coarse_pass')
h_pt_massSD_coarse_total = outFile.Get('pt_massSD_coarse_total')

eff_pt_mass_2b = ROOT.TEfficiency(h_pt_mass_pass_2b, h_pt_mass_total_2b)
h_eff_pt_mass_2b = eff_pt_mass_2b.CreateHistogram('eff_pt_mass_2b')
h_eff_pt_mass_2b.SetName('eff_pt_mass_2b')
h_eff_pt_mass_2b = fixUncertainties(eff_pt_mass_2b, h_eff_pt_mass_2b, pt_thresholds, mass_thresholds_coarse)

eff_pt_mass_1b = ROOT.TEfficiency(h_pt_mass_pass_1b, h_pt_mass_total_1b)
h_eff_pt_mass_1b = eff_pt_mass_1b.CreateHistogram('eff_pt_mass_1b')
h_eff_pt_mass_1b.SetName('eff_pt_mass_1b')
h_eff_pt_mass_1b = fixUncertainties(eff_pt_mass_1b, h_eff_pt_mass_1b, pt_thresholds, mass_thresholds_coarse)

eff_pt_mass_0b = ROOT.TEfficiency(h_pt_mass_pass_0b, h_pt_mass_total_0b)
h_eff_pt_mass_0b = eff_pt_mass_0b.CreateHistogram('eff_pt_mass_0b')
h_eff_pt_mass_0b.SetName('eff_pt_mass_0b')
h_eff_pt_mass_0b = fixUncertainties(eff_pt_mass_0b, h_eff_pt_mass_0b, pt_thresholds, mass_thresholds_coarse)

eff_pt_massSD = ROOT.TEfficiency(h_pt_massSD_pass, h_pt_massSD_total)
h_eff_pt_massSD = eff_pt_massSD.CreateHistogram('eff_pt_massSD')
h_eff_pt_massSD.SetName('eff_pt_massSD')
h_eff_pt_massSD = fixUncertainties(eff_pt_massSD, h_eff_pt_massSD, pt_thresholds, mass_thresholds)

eff_pt_massSD_coarse = ROOT.TEfficiency(h_pt_massSD_coarse_pass, h_pt_massSD_coarse_total)
h_eff_pt_massSD_coarse = eff_pt_massSD_coarse.CreateHistogram('eff_pt_massSD_coarse')
h_eff_pt_massSD_coarse.SetName('eff_pt_massSD_coarse')
h_eff_pt_massSD_coarse = fixUncertainties(eff_pt_massSD_coarse, h_eff_pt_massSD_coarse, pt_thresholds, mass_thresholds_coarse)

## 2D
h_eff_pt_mass_2b.GetXaxis().SetNdivisions(712)
h_eff_pt_mass_2b.GetXaxis().SetMoreLogLabels()
h_eff_pt_mass_2b.GetXaxis().SetNoExponent()
h_eff_pt_mass_2b.GetYaxis().SetNdivisions(712)
h_eff_pt_mass_2b.GetYaxis().SetMoreLogLabels()
h_eff_pt_mass_2b.GetYaxis().SetNoExponent()

h_eff_pt_mass_1b.GetXaxis().SetNdivisions(712)
h_eff_pt_mass_1b.GetXaxis().SetMoreLogLabels()
h_eff_pt_mass_1b.GetXaxis().SetNoExponent()
h_eff_pt_mass_1b.GetYaxis().SetNdivisions(712)
h_eff_pt_mass_1b.GetYaxis().SetMoreLogLabels()
h_eff_pt_mass_1b.GetYaxis().SetNoExponent()

h_eff_pt_mass_0b.GetXaxis().SetNdivisions(712)
h_eff_pt_mass_0b.GetXaxis().SetMoreLogLabels()
h_eff_pt_mass_0b.GetXaxis().SetNoExponent()
h_eff_pt_mass_0b.GetYaxis().SetNdivisions(712)
h_eff_pt_mass_0b.GetYaxis().SetMoreLogLabels()
h_eff_pt_mass_0b.GetYaxis().SetNoExponent()

h_eff_pt_massSD.GetXaxis().SetNdivisions(712)
h_eff_pt_massSD.GetXaxis().SetMoreLogLabels()
h_eff_pt_massSD.GetXaxis().SetNoExponent()
h_eff_pt_massSD.GetYaxis().SetNdivisions(712)
h_eff_pt_massSD.GetYaxis().SetMoreLogLabels()
h_eff_pt_massSD.GetYaxis().SetNoExponent()

h_eff_pt_massSD_coarse.GetXaxis().SetNdivisions(712)
h_eff_pt_massSD_coarse.GetXaxis().SetMoreLogLabels()
h_eff_pt_massSD_coarse.GetXaxis().SetNoExponent()
h_eff_pt_massSD_coarse.GetYaxis().SetNdivisions(712)
h_eff_pt_massSD_coarse.GetYaxis().SetMoreLogLabels()
h_eff_pt_massSD_coarse.GetYaxis().SetNoExponent()

writeObjToFile('eff_pt_mass_'+sample.name+'.root', h_eff_pt_mass_2b)
writeObjToFile('eff_pt_mass_'+sample.name+'.root', h_eff_pt_mass_1b, update=True)
writeObjToFile('eff_pt_mass_'+sample.name+'.root', h_eff_pt_mass_0b, update=True)

plot = Plot.fromHisto(name = '2b_pt_mass_'+sample.name, histos = [[ h_eff_pt_mass_2b ]], texX = "p_{T} of FatJet", texY = "Mass (GeV)")
plot.drawOption="colz texte"
plotting.draw2D(
    plot,
    plot_directory = plot_path, #ratio = ratio, 
    logX = True, logY = True, logZ=False,
     zRange = (0,1.05),
)

plot = Plot.fromHisto(name = '1b_pt_mass_'+sample.name, histos = [[ h_eff_pt_mass_1b ]], texX = "p_{T} of FatJet", texY = "Mass (GeV)")
plot.drawOption="colz texte"
plotting.draw2D(
    plot,
    plot_directory = plot_path, #ratio = ratio, 
    logX = True, logY = True, logZ=False,
     zRange = (0,1.05),
)

plot = Plot.fromHisto(name = '0b_pt_mass_'+sample.name, histos = [[ h_eff_pt_mass_0b ]], texX = "p_{T} of FatJet", texY = "Mass (GeV)")
plot.drawOption="colz texte"
plotting.draw2D(
    plot,
    plot_directory = plot_path, #ratio = ratio, 
    logX = True, logY = True, logZ=False,
     zRange = (0,1.05),
)

plot = Plot.fromHisto(name = '2b_pt_massSD_'+sample.name, histos = [[ h_eff_pt_massSD ]], texX = "p_{T} of FatJet", texY = "SD Mass (GeV)")
plot.drawOption="colz texte"
plotting.draw2D(
    plot,
    plot_directory = plot_path, #ratio = ratio, 
    logX = True, logY = True, logZ=False,
     zRange = (0,1.05),
)

plot = Plot.fromHisto(name = '2b_pt_massSD_coarse_'+sample.name, histos = [[ h_eff_pt_massSD_coarse ]], texX = "p_{T} of FatJet", texY = "SD Mass (GeV)")
plot.drawOption="colz texte"
plotting.draw2D(
    plot,
    plot_directory = plot_path, #ratio = ratio, 
    logX = True, logY = True, logZ=False,
     zRange = (0,1.05),
)
