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

## Define QCD samples

QCD_100to200    = Sample.fromDirectory("QCD_100to200", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT100to200_TuneCP5_13TeV-madgraph-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/", "Events", xSection=123.)
QCD_300to500    = Sample.fromDirectory("QCD_300to500", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT300to500_TuneCP5_13TeV-madgraph-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/", "Events", xSection=123.)
QCD_500to700    = Sample.fromDirectory("QCD_500to700", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT500to700_TuneCP5_13TeV-madgraph-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/", "Events", xSection=123.)
QCD_700to1000   = Sample.fromDirectory("QCD_700to1000", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/", "Events", xSection=123.)
QCD_1000to1500  = Sample.fromDirectory("QCD_1000to1500", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/", "Events", xSection=123.)
QCD_1500to2000  = Sample.fromDirectory("QCD_1500to2000", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/", "Events", xSection=123.)
QCD_2000toInf   = Sample.fromDirectory("QCD_2000toInf", "/hadoop/cms/store/user/dspitzba/nanoAOD/QCD_bEnriched_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/", "Events", xSection=123.)

samples = [QCD_100to200]

for s in samples:
    s.normalization = s.getYieldFromDraw("(1)", "genWeight")
    s.weight = lambda sample, event: event.genWeight*sample.xSection*1000/sample.normalziation

#sample = QCD_1000to1500

sample = Sample.combine("QCD_combined", [QCD_100to200,QCD_300to500,QCD_500to700,QCD_700to1000,QCD_1000to1500,QCD_1500to2000,QCD_2000toInf])

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
        mass_thresholds_coarse  = [0,45,90,150,200,250,400]

        # 1D hists
        self.h_nFatJets         = ROOT.TH1F("nFatJets",         "", 5, -0.5, 4.5)
        self.h_nFatJets_withB   = ROOT.TH1F("nFatJets_withB",   "", 5, -0.5, 4.5)
        self.h_nFatJets_Htagged = ROOT.TH1F("nFatJets_Htagged", "", 5, -0.5, 4.5)

        # 2D hists
        self.h_pt_mass_pass  = ROOT.TH2D("pt_mass_pass","",  len(pt_thresholds)-1, array.array('d',pt_thresholds), len(mass_thresholds)-1, array.array('d',mass_thresholds))
        self.h_pt_mass_total = ROOT.TH2D("pt_mass_total","", len(pt_thresholds)-1, array.array('d',pt_thresholds), len(mass_thresholds)-1, array.array('d',mass_thresholds))
        self.h_pt_massSD_pass  = ROOT.TH2D("pt_massSD_pass","",  len(pt_thresholds)-1, array.array('d',pt_thresholds), len(mass_thresholds)-1, array.array('d',mass_thresholds))
        self.h_pt_massSD_total = ROOT.TH2D("pt_massSD_total","", len(pt_thresholds)-1, array.array('d',pt_thresholds), len(mass_thresholds)-1, array.array('d',mass_thresholds))
        self.h_pt_massSD_coarse_pass  = ROOT.TH2D("pt_massSD_coarse_pass","",  len(pt_thresholds)-1, array.array('d',pt_thresholds), len(mass_thresholds_coarse)-1, array.array('d',mass_thresholds_coarse))
        self.h_pt_massSD_coarse_total = ROOT.TH2D("pt_massSD_coarse_total","", len(pt_thresholds)-1, array.array('d',pt_thresholds), len(mass_thresholds_coarse)-1, array.array('d',mass_thresholds_coarse))


        for o in [self.h_nFatJets, self.h_nFatJets_withB, self.h_nFatJets_Htagged]:
            self.addObject(o)

        for o in [self.h_pt_mass_pass,self.h_pt_mass_total,self.h_pt_massSD_pass,self.h_pt_massSD_total,self.h_pt_massSD_coarse_pass,self.h_pt_massSD_coarse_total]:
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
                self.h_pt_mass_total.Fill(fatjet.pt, fatjet.mass)
                self.h_pt_massSD_total.Fill(fatjet.pt, fatjet.msoftdrop)
                self.h_pt_massSD_coarse_total.Fill(fatjet.pt, fatjet.msoftdrop)

                if fatjet.deepTag_H>self.htagWP:
                    nFatJets_Htagged += 1
                    self.h_pt_mass_pass.Fill(fatjet.pt, fatjet.mass)
                    self.h_pt_massSD_pass.Fill(fatjet.pt, fatjet.msoftdrop)
                    self.h_pt_massSD_coarse_pass.Fill(fatjet.pt, fatjet.msoftdrop)

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

h_pt_mass_pass  = outFile.Get('pt_mass_pass')
h_pt_mass_total = outFile.Get('pt_mass_total')
h_pt_massSD_pass  = outFile.Get('pt_massSD_pass')
h_pt_massSD_total = outFile.Get('pt_massSD_total')
h_pt_massSD_coarse_pass  = outFile.Get('pt_massSD_coarse_pass')
h_pt_massSD_coarse_total = outFile.Get('pt_massSD_coarse_total')

eff_pt_mass = ROOT.TEfficiency(h_pt_mass_pass, h_pt_mass_total)
h_eff_pt_mass = eff_pt_mass.CreateHistogram('eff_pt_mass')
h_eff_pt_mass.SetName('eff_pt_mass')
h_eff_pt_mass = fixUncertainties(eff_pt_mass, h_eff_pt_mass, pt_thresholds, mass_thresholds)

eff_pt_massSD = ROOT.TEfficiency(h_pt_massSD_pass, h_pt_massSD_total)
h_eff_pt_massSD = eff_pt_massSD.CreateHistogram('eff_pt_massSD')
h_eff_pt_massSD.SetName('eff_pt_massSD')
h_eff_pt_massSD = fixUncertainties(eff_pt_massSD, h_eff_pt_massSD, pt_thresholds, mass_thresholds)

eff_pt_massSD_coarse = ROOT.TEfficiency(h_pt_massSD_coarse_pass, h_pt_massSD_coarse_total)
h_eff_pt_massSD_coarse = eff_pt_massSD_coarse.CreateHistogram('eff_pt_massSD_coarse')
h_eff_pt_massSD_coarse.SetName('eff_pt_massSD_coarse')
h_eff_pt_massSD_coarse = fixUncertainties(eff_pt_massSD_coarse, h_eff_pt_massSD_coarse, pt_thresholds, mass_thresholds_coarse)

## 2D
h_eff_pt_mass.GetXaxis().SetNdivisions(712)
h_eff_pt_mass.GetXaxis().SetMoreLogLabels()
h_eff_pt_mass.GetXaxis().SetNoExponent()
h_eff_pt_mass.GetYaxis().SetNdivisions(712)
h_eff_pt_mass.GetYaxis().SetMoreLogLabels()
h_eff_pt_mass.GetYaxis().SetNoExponent()

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

plot = Plot.fromHisto(name = 'pt_mass_'+sample.name, histos = [[ h_eff_pt_mass ]], texX = "p_{T} of FatJet", texY = "Mass (GeV)")
plot.drawOption="colz texte"
plotting.draw2D(
    plot,
    plot_directory = plot_path, #ratio = ratio, 
    logX = True, logY = True, logZ=False,
     zRange = (0,1.05),
)

plot = Plot.fromHisto(name = 'pt_massSD_'+sample.name, histos = [[ h_eff_pt_massSD ]], texX = "p_{T} of FatJet", texY = "SD Mass (GeV)")
plot.drawOption="colz texte"
plotting.draw2D(
    plot,
    plot_directory = plot_path, #ratio = ratio, 
    logX = True, logY = True, logZ=False,
     zRange = (0,1.05),
)

plot = Plot.fromHisto(name = 'pt_massSD_coarse_'+sample.name, histos = [[ h_eff_pt_massSD_coarse ]], texX = "p_{T} of FatJet", texY = "SD Mass (GeV)")
plot.drawOption="colz texte"
plotting.draw2D(
    plot,
    plot_directory = plot_path, #ratio = ratio, 
    logX = True, logY = True, logZ=False,
     zRange = (0,1.05),
)
