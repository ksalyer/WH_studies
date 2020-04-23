import ROOT

import glob
from RootTools.core.standard import *

### 2016
## FullSim samples
#fullSim      = Sample.fromDirectory("FullSim",    "/hadoop/cms/store/user/dspitzba/nanoAOD/SMS_TChiWH_WToLNu_HToBB_mChargino850_mLSP1_TuneCP5_13TeV-madgraphMLM-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/") # original file
fullSim      = Sample.fromFiles("FullSim",    glob.glob('/hadoop/cms/store/user/dspitzba/nanoAOD/TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/*.root'))

fullSim.reduceFiles(to=2)

## FastSim inclusive samples (not used here)
#fastSim      = Sample.fromFiles("FastSim",    ["ttdilep_JEC.root"])
fastSim      = Sample.fromFiles("FastSim",    ["/home/users/dspitzba/WH/CMSSW_10_2_9/src/ttdilep_JEC.root"])

fullSim.setSelectionString("Flag_goodVertices&&Flag_globalSuperTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_ecalBadCalibFilter&&Flag_BadPFMuonFilter&&Flag_BadChargedCandidateFilter&&Flag_ecalBadCalibFilterV2")

fastSim.setSelectionString("Flag_goodVertices&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_ecalBadCalibFilter&&Flag_BadPFMuonFilter&&Flag_BadChargedCandidateFilter&&Flag_ecalBadCalibFilter")

'''
Select events with one higgs tag (medium WP)
'''

#presel  = 'nFatJet>0'
presel  = '(Sum$(Electron_pt>25&&abs(Electron_eta)<2.4&&Electron_cutBased>=3&&abs(Electron_miniPFRelIso_all)<0.1)+Sum$(Muon_pt>25&&abs(Muon_eta)<2.4&&Muon_mediumId&&abs(Muon_miniPFRelIso_all)<0.1))>1'
presel += '&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_jetId>0)>1'
presel += '&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_jetId>0&&Jet_btagDeepB>0.4941)>0'

preselHighPt  = 'nFatJet>0&&Sum$(FatJet_pt>500)>0'

## JECs and jet responses
h_profile_JEC_full = fullSim.get1DHistoFromDraw(variableString="FatJet_pt/(FatJet_pt*(1-FatJet_rawFactor)):FatJet_pt", binning=[170, 200, 250, 300, 400, 600, 1000, 1500, 2000], binningIsExplicit=True, isProfile=True, selectionString=presel)
h_profile_JEC_fast = fastSim.get1DHistoFromDraw(variableString="FatJet_corr_JEC:FatJet_pt_nom", binning=[170, 200, 250, 300, 400, 600, 1000, 1500, 2000], binningIsExplicit=True, isProfile=True, selectionString=presel)

h_profile_response_b_full = fullSim.get1DHistoFromDraw(variableString="Jet_pt/GenJet_pt[Jet_genJetIdx]:Jet_pt", binning=[30,50,70,100,130, 170, 200, 250, 300, 400, 600, 1000], binningIsExplicit=True, isProfile=True, selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_hadronFlavour==5&&Jet_genJetIdx>-1')
h_profile_response_b_fast = fastSim.get1DHistoFromDraw(variableString="Jet_pt_nom/GenJet_pt[Jet_genJetIdx]:Jet_pt_nom", binning=[30,50,70,100,130,170, 200, 250, 300, 400, 600, 1000], binningIsExplicit=True, isProfile=True, selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_hadronFlavour==5&&Jet_genJetIdx>-1')

h_profile_response_ISR_full = fullSim.get1DHistoFromDraw(variableString="Jet_pt/GenJet_pt[Jet_genJetIdx]:Jet_pt", binning=[30,50,70,100,130, 170, 200, 250, 300, 400, 600, 1000], binningIsExplicit=True, isProfile=True, selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&!(Jet_hadronFlavour==5)&&Jet_btagDeepB<0.4941&&Jet_genJetIdx>-1')
h_profile_response_ISR_fast = fastSim.get1DHistoFromDraw(variableString="Jet_pt_nom/GenJet_pt[Jet_genJetIdx]:Jet_pt_nom", binning=[30,50,70,100,130,170, 200, 250, 300, 400, 600, 1000], binningIsExplicit=True, isProfile=True, selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&!(Jet_hadronFlavour==5)&&Jet_btagDeepB<0.4941&&Jet_genJetIdx>-1')

## plots of MET Significance, MT2ll and MT2blbl
if False:
    h_MSD_reco    = fastSim.get1DHistoFromDraw('FatJet_msoftdrop[0]',       [20,0,200], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    h_MSD_jec     = fastSim.get1DHistoFromDraw('FatJet_msoftdrop_nom[0]',   [20,0,200], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    h_MSD_full    = fullSim.get1DHistoFromDraw('FatJet_msoftdrop[0]',       [20,0,200], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    
    h_mass_reco    = fastSim.get1DHistoFromDraw('FatJet_mass[0]',       [20,0,200], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    h_mass_jec     = fastSim.get1DHistoFromDraw('FatJet_mass_nom[0]',   [20,0,200], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    h_mass_full    = fullSim.get1DHistoFromDraw('FatJet_mass[0]',       [20,0,200], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    
    h_FatJet_pt_reco    = fastSim.get1DHistoFromDraw('FatJet_pt[0]',  [20,150,1150], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    h_FatJet_pt_jec     = fastSim.get1DHistoFromDraw('FatJet_pt_nom[0]',  [20,150,1150], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    h_FatJet_pt_full    = fullSim.get1DHistoFromDraw('FatJet_pt[0]',  [20,150,1150], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    
    #h_FatJet_pt_noB_reco        = fastSim.get1DHistoFromDraw('FatJet_pt',       [20,150,1150], weightString='genWeight', selectionString='SubJet_btagDeepB[FatJet_subJetIdx1]<0.1522&&SubJet_btagDeepB[FatJet_subJetIdx2]<0.1522', addOverFlowBin='upper')
    #h_FatJet_pt_noB_jec         = fastSim.get1DHistoFromDraw('FatJet_pt_nom',   [20,150,1150], weightString='genWeight', selectionString='SubJet_btagDeepB[FatJet_subJetIdx1]<0.1522&&SubJet_btagDeepB[FatJet_subJetIdx2]<0.1522', addOverFlowBin='upper')
    #h_FatJet_pt_noB_full        = fullSim.get1DHistoFromDraw('FatJet_pt',       [20,150,1150], weightString='genWeight', selectionString='SubJet_btagDeepB[FatJet_subJetIdx1]<0.1522&&SubJet_btagDeepB[FatJet_subJetIdx2]<0.1522', addOverFlowBin='upper')
    
    h_MET_reco    = fastSim.get1DHistoFromDraw('MET_pt',  [25,0,1000], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    h_MET_jec     = fastSim.get1DHistoFromDraw('MET_pt_nom',  [25,0,1000], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    h_MET_full    = fullSim.get1DHistoFromDraw('MET_pt',  [25,0,1000], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    
    h_MET_incl_reco    = fastSim.get1DHistoFromDraw('MET_pt',       [25,0,1000], weightString='genWeight', selectionString='(1)', addOverFlowBin='upper')
    h_MET_incl_jec     = fastSim.get1DHistoFromDraw('MET_pt_nom',   [25,0,1000], weightString='genWeight', selectionString='(1)', addOverFlowBin='upper')
    h_MET_incl_full    = fullSim.get1DHistoFromDraw('MET_pt',       [25,0,1000], weightString='genWeight', selectionString='(1)', addOverFlowBin='upper')
    
    h_MET_coarse_reco    = fastSim.get1DHistoFromDraw('MET_pt',       [0,125,200,300,400,600], binningIsExplicit=True, weightString='genWeight', selectionString='(1)', addOverFlowBin='upper')
    h_MET_coarse_jec     = fastSim.get1DHistoFromDraw('MET_pt_nom',   [0,125,200,300,400,600], binningIsExplicit=True, weightString='genWeight', selectionString='(1)', addOverFlowBin='upper')
    h_MET_coarse_full    = fullSim.get1DHistoFromDraw('MET_pt',       [0,125,200,300,400,600], binningIsExplicit=True, weightString='genWeight', selectionString='(1)', addOverFlowBin='upper')
    
    h_RawMET_reco    = fastSim.get1DHistoFromDraw('RawMET_pt',  [25,0,1000], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    h_RawMET_full    = fullSim.get1DHistoFromDraw('RawMET_pt',  [25,0,1000], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    
    h_GenMET_reco    = fastSim.get1DHistoFromDraw('GenMET_pt',  [25,0,1000], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    h_GenMET_full    = fullSim.get1DHistoFromDraw('GenMET_pt',  [25,0,1000], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    
    h_RawMET_unweighted_reco    = fastSim.get1DHistoFromDraw('RawMET_pt',  [25,0,1000], weightString='(1)', selectionString=presel, addOverFlowBin='upper')
    h_RawMET_unweighted_full    = fullSim.get1DHistoFromDraw('RawMET_pt',  [25,0,1000], weightString='(1)', selectionString=presel, addOverFlowBin='upper')
    
    h_nJet_reco    = fastSim.get1DHistoFromDraw('Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_jetId>0)',  [8,-0.5,7.5], weightString='genWeight', selectionString='(1)', addOverFlowBin='upper')
    h_nJet_full    = fullSim.get1DHistoFromDraw('Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_jetId>0)',  [8,-0.5,7.5], weightString='genWeight', selectionString='(1)', addOverFlowBin='upper')
    
    h_top_pt_reco    = fastSim.get1DHistoFromDraw('GenPart_pt',  [25,0,1500], weightString='genWeight', selectionString='abs(GenPart_pdgId)==6&&GenPart_status==22', addOverFlowBin='upper')
    h_top_pt_full    = fullSim.get1DHistoFromDraw('GenPart_pt',  [25,0,1500], weightString='genWeight', selectionString='abs(GenPart_pdgId)==6&&GenPart_status==22', addOverFlowBin='upper')
    
    h_W_pt_reco    = fastSim.get1DHistoFromDraw('GenPart_pt',  [25,0,1500], weightString='genWeight', selectionString='abs(GenPart_pdgId)==24&&GenPart_status==22', addOverFlowBin='upper')
    h_W_pt_full    = fullSim.get1DHistoFromDraw('GenPart_pt',  [25,0,1500], weightString='genWeight', selectionString='abs(GenPart_pdgId)==24&&GenPart_status==22', addOverFlowBin='upper')
    
    h_true_b_pt_reco    = fastSim.get1DHistoFromDraw('Jet_pt',      [25,0,1500], weightString='genWeight', selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_hadronFlavour==5&&Jet_genJetIdx>-1', addOverFlowBin='upper')
    h_true_b_pt_jec     = fastSim.get1DHistoFromDraw('Jet_pt_nom',  [25,0,1500], weightString='genWeight', selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_hadronFlavour==5&&Jet_genJetIdx>-1', addOverFlowBin='upper')
    h_true_b_pt_full    = fullSim.get1DHistoFromDraw('Jet_pt',      [25,0,1500], weightString='genWeight', selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_hadronFlavour==5&&Jet_genJetIdx>-1', addOverFlowBin='upper')
    
    h_true_b_response_reco    = fastSim.get1DHistoFromDraw('Jet_pt/GenJet_pt[Jet_genJetIdx]',      [25,0,2.5], weightString='genWeight', selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_hadronFlavour==5&&Jet_genJetIdx>-1', addOverFlowBin='upper')
    h_true_b_response_jec     = fastSim.get1DHistoFromDraw('Jet_pt_nom/GenJet_pt[Jet_genJetIdx]',  [25,0,2.5], weightString='genWeight', selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_hadronFlavour==5&&Jet_genJetIdx>-1', addOverFlowBin='upper')
    h_true_b_response_full    = fullSim.get1DHistoFromDraw('Jet_pt/GenJet_pt[Jet_genJetIdx]',      [25,0,2.5], weightString='genWeight', selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_hadronFlavour==5&&Jet_genJetIdx>-1', addOverFlowBin='upper')
    
    
    
    h_btag_pt_reco    = fastSim.get1DHistoFromDraw('Jet_pt',     [25,0,1500], weightString='genWeight', selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_btagDeepB>0.4941', addOverFlowBin='upper')
    h_btag_pt_jec     = fastSim.get1DHistoFromDraw('Jet_pt_nom', [25,0,1500], weightString='genWeight', selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_btagDeepB>0.4941', addOverFlowBin='upper')
    h_btag_pt_full    = fullSim.get1DHistoFromDraw('Jet_pt',     [25,0,1500], weightString='genWeight', selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_btagDeepB>0.4941', addOverFlowBin='upper')
    
    
    h_ISR_pt_reco    = fastSim.get1DHistoFromDraw('Jet_pt',     [25,0,1000], weightString='genWeight', selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&!(Jet_hadronFlavour==5)&&Jet_btagDeepB<0.4941', addOverFlowBin='upper')
    h_ISR_pt_jec     = fastSim.get1DHistoFromDraw('Jet_pt_nom', [25,0,1000], weightString='genWeight', selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&!(Jet_hadronFlavour==5)&&Jet_btagDeepB<0.4941', addOverFlowBin='upper')
    h_ISR_pt_full    = fullSim.get1DHistoFromDraw('Jet_pt',     [25,0,1000], weightString='genWeight', selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&!(Jet_hadronFlavour==5)&&Jet_btagDeepB<0.4941', addOverFlowBin='upper')
    
    h_muon_pt_reco    = fastSim.get1DHistoFromDraw('Muon_pt',     [25,25,700], weightString='genWeight', selectionString='Muon_pt>25&&abs(Muon_eta)<2.4&&Muon_mediumId&&abs(Muon_miniPFRelIso_all)<0.1', addOverFlowBin='upper')
    h_muon_pt_full    = fullSim.get1DHistoFromDraw('Muon_pt',     [25,25,700], weightString='genWeight', selectionString='Muon_pt>25&&abs(Muon_eta)<2.4&&Muon_mediumId&&abs(Muon_miniPFRelIso_all)<0.1', addOverFlowBin='upper')
    
    h_ele_pt_reco    = fastSim.get1DHistoFromDraw('Electron_pt',     [25,25,700], weightString='genWeight', selectionString='Electron_pt>25&&abs(Electron_eta)<2.4&&Electron_cutBased>=3&&abs(Electron_miniPFRelIso_all)<0.1', addOverFlowBin='upper')
    h_ele_pt_full    = fullSim.get1DHistoFromDraw('Electron_pt',     [25,25,700], weightString='genWeight', selectionString='Electron_pt>25&&abs(Electron_eta)<2.4&&Electron_cutBased>=3&&abs(Electron_miniPFRelIso_all)<0.1', addOverFlowBin='upper')
    

## styles
h_profile_JEC_fast.legendText = 'FastSim'
h_profile_JEC_full.legendText = 'FullSim'
h_profile_JEC_fast.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_profile_JEC_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)

h_profile_response_b_fast.legendText = 'FastSim'
h_profile_response_b_full.legendText = 'FullSim'
h_profile_response_b_fast.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_profile_response_b_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)

h_profile_response_ISR_fast.legendText = 'FastSim'
h_profile_response_ISR_full.legendText = 'FullSim'
h_profile_response_ISR_fast.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_profile_response_ISR_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)

if False:
    h_MSD_reco.legendText = 'FastSim'
    h_MSD_jec.legendText  = 'FastSim, JEC reapplied'
    h_MSD_full.legendText = 'FullSim'
    h_MSD_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
    h_MSD_jec.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=True)
    h_MSD_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
    
    h_mass_reco.legendText = 'FastSim'
    h_mass_jec.legendText  = 'FastSim, JEC reapplied'
    h_mass_full.legendText = 'FullSim'
    h_mass_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
    h_mass_jec.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=True)
    h_mass_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
    
    h_FatJet_pt_reco.legendText = 'FastSim'
    h_FatJet_pt_jec.legendText  = 'FastSim, JEC reapplied'
    h_FatJet_pt_full.legendText = 'FullSim'
    h_FatJet_pt_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
    h_FatJet_pt_jec.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=True)
    h_FatJet_pt_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
    
    #h_FatJet_pt_noB_reco.legendText = 'FastSim'
    #h_FatJet_pt_noB_jec.legendText  = 'FastSim, JEC reapplied'
    #h_FatJet_pt_noB_full.legendText = 'FullSim'
    #h_FatJet_pt_noB_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
    #h_FatJet_pt_noB_jec.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=True)
    #h_FatJet_pt_noB_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
    
    h_MET_reco.legendText = 'FastSim'
    h_MET_jec.legendText  = 'FastSim, JEC reapplied'
    h_MET_full.legendText = 'FullSim'
    h_MET_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
    h_MET_jec.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=True)
    h_MET_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
    
    h_MET_incl_reco.legendText = 'FastSim'
    h_MET_incl_jec.legendText  = 'FastSim, JEC reapplied'
    h_MET_incl_full.legendText = 'FullSim'
    h_MET_incl_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
    h_MET_incl_jec.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=True)
    h_MET_incl_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
    
    h_MET_coarse_reco.legendText = 'FastSim'
    h_MET_coarse_jec.legendText  = 'FastSim, JEC reapplied'
    h_MET_coarse_full.legendText = 'FullSim'
    h_MET_coarse_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
    h_MET_coarse_jec.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=True)
    h_MET_coarse_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
    
    h_RawMET_reco.legendText = 'FastSim'
    h_RawMET_full.legendText = 'FullSim'
    h_RawMET_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
    h_RawMET_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
    
    h_GenMET_reco.legendText = 'FastSim'
    h_GenMET_full.legendText = 'FullSim'
    h_GenMET_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
    h_GenMET_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
    
    h_nJet_reco.legendText = 'FastSim'
    h_nJet_full.legendText = 'FullSim'
    h_nJet_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
    h_nJet_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
    
    h_RawMET_unweighted_reco.legendText = 'FastSim'
    h_RawMET_unweighted_full.legendText = 'FullSim'
    h_RawMET_unweighted_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
    h_RawMET_unweighted_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
    
    h_top_pt_reco.legendText = 'FastSim'
    h_top_pt_full.legendText = 'FullSim'
    h_top_pt_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
    h_top_pt_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
    
    h_W_pt_reco.legendText = 'FastSim'
    h_W_pt_full.legendText = 'FullSim'
    h_W_pt_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
    h_W_pt_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
    
    h_true_b_pt_reco.legendText = 'FastSim'
    h_true_b_pt_jec.legendText  = 'FastSim, JEC reapplied'
    h_true_b_pt_full.legendText = 'FullSim'
    h_true_b_pt_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
    h_true_b_pt_jec.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=True)
    h_true_b_pt_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
    
    h_true_b_response_reco.legendText = 'FastSim'
    h_true_b_response_jec.legendText  = 'FastSim, JEC reapplied'
    h_true_b_response_full.legendText = 'FullSim'
    h_true_b_response_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
    h_true_b_response_jec.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=True)
    h_true_b_response_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
    
    
    h_btag_pt_reco.legendText = 'FastSim'
    h_btag_pt_jec.legendText  = 'FastSim, JEC reapplied'
    h_btag_pt_full.legendText = 'FullSim'
    h_btag_pt_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
    h_btag_pt_jec.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=True)
    h_btag_pt_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
    
    
    h_ISR_pt_reco.legendText = 'FastSim'
    h_ISR_pt_jec.legendText  = 'FastSim, JEC reapplied'
    h_ISR_pt_full.legendText = 'FullSim'
    h_ISR_pt_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
    h_ISR_pt_jec.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=True)
    h_ISR_pt_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
    
    h_muon_pt_reco.legendText = 'FastSim'
    h_muon_pt_full.legendText = 'FullSim'
    h_muon_pt_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
    h_muon_pt_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
    
    h_ele_pt_reco.legendText = 'FastSim'
    h_ele_pt_full.legendText = 'FullSim'
    h_ele_pt_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
    h_ele_pt_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
    

plot_path = './FatJet_FastFull_top/'

plotting.draw(
    Plot.fromHisto(name = 'JEC_AK8', histos = [ [h_profile_JEC_fast], [h_profile_JEC_full] ], texX = "p_{T} (AK8) (GeV)", texY = "jet energy correction"),
    plot_directory = plot_path,
    logX = False, logY = False, sorting = False,
    #scaling = {1:0, 2:0},
    ratio = {'histos': [(0, 1)], 'texY': 'x / FullSim', 'yRange':(0.95,1.35)},
)

plotting.draw(
    Plot.fromHisto(name = 'response_b', histos = [ [h_profile_response_b_fast], [h_profile_response_b_full] ], texX = "p_{T} (b-jet) (GeV)", texY = "response"),
    plot_directory = plot_path,
    logX = False, logY = False, sorting = False,
    yRange = (0.9,1.8),
    #scaling = {1:0, 2:0},
    ratio = {'histos': [(0, 1)], 'texY': 'x / FullSim'},
)

plotting.draw(
    Plot.fromHisto(name = 'response_ISR', histos = [ [h_profile_response_ISR_fast], [h_profile_response_ISR_full] ], texX = "p_{T} (light jet) (GeV)", texY = "response"),
    plot_directory = plot_path,
    logX = False, logY = False, sorting = False,
    yRange = (0.9,1.8),
    #scaling = {1:0, 2:0},
    ratio = {'histos': [(0, 1)], 'texY': 'x / FullSim'},
)

if False:
    plotting.draw(
        Plot.fromHisto(name = 'mass', histos = [ [h_mass_reco], [h_mass_jec], [h_mass_full] ], texX = "M (GeV)", texY = "a.u."),
        plot_directory = plot_path,
        logX = False, logY = False, sorting = False,
        scaling = {1:0, 2:0},
        ratio = {'histos': [(0, 2), (1,2)], 'texY': 'x / FullSim'},
    )
    
    plotting.draw(
        Plot.fromHisto(name = 'MSD', histos = [ [h_MSD_reco], [h_MSD_jec], [h_MSD_full] ], texX = "M_{SD} (GeV)", texY = "a.u."),
        plot_directory = plot_path,
        logX = False, logY = False, sorting = False,
        scaling = {1:0, 2:0},
        ratio = {'histos': [(0,2), (1,2)], 'texY': 'x / FullSim'},
    )
    
    plotting.draw(
        Plot.fromHisto(name = 'FatJet_pt', histos = [ [h_FatJet_pt_reco], [h_FatJet_pt_jec], [h_FatJet_pt_full] ], texX = "p_{T} (GeV)", texY = "a.u."),
        plot_directory = plot_path,
        logX = False, logY = True, sorting = False,
        scaling = {1:0, 2:0},
        ratio = {'histos': [(0,2), (1,2)], 'texY': 'x / FullSim'},
    )
    
    #plotting.draw(
    #    Plot.fromHisto(name = 'FatJet_pt_noB', histos = [ [h_FatJet_pt_noB_reco], [h_FatJet_pt_noB_jec], [h_FatJet_pt_noB_full] ], texX = "p_{T} (GeV)", texY = "a.u."),
    #    plot_directory = plot_path,
    #    logX = False, logY = True, sorting = False,
    #    scaling = {1:0, 2:0},
    #    ratio = {'histos': [(0,2), (1,2)], 'texY': 'x / FullSim'},
    #)
    
    
    
    plotting.draw(
        Plot.fromHisto(name = 'MET_pt', histos = [ [h_MET_reco], [h_MET_jec], [h_MET_full] ], texX = "p_{T}^{miss} (GeV)", texY = "a.u."),
        plot_directory = plot_path,
        logX = False, logY = True, sorting = False,
        scaling = {1:0, 2:0},
        ratio = {'histos': [(0,2), (1,2)], 'texY': 'x / FullSim'},
    )
    
    plotting.draw(
        Plot.fromHisto(name = 'MET_pt_incl', histos = [ [h_MET_incl_reco], [h_MET_incl_jec], [h_MET_incl_full] ], texX = "p_{T}^{miss} (GeV)", texY = "a.u."),
        plot_directory = plot_path,
        logX = False, logY = True, sorting = False,
        scaling = {1:0, 2:0},
        ratio = {'histos': [(0,2), (1,2)], 'texY': 'x / FullSim'},
    )
    
    plotting.draw(
        Plot.fromHisto(name = 'MET_pt_coarse', histos = [ [h_MET_coarse_reco], [h_MET_coarse_jec], [h_MET_coarse_full] ], texX = "p_{T}^{miss} (GeV)", texY = "a.u."),
        plot_directory = plot_path,
        logX = False, logY = True, sorting = False,
        scaling = {1:0, 2:0},
        ratio = {'histos': [(0,2), (1,2)], 'texY': 'x / FullSim'},
    )
    
    plotting.draw(
        Plot.fromHisto(name = 'RawMET_pt', histos = [ [h_RawMET_reco], [h_RawMET_full] ], texX = "p_{T}^{miss} (GeV)", texY = "a.u."),
        plot_directory = plot_path,
        logX = False, logY = True, sorting = False,
        scaling = {1:0},
        ratio = {'histos': [(0,1)], 'texY': 'x / FullSim'},
    )
    
    plotting.draw(
        Plot.fromHisto(name = 'GenMET_pt', histos = [ [h_GenMET_reco], [h_GenMET_full] ], texX = "p_{T}^{miss} (GeV)", texY = "a.u."),
        plot_directory = plot_path,
        logX = False, logY = True, sorting = False,
        scaling = {1:0},
        ratio = {'histos': [(0,1)], 'texY': 'x / FullSim'},
    )
    
    
    plotting.draw(
        Plot.fromHisto(name = 'RawMET_pt_unweighted', histos = [ [h_RawMET_unweighted_reco], [h_RawMET_unweighted_full] ], texX = "p_{T}^{miss} (GeV)", texY = "a.u."),
        plot_directory = plot_path,
        logX = False, logY = True, sorting = False,
        scaling = {1:0},
        ratio = {'histos': [(0,1)], 'texY': 'x / FullSim'},
    )
    
    plotting.draw(
        Plot.fromHisto(name = 'nJet', histos = [ [h_nJet_reco], [h_nJet_full] ], texX = "N_{jet}", texY = "a.u."),
        plot_directory = plot_path,
        logX = False, logY = True, sorting = False,
        scaling = {1:0},
        ratio = {'histos': [(0,1)], 'texY': 'x / FullSim'},
    )
    
    plotting.draw(
        Plot.fromHisto(name = 'top_pt', histos = [ [h_top_pt_reco], [h_top_pt_full] ], texX = "gen-p_{T}(top) (GeV)", texY = "a.u."),
        plot_directory = plot_path,
        logX = False, logY = True, sorting = False,
        scaling = {1:0},
        ratio = {'histos': [(0,1)], 'texY': 'x / FullSim'},
    )
    
    plotting.draw(
        Plot.fromHisto(name = 'W_pt', histos = [ [h_W_pt_reco], [h_W_pt_full] ], texX = "gen-p_{T}(W) (GeV)", texY = "a.u."),
        plot_directory = plot_path,
        logX = False, logY = True, sorting = False,
        scaling = {1:0},
        ratio = {'histos': [(0,1)], 'texY': 'x / FullSim'},
    )
    
    plotting.draw(
        Plot.fromHisto(name = 'true_b_pt', histos = [ [h_true_b_pt_reco], [h_true_b_pt_jec], [h_true_b_pt_full] ], texX = "p_{T}(true b-jet) (GeV)", texY = "a.u."),
        plot_directory = plot_path,
        logX = False, logY = True, sorting = False,
        scaling = {1:0, 2:0},
        ratio = {'histos': [(0,2), (1,2)], 'texY': 'x / FullSim'},
    )
    
    plotting.draw(
        Plot.fromHisto(name = 'true_b_response', histos = [ [h_true_b_response_reco], [h_true_b_response_jec], [h_true_b_response_full] ], texX = " true b-jet response", texY = "a.u."),
        plot_directory = plot_path,
        logX = False, logY = True, sorting = False,
        scaling = {1:0, 2:0},
        ratio = {'histos': [(0,2), (1,2)], 'texY': 'x / FullSim'},
    )
    
    plotting.draw(
        Plot.fromHisto(name = 'btag_pt', histos = [ [h_btag_pt_reco], [h_btag_pt_jec], [h_btag_pt_full] ], texX = "p_{T}(b-tag) (GeV)", texY = "a.u."),
        plot_directory = plot_path,
        logX = False, logY = True, sorting = False,
        scaling = {1:0, 2:0},
        ratio = {'histos': [(0,2), (1,2)], 'texY': 'x / FullSim'},
    )
    
    
    plotting.draw(
        Plot.fromHisto(name = 'ISR_pt', histos = [ [h_ISR_pt_reco], [h_ISR_pt_jec], [h_ISR_pt_full] ], texX = "p_{T}(ISR) (GeV)", texY = "a.u."),
        plot_directory = plot_path,
        logX = False, logY = True, sorting = False,
        scaling = {1:0, 2:0},
        ratio = {'histos': [(0,2), (1,2)], 'texY': 'x / FullSim'},
    )
    
    plotting.draw(
        Plot.fromHisto(name = 'Muon_pt', histos = [ [h_muon_pt_reco], [h_muon_pt_full] ], texX = "p_{T}(mu) (GeV)", texY = "a.u."),
        plot_directory = plot_path,
        logX = False, logY = True, sorting = False,
        scaling = {1:0},
        ratio = {'histos': [(0,1)], 'texY': 'x / FullSim'},
    )
    
    plotting.draw(
        Plot.fromHisto(name = 'Electron_pt', histos = [ [h_ele_pt_reco], [h_ele_pt_full] ], texX = "p_{T}(ele) (GeV)", texY = "a.u."),
        plot_directory = plot_path,
        logX = False, logY = True, sorting = False,
        scaling = {1:0},
        ratio = {'histos': [(0,1)], 'texY': 'x / FullSim'},
    )
    
