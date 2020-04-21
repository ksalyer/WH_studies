'''
Some plots for comparing FastSim and FullSim for SUSY signals
This uses the RootTools package to handle samples, make histograms and produce plots

'''

import ROOT

from RootTools.core.standard import *

### 2016
## FullSim samples
#fullSim      = Sample.fromDirectory("FullSim",    "/hadoop/cms/store/user/dspitzba/nanoAOD/SMS_TChiWH_WToLNu_HToBB_mChargino850_mLSP1_TuneCP5_13TeV-madgraphMLM-pythia8__RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/") # original file
fullSim      = Sample.fromFiles("FullSim",    ["/hadoop/cms/store/user/dspitzba/WH_studies/WH_FullSim_JEC.root"])

## FastSim sample, only 850,1 mass point
fastSim      = Sample.fromFiles("FastSim",    ["/hadoop/cms/store/user/dspitzba/WH_studies/WH_FastSim_JEC.root"])

# Apply MET filters
fullSim.setSelectionString("Flag_goodVertices&&Flag_globalSuperTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_ecalBadCalibFilter&&Flag_BadPFMuonFilter&&Flag_BadChargedCandidateFilter&&Flag_ecalBadCalibFilterV2")

fastSim.setSelectionString("Flag_goodVertices&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_ecalBadCalibFilter&&Flag_BadPFMuonFilter&&Flag_BadChargedCandidateFilter&&Flag_ecalBadCalibFilter")

# Select events with one higgs tag (medium WP)
presel  = 'nFatJet>0&&Sum$(FatJet_pt>200&&FatJet_deepTagMD_HbbvsQCD>0.8695)>0'
preselHighPt  = 'nFatJet>0&&Sum$(FatJet_pt>500&&FatJet_deepTagMD_HbbvsQCD>0.8695)>0'

## plots of MET Significance, MT2ll and MT2blbl
h_MSD_reco    = fastSim.get1DHistoFromDraw('FatJet_msoftdrop[0]',       [20,0,200], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
h_MSD_jec     = fastSim.get1DHistoFromDraw('FatJet_msoftdrop_nom[0]',   [20,0,200], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
h_MSD_full    = fullSim.get1DHistoFromDraw('FatJet_msoftdrop[0]',       [20,0,200], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
h_MSD_full_jec = fullSim.get1DHistoFromDraw('FatJet_msoftdrop_nom[0]',       [20,0,200], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')

h_MSD_highPt_reco     = fastSim.get1DHistoFromDraw('FatJet_msoftdrop[0]',       [20,0,200], weightString='genWeight', selectionString=preselHighPt, addOverFlowBin='upper')
h_MSD_highPt_jec      = fastSim.get1DHistoFromDraw('FatJet_msoftdrop_nom[0]',   [20,0,200], weightString='genWeight', selectionString=preselHighPt, addOverFlowBin='upper')
h_MSD_highPt_full     = fullSim.get1DHistoFromDraw('FatJet_msoftdrop[0]',       [20,0,200], weightString='genWeight', selectionString=preselHighPt, addOverFlowBin='upper')
h_MSD_highPt_full_jec = fullSim.get1DHistoFromDraw('FatJet_msoftdrop_nom[0]',   [20,0,200], weightString='genWeight', selectionString=preselHighPt, addOverFlowBin='upper')

h_mass_reco    = fastSim.get1DHistoFromDraw('FatJet_mass[0]',       [20,0,200], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
h_mass_jec     = fastSim.get1DHistoFromDraw('FatJet_mass_nom[0]',   [20,0,200], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
h_mass_full    = fullSim.get1DHistoFromDraw('FatJet_mass[0]',       [20,0,200], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
h_mass_full_jec    = fullSim.get1DHistoFromDraw('FatJet_mass_nom[0]',       [20,0,200], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')

h_FatJet_pt_reco    = fastSim.get1DHistoFromDraw('FatJet_pt[0]',  [20,150,1150], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
h_FatJet_pt_jec     = fastSim.get1DHistoFromDraw('FatJet_pt_nom[0]',  [20,150,1150], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
h_FatJet_pt_full    = fullSim.get1DHistoFromDraw('FatJet_pt[0]',  [20,150,1150], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
h_FatJet_pt_full_jec    = fullSim.get1DHistoFromDraw('FatJet_pt_nom[0]',  [20,150,1150], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')

h_FatJet_score_reco    = fastSim.get1DHistoFromDraw('FatJet_deepTagMD_HbbvsQCD',  [30,0,1], weightString='genWeight', selectionString='nFatJet>0', addOverFlowBin='both')
h_FatJet_score_full    = fullSim.get1DHistoFromDraw('FatJet_deepTagMD_HbbvsQCD',  [30,0,1], weightString='genWeight', selectionString='nFatJet>0', addOverFlowBin='both')

h_FatJet_pt_noB_reco        = fastSim.get1DHistoFromDraw('FatJet_pt',       [20,150,1150], weightString='genWeight', selectionString='SubJet_btagDeepB[FatJet_subJetIdx1]<0.1522&&SubJet_btagDeepB[FatJet_subJetIdx2]<0.1522', addOverFlowBin='upper')
h_FatJet_pt_noB_jec         = fastSim.get1DHistoFromDraw('FatJet_pt_nom',   [20,150,1150], weightString='genWeight', selectionString='SubJet_btagDeepB[FatJet_subJetIdx1]<0.1522&&SubJet_btagDeepB[FatJet_subJetIdx2]<0.1522', addOverFlowBin='upper')
h_FatJet_pt_noB_full        = fullSim.get1DHistoFromDraw('FatJet_pt',       [20,150,1150], weightString='genWeight', selectionString='SubJet_btagDeepB[FatJet_subJetIdx1]<0.1522&&SubJet_btagDeepB[FatJet_subJetIdx2]<0.1522', addOverFlowBin='upper')
h_FatJet_pt_noB_full_jec    = fullSim.get1DHistoFromDraw('FatJet_pt_nom',   [20,150,1150], weightString='genWeight', selectionString='SubJet_btagDeepB[FatJet_subJetIdx1]<0.1522&&SubJet_btagDeepB[FatJet_subJetIdx2]<0.1522', addOverFlowBin='upper')

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

h_N2mass_reco    = fastSim.get1DHistoFromDraw('Max$(GenPart_mass*(abs(GenPart_pdgId)==1000023))',  [100,0,1000], weightString='(1)', selectionString='(1)', addOverFlowBin='upper')
h_N2mass_full    = fullSim.get1DHistoFromDraw('Max$(GenPart_mass*(abs(GenPart_pdgId)==1000023))',  [100,0,1000], weightString='(1)', selectionString='(1)', addOverFlowBin='upper')

h_N1mass_reco    = fastSim.get1DHistoFromDraw('Max$(GenPart_mass*(abs(GenPart_pdgId)==1000022))',  [100,0,1000], weightString='(1)', selectionString='(1)', addOverFlowBin='upper')
h_N1mass_full    = fullSim.get1DHistoFromDraw('Max$(GenPart_mass*(abs(GenPart_pdgId)==1000022))',  [100,0,1000], weightString='(1)', selectionString='(1)', addOverFlowBin='upper')

h_Higgs_pt_reco    = fastSim.get1DHistoFromDraw('GenPart_pt',  [25,0,1500], weightString='genWeight', selectionString='abs(GenPart_pdgId)==25&&GenPart_status==22', addOverFlowBin='upper')
h_Higgs_pt_full    = fullSim.get1DHistoFromDraw('GenPart_pt',  [25,0,1500], weightString='genWeight', selectionString='abs(GenPart_pdgId)==25&&GenPart_status==22', addOverFlowBin='upper')

h_W_pt_reco    = fastSim.get1DHistoFromDraw('GenPart_pt',  [25,0,1500], weightString='genWeight', selectionString='abs(GenPart_pdgId)==24&&GenPart_status==22', addOverFlowBin='upper')
h_W_pt_full    = fullSim.get1DHistoFromDraw('GenPart_pt',  [25,0,1500], weightString='genWeight', selectionString='abs(GenPart_pdgId)==24&&GenPart_status==22', addOverFlowBin='upper')

h_true_b_pt_reco    = fastSim.get1DHistoFromDraw('Jet_pt',  [25,0,1500], weightString='genWeight', selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_hadronFlavour==5', addOverFlowBin='upper')
h_true_b_pt_jec     = fastSim.get1DHistoFromDraw('Jet_pt_nom',  [25,0,1500], weightString='genWeight', selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_hadronFlavour==5', addOverFlowBin='upper')
h_true_b_pt_full    = fullSim.get1DHistoFromDraw('Jet_pt',  [25,0,1500], weightString='genWeight', selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_hadronFlavour==5', addOverFlowBin='upper')

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

h_GenJet_pt_reco    = fastSim.get1DHistoFromDraw('GenJet_pt',     [30,25,1000], weightString='genWeight', selectionString='abs(GenJet_hadronFlavour)==5', addOverFlowBin='upper')
h_GenJet_pt_full    = fullSim.get1DHistoFromDraw('GenJet_pt',     [30,25,1000], weightString='genWeight', selectionString='abs(GenJet_hadronFlavour)==5', addOverFlowBin='upper')

h_GenFatJet_pt_reco    = fastSim.get1DHistoFromDraw('GenJetAK8_pt',     [30,25,1500], weightString='genWeight', selectionString='(1)', addOverFlowBin='upper')
h_GenFatJet_pt_full    = fullSim.get1DHistoFromDraw('GenJetAK8_pt',     [30,25,1500], weightString='genWeight', selectionString='(1)', addOverFlowBin='upper')

h_GenFatJet_mass_reco    = fastSim.get1DHistoFromDraw('GenJetAK8_mass',     [10,25,500], weightString='genWeight', selectionString='(1)', addOverFlowBin='upper')
h_GenFatJet_mass_full    = fullSim.get1DHistoFromDraw('GenJetAK8_mass',     [10,25,500], weightString='genWeight', selectionString='(1)', addOverFlowBin='upper')

h_SV_x_reco    = fastSim.get1DHistoFromDraw('SV_x',     [25,-5,5], weightString='genWeight', selectionString='(1)', addOverFlowBin='both')
h_SV_x_full    = fullSim.get1DHistoFromDraw('SV_x',     [25,-5,5], weightString='genWeight', selectionString='(1)', addOverFlowBin='both')

h_SV_y_reco    = fastSim.get1DHistoFromDraw('SV_y',     [25,-5,5], weightString='genWeight', selectionString='(1)', addOverFlowBin='both')
h_SV_y_full    = fullSim.get1DHistoFromDraw('SV_y',     [25,-5,5], weightString='genWeight', selectionString='(1)', addOverFlowBin='both')

h_SV_z_reco    = fastSim.get1DHistoFromDraw('SV_z',     [25,-15,15], weightString='genWeight', selectionString='(1)', addOverFlowBin='both')
h_SV_z_full    = fullSim.get1DHistoFromDraw('SV_z',     [25,-15,15], weightString='genWeight', selectionString='(1)', addOverFlowBin='both')

## styles
h_MSD_reco.legendText = 'FastSim'
h_MSD_jec.legendText  = 'FastSim, JEC reapplied'
h_MSD_full.legendText = 'FullSim'
h_MSD_full_jec.legendText = 'FullSim, JEC reapplied'
h_MSD_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_MSD_jec.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=True)
h_MSD_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
h_MSD_full_jec.style      = styles.lineStyle(ROOT.kOrange+1,    width=2, errors=True)

h_MSD_highPt_reco.legendText = 'FastSim'
h_MSD_highPt_jec.legendText  = 'FastSim, JEC reapplied'
h_MSD_highPt_full.legendText = 'FullSim'
h_MSD_highPt_full_jec.legendText = 'FullSim, JEC reapplied'
h_MSD_highPt_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_MSD_highPt_jec.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=True)
h_MSD_highPt_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
h_MSD_highPt_full_jec.style      = styles.lineStyle(ROOT.kOrange+1,    width=2, errors=True)

h_mass_reco.legendText = 'FastSim'
h_mass_jec.legendText  = 'FastSim, JEC reapplied'
h_mass_full.legendText = 'FullSim'
h_mass_full_jec.legendText = 'FullSim, JEC reapplied'
h_mass_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_mass_jec.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=True)
h_mass_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
h_mass_full_jec.style      = styles.lineStyle(ROOT.kOrange+1,    width=2, errors=True)

h_FatJet_pt_reco.legendText = 'FastSim'
h_FatJet_pt_jec.legendText  = 'FastSim, JEC reapplied'
h_FatJet_pt_full.legendText = 'FullSim'
h_FatJet_pt_full_jec.legendText = 'FullSim, JEC reapplied'
h_FatJet_pt_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_FatJet_pt_jec.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=True)
h_FatJet_pt_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
h_FatJet_pt_full_jec.style      = styles.lineStyle(ROOT.kOrange+1,    width=2, errors=True)

h_FatJet_score_reco.legendText = 'FastSim'
h_FatJet_score_full.legendText = 'FullSim'
h_FatJet_score_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_FatJet_score_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)

h_FatJet_pt_noB_reco.legendText = 'FastSim'
h_FatJet_pt_noB_jec.legendText  = 'FastSim, JEC reapplied'
h_FatJet_pt_noB_full.legendText = 'FullSim'
h_FatJet_pt_noB_full_jec.legendText = 'FullSim, JEC reapplied'
h_FatJet_pt_noB_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_FatJet_pt_noB_jec.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=True)
h_FatJet_pt_noB_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
h_FatJet_pt_noB_full_jec.style      = styles.lineStyle(ROOT.kOrange+1,    width=2, errors=True)

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

h_N2mass_reco.legendText = 'FastSim'
h_N2mass_full.legendText = 'FullSim'
h_N2mass_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_N2mass_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)

h_N1mass_reco.legendText = 'FastSim'
h_N1mass_full.legendText = 'FullSim'
h_N1mass_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_N1mass_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)

h_Higgs_pt_reco.legendText = 'FastSim'
h_Higgs_pt_full.legendText = 'FullSim'
h_Higgs_pt_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_Higgs_pt_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)

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

h_GenJet_pt_reco.legendText = 'FastSim'
h_GenJet_pt_full.legendText = 'FullSim'
h_GenJet_pt_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_GenJet_pt_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)

h_GenFatJet_pt_reco.legendText = 'FastSim'
h_GenFatJet_pt_full.legendText = 'FullSim'
h_GenFatJet_pt_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_GenFatJet_pt_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)

h_GenFatJet_mass_reco.legendText = 'FastSim'
h_GenFatJet_mass_full.legendText = 'FullSim'
h_GenFatJet_mass_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_GenFatJet_mass_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)

h_SV_x_reco.legendText = 'FastSim'
h_SV_x_full.legendText = 'FullSim'
h_SV_x_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_SV_x_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)

h_SV_y_reco.legendText = 'FastSim'
h_SV_y_full.legendText = 'FullSim'
h_SV_y_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_SV_y_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)

h_SV_z_reco.legendText = 'FastSim'
h_SV_z_full.legendText = 'FullSim'
h_SV_z_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_SV_z_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)

# do the actual plotting

plot_path = './FatJet_FastFull/'

plotting.draw(
    Plot.fromHisto(name = 'mass', histos = [ [h_mass_reco], [h_mass_jec], [h_mass_full], [h_mass_full_jec] ], texX = "M (GeV)", texY = "a.u."),
    plot_directory = plot_path,
    logX = False, logY = False, sorting = False,
    scaling = {1:0, 2:0, 3:0},
    ratio = {'histos': [(0, 2), (1,2), (3,2)], 'texY': 'x / FullSim'},
)

plotting.draw(
    Plot.fromHisto(name = 'MSD', histos = [ [h_MSD_reco], [h_MSD_jec], [h_MSD_full], [h_MSD_full_jec] ], texX = "M_{SD} (GeV)", texY = "a.u."),
    plot_directory = plot_path,
    logX = False, logY = False, sorting = False,
    scaling = {1:0, 2:0, 3:0},
    ratio = {'histos': [(0,2), (1,2), (3,2)], 'texY': 'x / FullSim'},
)

plotting.draw(
    Plot.fromHisto(name = 'MSD_highPt', histos = [ [h_MSD_highPt_reco], [h_MSD_highPt_jec], [h_MSD_highPt_full], [h_MSD_highPt_full_jec] ], texX = "M_{SD} (GeV)", texY = "a.u."),
    plot_directory = plot_path,
    logX = False, logY = False, sorting = False,
    scaling = {1:0, 2:0, 3:0},
    ratio = {'histos': [(0,2), (1,2), (3,2)], 'texY': 'x / FullSim'},
)


plotting.draw(
    Plot.fromHisto(name = 'FatJet_pt', histos = [ [h_FatJet_pt_reco], [h_FatJet_pt_jec], [h_FatJet_pt_full], [h_FatJet_pt_full_jec] ], texX = "p_{T} (GeV)", texY = "a.u."),
    plot_directory = plot_path,
    logX = False, logY = True, sorting = False,
    scaling = {1:0, 2:0, 3:0},
    ratio = {'histos': [(0,2), (1,2), (3,2)], 'texY': 'x / FullSim'},
)

plotting.draw(
    Plot.fromHisto(name = 'FatJet_score', histos = [ [h_FatJet_score_reco], [h_FatJet_score_full] ], texX = "H score", texY = "a.u."),
    plot_directory = plot_path,
    logX = False, logY = True, sorting = False,
    scaling = {1:0},
    ratio = {'histos': [(0,1)], 'texY': 'x / FullSim'},
)

plotting.draw(
    Plot.fromHisto(name = 'FatJet_pt_noB', histos = [ [h_FatJet_pt_noB_reco], [h_FatJet_pt_noB_jec], [h_FatJet_pt_noB_full], [h_FatJet_pt_noB_full_jec] ], texX = "p_{T} (GeV)", texY = "a.u."),
    plot_directory = plot_path,
    logX = False, logY = True, sorting = False,
    scaling = {1:0, 2:0, 3:0},
    ratio = {'histos': [(0,2), (1,2), (3,2)], 'texY': 'x / FullSim'},
)



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
    Plot.fromHisto(name = 'N2_mass', histos = [ [h_N2mass_reco], [h_N2mass_full] ], texX = "M(#Chi_{2}^{0}) (GeV)", texY = "a.u."),
    plot_directory = plot_path,
    logX = False, logY = True, sorting = False,
    scaling = {1:0},
    ratio = {'histos': [(0,1)], 'texY': 'x / FullSim'},
)


plotting.draw(
    Plot.fromHisto(name = 'N1_mass', histos = [ [h_N1mass_reco], [h_N1mass_full] ], texX = "M(#Chi_{1}^{0}) (GeV)", texY = "a.u."),
    plot_directory = plot_path,
    logX = False, logY = True, sorting = False,
    scaling = {1:0},
    ratio = {'histos': [(0,1)], 'texY': 'x / FullSim'},
)

plotting.draw(
    Plot.fromHisto(name = 'Higgs_pt', histos = [ [h_Higgs_pt_reco], [h_Higgs_pt_full] ], texX = "gen-p_{T}(Higgs) (GeV)", texY = "a.u."),
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

plotting.draw(
    Plot.fromHisto(name = 'GenJet_pt', histos = [ [h_GenJet_pt_reco], [h_GenJet_pt_full] ], texX = "p_{T}(Gen-jet) (GeV)", texY = "a.u."),
    plot_directory = plot_path,
    logX = False, logY = True, sorting = False,
    yRange = (200,20000),
    scaling = {1:0},
    ratio = {'histos': [(0,1)], 'texY': 'x / FullSim'},
)

plotting.draw(
    Plot.fromHisto(name = 'GenFatJet_pt', histos = [ [h_GenFatJet_pt_reco], [h_GenFatJet_pt_full] ], texX = "p_{T}(Gen-jet) (GeV)", texY = "a.u."),
    plot_directory = plot_path,
    logX = False, logY = True, sorting = False,
    yRange = (200,20000),
    scaling = {1:0},
    ratio = {'histos': [(0,1)], 'texY': 'x / FullSim'},
)

plotting.draw(
    Plot.fromHisto(name = 'GenFatJet_mass', histos = [ [h_GenFatJet_mass_reco], [h_GenFatJet_mass_full] ], texX = "M (Gen-jet) (GeV)", texY = "a.u."),
    plot_directory = plot_path,
    logX = False, logY = True, sorting = False,
    #yRange = (200,20000),
    scaling = {1:0},
    ratio = {'histos': [(0,1)], 'texY': 'x / FullSim'},
)

plotting.draw(
    Plot.fromHisto(name = 'SV_x', histos = [ [h_SV_x_reco], [h_SV_x_full] ], texX = "x(SV) (cm)", texY = "a.u."),
    plot_directory = plot_path,
    logX = False, logY = True, sorting = False,
    scaling = {1:0},
    ratio = {'histos': [(0,1)], 'texY': 'x / FullSim'},
)

plotting.draw(
    Plot.fromHisto(name = 'SV_y', histos = [ [h_SV_y_reco], [h_SV_y_full] ], texX = "y(SV) (cm)", texY = "a.u."),
    plot_directory = plot_path,
    logX = False, logY = True, sorting = False,
    scaling = {1:0},
    ratio = {'histos': [(0,1)], 'texY': 'x / FullSim'},
)

plotting.draw(
    Plot.fromHisto(name = 'SV_z', histos = [ [h_SV_z_reco], [h_SV_z_full] ], texX = "z(SV) (cm)", texY = "a.u."),
    plot_directory = plot_path,
    logX = False, logY = True, sorting = False,
    scaling = {1:0},
    ratio = {'histos': [(0,1)], 'texY': 'x / FullSim'},
)


