import ROOT
import os
import numpy as np
import math
import itertools
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module



class WHObjects(Module):

    def __init__(self, year=2018):
        self.year = year
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Muon_isGoodMuon", "I", lenVar="nMuon")
        self.out.branch("Muon_isVeto", "I", lenVar="nMuon")
        self.out.branch("Electron_isGoodElectron", "I", lenVar="nElectron")
        self.out.branch("Electron_isVeto", "I", lenVar="nElectron")
        self.out.branch("Jet_crossClean", "I", lenVar="nJet")
        self.out.branch("Jet_isGoodJet", "I", lenVar="nJet")
        self.out.branch("Jet_isGoodBJet", "I", lenVar="nJet")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def isGoodJet(self, jet):
        return (jet.pt > 30 and abs(jet.eta)<2.4 and jet.jetId>1)

    def isGoodBJet(self, jet):
        if self.year == 2018:
            threshold = 0.4184
        return (self.isGoodJet(jet) and jet.btagDeepB > threshold)

    def isVetoMuon(self, muon):
        return (muon.looseId and muon.pt>5 and abs(muon.eta)<2.4 and muon.miniPFRelIso_all < 0.2 and abs(muon.dxy)<0.1 and abs(muon.dz)<0.5)

    def isVetoElectron(self, electron):
        return (electron.cutBased>0 and electron.miniPFRelIso_all < 0.2)

    def isGoodMuon(self, muon):
        return (muon.pt > 25 and muon.mediumId and abs(muon.eta)<2.4 and muon.miniPFRelIso_all < 0.1)

    def isGoodElectron(self, electron):
        return (electron.pt > 30 and electron.cutBased >= 3 and abs(electron.eta) < 2.4 and electron.miniPFRelIso_all < 0.1)# and electron.sip3d < 4.0 and abs(electron.dxy) < 0.05 and abs(electron.dz) < 0.1)

    def deltaPhi(self, phi1, phi2):
        dphi = phi2-phi1
        if  dphi > math.pi:
            dphi -= 2.0*math.pi
        if dphi <= -math.pi:
            dphi += 2.0*math.pi
        return abs(dphi)

    def deltaR2(self, l1, l2):
        return self.deltaPhi(l1.phi, l2.phi)**2 + (l1.eta - l2.eta)**2

    def deltaR(self, l1, l2):
        return math.sqrt(self.deltaR2(l1,l2))

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muons       = Collection(event, "Muon")
        electrons   = Collection(event, "Electron")
        photons     = Collection(event, "Photon")
        jets        = Collection(event, "Jet")

        isGoodMuon = []
        isVetoMuon = []
        for mu in muons:
            mu.isGoodMuon   = 1 if self.isGoodMuon(mu) else 0
            mu.isVeto       = 1 if self.isVetoMuon(mu) else 0
            isGoodMuon.append(mu.isGoodMuon)
            isVetoMuon.append(mu.isVeto)
        
        isGoodElectron = []
        isVetoElectron = []
        for el in electrons:
            el.isGoodElectron   = 1 if self.isGoodElectron(el) else 0
            el.isVeto           = 1 if self.isVetoElectron(el) else 0
            isGoodElectron.append(el.isGoodElectron)
            isVetoElectron.append(el.isVeto)

        cleanMaskV  = []
        isGoodJet   = []
        isGoodBJet  = []

        for j in jets:
            isGoodJet.append(1 if self.isGoodJet(j) else 0)
            isGoodBJet.append(1 if self.isGoodBJet(j) else 0)

            cleanMask = 1
            for coll in [electrons, muons]:
                for p in coll:
                    if p.isVeto:
                        if self.deltaR(j, p) < 0.4:
                            cleanMask = 0
            
            cleanMaskV.append(cleanMask)

        self.out.fillBranch("Muon_isGoodMuon", isGoodMuon)
        self.out.fillBranch("Muon_isVeto", isVetoMuon)
        self.out.fillBranch("Electron_isGoodElectron", isGoodElectron)
        self.out.fillBranch("Electron_isVeto", isVetoElectron)
        self.out.fillBranch("Jet_crossClean",  cleanMaskV)
        self.out.fillBranch("Jet_isGoodJet",  isGoodJet)
        self.out.fillBranch("Jet_isGoodBJet",  isGoodBJet)
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

tools = lambda : WHObjects( )
