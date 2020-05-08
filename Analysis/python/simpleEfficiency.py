#!/usr/bin/env python
import os, sys
import ROOT
import array
import json
import math

ROOT.PyConfig.IgnoreCommandLineOptions = True

from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from RootTools.core.standard import *
from WH_studies.Tools.u_float import u_float as uf

def hasBit(value,bit):
  """Check if i'th bit is set to 1, i.e. binary of 2^(i-1),
  from the right to the left, starting from position i=0."""
  # https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html#GenPart
  # Gen status flags, stored bitwise, are:
  #    0: isPrompt,                          8: fromHardProcess,
  #    1: isDecayedLeptonHadron,             9: isHardProcessTauDecayProduct,
  #    2: isTauDecayProduct,                10: isDirectHardProcessTauDecayProduct,
  #    3: isPromptTauDecayProduct,          11: fromHardProcessBeforeFSR,
  #    4: isDirectTauDecayProduct,          12: isFirstCopy,
  #    5: isDirectPromptTauDecayProduct,    13: isLastCopy,
  #    6: isDirectHadronDecayProduct,       14: isLastCopyBeforeFSR
  #    7: isHardProcess,
  ###return bin(value)[-bit-1]=='1'
  ###return format(value,'b').zfill(bit+1)[-bit-1]=='1'
  return (value & (1 << bit))>0


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



## Do the nanoAOD-tools stuff
class TaggerAnalysis(Module):
    def __init__(self, btagWP=0.4941, htagWP=0.8, tagger="deepTagMD_HbbvsQCD"):
        self.writeHistFile = True
        self.btagWP = btagWP
        self.htagWP = htagWP
        self.tagger = tagger

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)

        pt_thresholds           = [200,300,400,500,600,2000]

        # 1D hists
        self.h_FatJet_pt_all    = ROOT.TH1F("FatJet_pt_all",    "", len(pt_thresholds)-1, array.array('d',pt_thresholds))
        self.h_FatJet_pt_pass   = ROOT.TH1F("FatJet_pt_pass",   "", len(pt_thresholds)-1, array.array('d',pt_thresholds))

        for o in [self.h_FatJet_pt_all, self.h_FatJet_pt_pass]:
            self.addObject(o)

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

    def hasAncestor(self, p, ancestorPdg, genParts):
        motherIdx = p.genPartIdxMother
        while motherIdx>0:
            if (abs(genParts[motherIdx].pdgId) == ancestorPdg): return True
            motherIdx = genParts[motherIdx].genPartIdxMother
        return False

    def analyze(self, event):
        subjets     = Collection(event, "SubJet")
        fatjets     = Collection(event, "FatJet")
        genparts    = Collection(event, "GenPart")

        # filter out all the Higgs bosons from the generated particles
        Higgs = [ p for p in genparts if (abs(p.pdgId)==25 and hasBit(p.statusFlags,13) ) ] # last copy Ws

        # there should only be one.
        if len(Higgs)>1:
            print "Found more than 1 Higgs. Please check!"
            return False

        nFatJets = len(fatjets)

        # only measure if at least one Higgs boson was found in the generated particles
        nHiggsInFatJet = 0

        if len(Higgs)>0:
            # loop over all FatJets
            for fatjet in fatjets:
                # deltaR matching of the fatjet and the higgs boson
                if self.deltaR(fatjet, Higgs[0]) < 0.4:
                    # that speaks for itself
                    nHiggsInFatJet += 1
                    self.h_FatJet_pt_all.Fill(fatjet.pt)
                    if getattr(fatjet, self.tagger) > self.htagWP:
                        self.h_FatJet_pt_pass.Fill(fatjet.pt)
        
        if nHiggsInFatJet>1:
            print "More than one FatJet with Higgs boson deltaR match. Weird -> please check!"

        return True

    def endJob(self):
        pass
        #self.eff    = ROOT.TEfficiency(self.h_pt1_passEvents, self.h_pt1_totalEvents)
        #self.addObject(self.eff)

if __name__ == "__main__":

    ## Define WH samples
    WH_F17_FullSim = Sample.fromFiles("WH_F17_FullSim", ["/hadoop/cms/store/user/dspitzba/WH_studies/WH_FullSim_JEC.root"], "Events", xSection=123.) # arbitrary x-sec
    WH_F17_FastSim = Sample.fromFiles("WH_F17_FastSim", ["/hadoop/cms/store/user/dspitzba/WH_studies/WH_FastSim_JEC.root"], "Events", xSection=123.) # arbitrary x-sec

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--year",                  dest="year",                  default=2016, type="int",    action="store",      help="Which year?")
    parser.add_option("--tagger",                dest="tagger",                default="deepTagMD_HbbvsQCD",action="store",      help="Which Higgs tagger should be used?")
    parser.add_option("--customWP",              dest="customWP",              default=-1,   type="float",  action="store",      help="Define a custom higgs tagger WP")
    parser.add_option("--fastSim",               dest="fastSim",               default=False,               action="store_true", help="Use FastSim?")
    (options, args) = parser.parse_args()

    ## select proper b-tag WP depending on year.
    if options.year == 2016:
        btagWP = 0.6321
        htagWP = 0.8 # replace!
        sample = S16
    elif options.year == 2017:
        btagWP = 0.4941
        htagWP = 0.8695
        sample = WH_F17_FullSim if not options.fastSim else WH_F17_FastSim
    elif options.year == 2018:
        btagWP = 0.4184
        htagWP = 0.8 # replace!
        sample = A18
    else:
        print "Don't know year %s"%options.year
        btatWP = 1

    if options.customWP > 0:
        htagWP = options.customWP

    # very loose preselection
    preselection = 'nFatJet>0'
    files = sample.files
    
    # this is where the magic happens
    p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[TaggerAnalysis(btagWP, htagWP, options.tagger)], noOut=True, histFileName="histOut.root", histDirName="plots")
    print "Starting the processor"
    p.run()
    
    # get the root histograms from the processor
    h_all   = p.histFile.Get("FatJet_pt_all")
    h_pass  = p.histFile.Get("FatJet_pt_pass")

    # get the efficiency. we use TEfficiency because the uncertainties are correlated, and this is taken into account in this ROOT routine
    eff     = ROOT.TEfficiency(h_pass, h_all)

    # pt thresholds
    pt_thresholds   = [200,300,400,500,600,2000]
    
    # get the efficiencies into a list, and symmetrize the uncertainties
    efficiencies    = [ uf(eff.GetEfficiency(i+1), (eff.GetEfficiencyErrorUp(i+1)+eff.GetEfficiencyErrorLow(i+1))/2) for i in range(len(pt_thresholds)) ] # root bin numbers start with 1 (0 is the underflow bin)
    bin_str = [ "%s-%s"%(pt_thresholds[i], pt_thresholds[i+1]) for i in range(len(pt_thresholds)) if i<len(pt_thresholds)-1 ] + ['>2000'] # also use overflow

    print
    print "| {:15}|{:>17} |".format("pt bin (GeV)", "efficiency")
    print "| "+"-"*33+" |"
    for i, eff in enumerate(efficiencies):
        print "| {:15}|{:6.3f} +/- {:6.3f} |".format(bin_str[i], eff.val, eff.sigma)
    


