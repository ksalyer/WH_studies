import ROOT

import glob
from RootTools.core.standard import *

#sampleName = "TChiWH_350_100_a18"
sampleName = "TChiWH_750_1_s16"

### 2018
## FullSim samples
fullSim      = Sample.fromFiles("FullSim",    ["%s_Full.root"%sampleName])
#fullSim      = Sample.fromFiles("FullSim",    ["/hadoop/cms/store/user/dspitzba/WH_studies/WH_FullSim_JEC.root"])

fastSim      = Sample.fromFiles("FastSim",    ["%s_Fast.root"%sampleName])
#fastSim      = Sample.fromFiles("FastSim",    ["/hadoop/cms/store/user/dspitzba/WH_studies/WH_FastSim_JEC.root"])

fullSim.setSelectionString("Flag_goodVertices&&Flag_globalSuperTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_BadPFMuonFilter")
fastSim.setSelectionString("Flag_goodVertices&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_BadPFMuonFilter")

'''
Select events with one higgs tag (medium WP)
'''

presel  = 'nFatJet>0'
#presel  = '(Sum$(Electron_pt>25&&abs(Electron_eta)<2.4&&Electron_cutBased>=3&&abs(Electron_miniPFRelIso_all)<0.1)+Sum$(Muon_pt>25&&abs(Muon_eta)<2.4&&Muon_mediumId&&abs(Muon_miniPFRelIso_all)<0.1))>1'
#presel += '&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_jetId>0)>1'
#presel += '&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_jetId>0&&Jet_btagDeepB>0.4941)>0'

preselHighPt  = 'nFatJet>0&&Sum$(FatJet_pt>500)>0'

spuriousJetVeto = 'Sum$(Jet_genJetIdx<0&&Jet_chHEF<0.1)==0' # veto events that have unmached jets with charged hadron energy fraction less than 10%

#presel = 'nFatJet>0'
#presel += '&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_jetId>0)>1'

## JECs and jet responses
h_profile_Fat_full = fullSim.get1DHistoFromDraw(variableString="FatJet_pt/GenJetAK8_pt[FatJet_genJetAK8Idx]:GenJetAK8_pt[FatJet_genJetAK8Idx]", binning=[170, 200, 250, 350, 500, 1000], binningIsExplicit=True, isProfile=True, selectionString=presel+'&&FatJet_subJetIdx1>0&&SubJet_btagDeepB[FatJet_subJetIdx1]>0.1522&&FatJet_genJetAK8Idx>-1')
h_profile_Fat_full_JESdown = fullSim.get1DHistoFromDraw(variableString="FatJet_pt_jesTotalDown/GenJetAK8_pt[FatJet_genJetAK8Idx]:GenJetAK8_pt[FatJet_genJetAK8Idx]", binning=[170, 200, 250, 350, 500, 1000], binningIsExplicit=True, isProfile=True, selectionString=presel+'&&FatJet_subJetIdx1>0&&SubJet_btagDeepB[FatJet_subJetIdx1]>0.1522&&FatJet_genJetAK8Idx>-1')
h_profile_Fat_full_JESup = fullSim.get1DHistoFromDraw(variableString="FatJet_pt_jesTotalUp/GenJetAK8_pt[FatJet_genJetAK8Idx]:GenJetAK8_pt[FatJet_genJetAK8Idx]", binning=[170, 200, 250, 350, 500, 1000], binningIsExplicit=True, isProfile=True, selectionString=presel+'&&FatJet_subJetIdx1>0&&SubJet_btagDeepB[FatJet_subJetIdx1]>0.1522&&FatJet_genJetAK8Idx>-1')
h_profile_Fat_fast = fastSim.get1DHistoFromDraw(variableString="FatJet_pt_nom/GenJetAK8_pt[FatJet_genJetAK8Idx]:GenJetAK8_pt[FatJet_genJetAK8Idx]", binning=[170, 200, 250, 350, 500, 1000], binningIsExplicit=True, isProfile=True, selectionString=presel+'&&FatJet_subJetIdx1>0&&SubJet_btagDeepB[FatJet_subJetIdx1]>0.1522&&FatJet_genJetAK8Idx>-1')
h_profile_Fat_fast_JESup = fastSim.get1DHistoFromDraw(variableString="FatJet_pt_jesTotalUp/GenJetAK8_pt[FatJet_genJetAK8Idx]:GenJetAK8_pt[FatJet_genJetAK8Idx]", binning=[170, 200, 250, 350, 500, 1000], binningIsExplicit=True, isProfile=True, selectionString=presel+'&&FatJet_subJetIdx1>0&&SubJet_btagDeepB[FatJet_subJetIdx1]>0.1522&&FatJet_genJetAK8Idx>-1')
h_profile_Fat_fast_JESdown = fastSim.get1DHistoFromDraw(variableString="FatJet_pt_jesTotalDown/GenJetAK8_pt[FatJet_genJetAK8Idx]:GenJetAK8_pt[FatJet_genJetAK8Idx]", binning=[170, 200, 250, 350, 500, 1000], binningIsExplicit=True, isProfile=True, selectionString=presel+'&&FatJet_subJetIdx1>0&&SubJet_btagDeepB[FatJet_subJetIdx1]>0.1522&&FatJet_genJetAK8Idx>-1')

h_profile2D_Fat_full = fullSim.get2DHistoFromDraw(variableString="FatJet_pt/GenJetAK8_pt[FatJet_genJetAK8Idx]:GenJetAK8_pt[FatJet_genJetAK8Idx]:FatJet_eta", binning=[[-2.4,-1.5,0.,1.5,2.4],[170, 250, 400, 1000]], binningIsExplicit=True, isProfile='s', selectionString=presel+'&&FatJet_genJetAK8Idx>-1')
h_profile2D_Fat_fast = fullSim.get2DHistoFromDraw(variableString="FatJet_pt_nom/GenJetAK8_pt[FatJet_genJetAK8Idx]:GenJetAK8_pt[FatJet_genJetAK8Idx]:FatJet_eta", binning=[[-2.4,-1.5,0.,1.5,2.4],[170, 250, 400, 1000]], binningIsExplicit=True, isProfile='s', selectionString=presel+'&&FatJet_genJetAK8Idx>-1')

h_profile_response_MET_full = fullSim.get1DHistoFromDraw(variableString="MET_pt_nom/GenMET_pt:GenMET_pt", binning=[50,125,200,300,400, 600], binningIsExplicit=True, isProfile=True, selectionString='(1)&&'+spuriousJetVeto)
h_profile_response_MET_fast = fastSim.get1DHistoFromDraw(variableString="MET_pt_nom/GenMET_pt:GenMET_pt", binning=[50,125,200,300,400, 600], binningIsExplicit=True, isProfile=True, selectionString='(1)&&'+spuriousJetVeto)
h_profile_response_MET_fast_JESdown = fastSim.get1DHistoFromDraw(variableString="MET_pt_jesTotalUp/GenMET_pt:GenMET_pt", binning=[50,125,200,300,400, 600], binningIsExplicit=True, isProfile=True, selectionString='(1)&&'+spuriousJetVeto)
h_profile_response_MET_fast_JESup = fastSim.get1DHistoFromDraw(variableString="MET_pt_jesTotalDown/GenMET_pt:GenMET_pt", binning=[50,125,200,300,400, 600], binningIsExplicit=True, isProfile=True, selectionString='(1)&&'+spuriousJetVeto)

h_profile_response_all_full = fullSim.get1DHistoFromDraw(variableString="Jet_pt/GenJet_pt[Jet_genJetIdx]:GenJet_pt[Jet_genJetIdx]", binning=[30,50,70,100,130, 170, 200, 250, 300, 400, 600, 1000], binningIsExplicit=True, isProfile=True, selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_genJetIdx>-1')
h_profile_response_all_fast = fastSim.get1DHistoFromDraw(variableString="Jet_pt/GenJet_pt[Jet_genJetIdx]:GenJet_pt[Jet_genJetIdx]", binning=[30,50,70,100,130,170, 200, 250, 300, 400, 600, 1000], binningIsExplicit=True, isProfile=True, selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_genJetIdx>-1')
h_profile_response_all_fast_JEC = fastSim.get1DHistoFromDraw(variableString="Jet_pt_nom/GenJet_pt[Jet_genJetIdx]:GenJet_pt[Jet_genJetIdx]", binning=[30,50,70,100,130,170, 200, 250, 300, 400, 600, 1000], binningIsExplicit=True, isProfile=True, selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_genJetIdx>-1')
h_profile_response_all_fast_JESdown = fastSim.get1DHistoFromDraw(variableString="Jet_pt_jesTotalDown/GenJet_pt[Jet_genJetIdx]:GenJet_pt[Jet_genJetIdx]", binning=[30,50,70,100,130,170, 200, 250, 300, 400, 600, 1000], binningIsExplicit=True, isProfile=True, selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_genJetIdx>-1')
h_profile_response_all_fast_JESup = fastSim.get1DHistoFromDraw(variableString="Jet_pt_jesTotalUp/GenJet_pt[Jet_genJetIdx]:GenJet_pt[Jet_genJetIdx]", binning=[30,50,70,100,130,170, 200, 250, 300, 400, 600, 1000], binningIsExplicit=True, isProfile=True, selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_genJetIdx>-1')

h_profile_response_b_full = fullSim.get1DHistoFromDraw(variableString="Jet_pt/GenJet_pt[Jet_genJetIdx]:GenJet_pt[Jet_genJetIdx]", binning=[30,50,70,100,130, 170, 200, 250, 300, 400, 600, 1000], binningIsExplicit=True, isProfile=True, selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_hadronFlavour==5&&Jet_genJetIdx>-1')
h_profile_response_b_fast = fastSim.get1DHistoFromDraw(variableString="Jet_pt/GenJet_pt[Jet_genJetIdx]:GenJet_pt[Jet_genJetIdx]", binning=[30,50,70,100,130,170, 200, 250, 300, 400, 600, 1000], binningIsExplicit=True, isProfile=True, selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_hadronFlavour==5&&Jet_genJetIdx>-1')
h_profile_response_b_fast_JEC = fastSim.get1DHistoFromDraw(variableString="Jet_pt_nom/GenJet_pt[Jet_genJetIdx]:GenJet_pt[Jet_genJetIdx]", binning=[30,50,70,100,130,170, 200, 250, 300, 400, 600, 1000], binningIsExplicit=True, isProfile=True, selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_hadronFlavour==5&&Jet_genJetIdx>-1')
h_profile_response_b_fast_JESdown = fastSim.get1DHistoFromDraw(variableString="Jet_pt_jesTotalDown/GenJet_pt[Jet_genJetIdx]:GenJet_pt[Jet_genJetIdx]", binning=[30,50,70,100,130,170, 200, 250, 300, 400, 600, 1000], binningIsExplicit=True, isProfile=True, selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_hadronFlavour==5&&Jet_genJetIdx>-1')
h_profile_response_b_fast_JESup = fastSim.get1DHistoFromDraw(variableString="Jet_pt_jesTotalUp/GenJet_pt[Jet_genJetIdx]:GenJet_pt[Jet_genJetIdx]", binning=[30,50,70,100,130,170, 200, 250, 300, 400, 600, 1000], binningIsExplicit=True, isProfile=True, selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&Jet_hadronFlavour==5&&Jet_genJetIdx>-1')

h_profile_response_ISR_full = fullSim.get1DHistoFromDraw(variableString="Jet_pt/GenJet_pt[Jet_genJetIdx]:GenJet_pt[Jet_genJetIdx]", binning=[30,50,70,100,130, 170, 200, 250, 300, 400, 600, 1000], binningIsExplicit=True, isProfile=True, selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&!(Jet_hadronFlavour==5)&&Jet_btagDeepB<0.4941&&Jet_genJetIdx>-1')
h_profile_response_ISR_fast = fastSim.get1DHistoFromDraw(variableString="Jet_pt/GenJet_pt[Jet_genJetIdx]:GenJet_pt[Jet_genJetIdx]", binning=[30,50,70,100,130,170, 200, 250, 300, 400, 600, 1000], binningIsExplicit=True, isProfile=True, selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&!(Jet_hadronFlavour==5)&&Jet_btagDeepB<0.4941&&Jet_genJetIdx>-1')
h_profile_response_ISR_fast_JEC = fastSim.get1DHistoFromDraw(variableString="Jet_pt_nom/GenJet_pt[Jet_genJetIdx]:GenJet_pt[Jet_genJetIdx]", binning=[30,50,70,100,130,170, 200, 250, 300, 400, 600, 1000], binningIsExplicit=True, isProfile=True, selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&!(Jet_hadronFlavour==5)&&Jet_btagDeepB<0.4941&&Jet_genJetIdx>-1')
h_profile_response_ISR_fast_JESdown = fastSim.get1DHistoFromDraw(variableString="Jet_pt_jesTotalDown/GenJet_pt[Jet_genJetIdx]:GenJet_pt[Jet_genJetIdx]", binning=[30,50,70,100,130,170, 200, 250, 300, 400, 600, 1000], binningIsExplicit=True, isProfile=True, selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&!(Jet_hadronFlavour==5)&&Jet_btagDeepB<0.4941&&Jet_genJetIdx>-1')
h_profile_response_ISR_fast_JESup = fastSim.get1DHistoFromDraw(variableString="Jet_pt_jesTotalUp/GenJet_pt[Jet_genJetIdx]:GenJet_pt[Jet_genJetIdx]", binning=[30,50,70,100,130,170, 200, 250, 300, 400, 600, 1000], binningIsExplicit=True, isProfile=True, selectionString='Jet_pt>0&&abs(Jet_eta)<2.4&&Jet_jetId&&!(Jet_hadronFlavour==5)&&Jet_btagDeepB<0.4941&&Jet_genJetIdx>-1')

if True:

    h_MET_reco    = fastSim.get1DHistoFromDraw('MET_pt',  [50,75,100,125,150,200,250,300,350,400,600],binningIsExplicit=True, weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    h_MET_jec     = fastSim.get1DHistoFromDraw('MET_pt_nom',  [50,75,100,125,150,200,250,300,350,400,600],binningIsExplicit=True, weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    h_MET_JESup   = fastSim.get1DHistoFromDraw('MET_pt_jesTotalUp',  [50,75,100,125,150,200,250,300,350,400,600],binningIsExplicit=True, weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    h_MET_JESdown = fastSim.get1DHistoFromDraw('MET_pt_jesTotalDown',  [50,75,100,125,150,200,250,300,350,400,600],binningIsExplicit=True, weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    h_MET_full    = fullSim.get1DHistoFromDraw('MET_pt',  [50,75,100,125,150,200,250,300,350,400,600],binningIsExplicit=True, weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    
    h_MET_incl_reco    = fastSim.get1DHistoFromDraw('MET_pt_nom',   [25,0,1000], weightString='genWeight', selectionString='(1)', addOverFlowBin='upper')
    h_MET_incl_jec     = fastSim.get1DHistoFromDraw('MET_pt_nom',   [25,0,1000], weightString='genWeight', selectionString='(1)&&'+spuriousJetVeto, addOverFlowBin='upper')
    h_MET_incl_JESup   = fastSim.get1DHistoFromDraw('MET_pt_jesTotalUp',   [25,0,1000], weightString='genWeight', selectionString='(1)&&'+spuriousJetVeto, addOverFlowBin='upper')
    h_MET_incl_JESdown = fastSim.get1DHistoFromDraw('MET_pt_jesTotalDown',   [25,0,1000], weightString='genWeight', selectionString='(1)&&'+spuriousJetVeto, addOverFlowBin='upper')
    h_MET_incl_full    = fullSim.get1DHistoFromDraw('MET_pt',       [25,0,1000], weightString='genWeight', selectionString='(1)', addOverFlowBin='upper')
    
    h_MET_coarse_reco    = fastSim.get1DHistoFromDraw('MET_pt',       [0,125,200,300,400,600], binningIsExplicit=True, weightString='genWeight', selectionString='(1)', addOverFlowBin='upper')
    h_MET_coarse_jec     = fastSim.get1DHistoFromDraw('MET_pt_nom',   [0,125,200,300,400,600], binningIsExplicit=True, weightString='genWeight', selectionString='(1)', addOverFlowBin='upper')
    h_MET_coarse_full    = fullSim.get1DHistoFromDraw('MET_pt',       [0,125,200,300,400,600], binningIsExplicit=True, weightString='genWeight', selectionString='(1)', addOverFlowBin='upper')
    
    h_RawMET_reco    = fastSim.get1DHistoFromDraw('RawMET_pt',  [25,0,1000], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    h_RawMET_full    = fullSim.get1DHistoFromDraw('RawMET_pt',  [25,0,1000], weightString='genWeight', selectionString=presel, addOverFlowBin='upper')
    
    h_GenMET_reco    = fastSim.get1DHistoFromDraw('GenMET_pt',  [25,0,1000], weightString='genWeight', selectionString='(1)', addOverFlowBin='upper')
    h_GenMET_full    = fullSim.get1DHistoFromDraw('GenMET_pt',  [25,0,1000], weightString='genWeight', selectionString='(1)', addOverFlowBin='upper')
    
    h_RawMET_unweighted_reco    = fastSim.get1DHistoFromDraw('RawMET_pt',  [25,0,1000], weightString='(1)', selectionString=presel, addOverFlowBin='upper')
    h_RawMET_unweighted_full    = fullSim.get1DHistoFromDraw('RawMET_pt',  [25,0,1000], weightString='(1)', selectionString=presel, addOverFlowBin='upper')


## styles
h_profile_response_MET_fast.legendText = 'FastSim'
h_profile_response_MET_full.legendText = 'FullSim'
h_profile_response_MET_fast.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_profile_response_MET_fast_JESup.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=False, dashed=True)
h_profile_response_MET_fast_JESdown.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=False, dashed=True)
h_profile_response_MET_full.style      = styles.lineStyle(ROOT.kBlue+1,   width=2, errors=True)

h_profile_Fat_fast.legendText = 'FastSim'
h_profile_Fat_full.legendText = 'FullSim'
h_profile_Fat_fast.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_profile_Fat_fast_JESdown.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=False, dashed=True)
h_profile_Fat_fast_JESup.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=False, dashed=True)
h_profile_Fat_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)
h_profile_Fat_full_JESdown.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=False, dashed=True)
h_profile_Fat_full_JESup.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=False, dashed=True)

h_profile_response_all_fast.legendText = 'FastSim'
h_profile_response_all_fast_JEC.legendText = 'FastSim, re-JEC'
h_profile_response_all_full.legendText = 'FullSim'
h_profile_response_all_fast.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_profile_response_all_fast_JEC.style      = styles.lineStyle(ROOT.kOrange+1,   width=2, errors=True)
h_profile_response_all_fast_JESup.style      = styles.lineStyle(ROOT.kOrange+1,   width=2, errors=False, dashed=True)
h_profile_response_all_fast_JESdown.style      = styles.lineStyle(ROOT.kOrange+1,   width=2, errors=False, dashed=True)
h_profile_response_all_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)


h_profile_response_b_fast.legendText = 'FastSim'
h_profile_response_b_fast_JEC.legendText = 'FastSim, re-JEC'
h_profile_response_b_full.legendText = 'FullSim'
h_profile_response_b_fast.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_profile_response_b_fast_JEC.style      = styles.lineStyle(ROOT.kOrange+1,   width=2, errors=True)
h_profile_response_b_fast_JESdown.style      = styles.lineStyle(ROOT.kOrange+1,   width=2, errors=False, dashed=True)
h_profile_response_b_fast_JESup.style      = styles.lineStyle(ROOT.kOrange+1,   width=2, errors=False, dashed=True)
h_profile_response_b_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)

h_profile_response_ISR_fast.legendText = 'FastSim'
h_profile_response_ISR_fast_JEC.legendText = 'FastSim, re-JEC'
h_profile_response_ISR_full.legendText = 'FullSim'
h_profile_response_ISR_fast.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_profile_response_ISR_fast_JEC.style      = styles.lineStyle(ROOT.kOrange+1,   width=2, errors=True)
h_profile_response_ISR_fast_JESdown.style      = styles.lineStyle(ROOT.kOrange+1,   width=2, errors=False, dashed=True)
h_profile_response_ISR_fast_JESup.style      = styles.lineStyle(ROOT.kOrange+1,   width=2, errors=False, dashed=True)
h_profile_response_ISR_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)

h_MET_reco.legendText = 'FastSim'
h_MET_jec.legendText  = 'FastSim'
h_MET_full.legendText = 'FullSim'
h_MET_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_MET_jec.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=True)
h_MET_JESup.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=False, dotted=True)
h_MET_JESdown.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=False, dotted=True)
h_MET_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)

h_MET_incl_reco.legendText = 'FastSim, re-JEC'
h_MET_incl_jec.legendText  = 'FastSim, re-JEC, spurious jet filter'
h_MET_incl_full.legendText = 'FullSim'
h_MET_incl_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_MET_incl_jec.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=True)
h_MET_incl_JESup.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=False, dotted=True)
h_MET_incl_JESdown.style       = styles.lineStyle(ROOT.kRed+1,   width=2, errors=False, dotted=True)
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

h_GenMET_reco.legendText = 'Gen, FastSim'
h_GenMET_full.legendText = 'Gen, FullSim'
h_GenMET_reco.style      = styles.lineStyle(ROOT.kCyan+1,   width=2, errors=True)
h_GenMET_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)

h_RawMET_unweighted_reco.legendText = 'FastSim'
h_RawMET_unweighted_full.legendText = 'FullSim'
h_RawMET_unweighted_reco.style      = styles.lineStyle(ROOT.kGreen+1,   width=2, errors=True)
h_RawMET_unweighted_full.style      = styles.lineStyle(ROOT.kBlue+1,    width=2, errors=True)

def drawObjects( isData=False, lumi=36. ):
    tex = ROOT.TLatex()
    tex.SetNDC()
    tex.SetTextSize(0.05)
    tex.SetTextAlign(11) # align right
    lines = [
      (0.15, 0.945, 'CMS #bf{#it{Simulation}}'),
      (0.75, 0.945, '#bf{(13 TeV)}' )
    ]
    return [tex.DrawLatex(*l) for l in lines]

plot_path = './%s/'%sampleName

plotting.draw2D(
    Plot.fromHisto(name = 'FatJet_2D_full', histos = [ [h_profile2D_Fat_full] ], texX = "p_{T} (AK8) (GeV)", texY = "response"),
    plot_directory = plot_path,
    logX = False, logY = False, logZ = False,
    #scaling = {1:0, 2:0},
    #ratio = {'histos': [(0, 1)], 'texY': 'x / FullSim', 'yRange':(0.95,1.35)},
)

plotting.draw2D(
    Plot.fromHisto(name = 'FatJet_2D_fast', histos = [ [h_profile2D_Fat_fast] ], texX = "p_{T} (AK8) (GeV)", texY = "response"),
    plot_directory = plot_path,
    logX = False, logY = False, logZ = False,
    #scaling = {1:0, 2:0},
    #ratio = {'histos': [(0, 1)], 'texY': 'x / FullSim', 'yRange':(0.95,1.35)},
)

plotting.draw(
    Plot.fromHisto(name = 'FatJet', histos = [ [h_profile_Fat_fast], [h_profile_Fat_full], [h_profile_Fat_fast_JESdown], [h_profile_Fat_fast_JESup], [h_profile_Fat_full_JESdown], [h_profile_Fat_full_JESup] ], texX = "p_{T} (AK8) (GeV)", texY = "response"),
    plot_directory = plot_path,
    logX = False, logY = False, sorting = False,
    yRange = (0.9,1.2),
    legend = (0.65,0.70, 0.95, 0.80),
    drawObjects = drawObjects(),
    #scaling = {1:0, 2:0},
    #ratio = {'histos': [(0, 1)], 'texY': 'x / FullSim', 'yRange':(0.95,1.35)},
)

plotting.draw(
    Plot.fromHisto(name = 'MET_response', histos = [ [h_profile_response_MET_fast], [h_profile_response_MET_full], [h_profile_response_MET_fast_JESdown], [h_profile_response_MET_fast_JESup] ], texX = "p_{T}^{miss} (GeV)", texY = "response"),
    plot_directory = plot_path,
    logX = False, logY = False, sorting = False,
    yRange = (0.9,1.2),
    legend = (0.65,0.70, 0.95, 0.80),
    drawObjects = drawObjects(),
    #scaling = {1:0, 2:0},
    #ratio = {'histos': [(0, 1)], 'texY': 'x / FullSim', 'yRange':(0.95,1.35)},
)


plotting.draw(
    Plot.fromHisto(name = 'response_all', histos = [ [h_profile_response_all_fast], [h_profile_response_all_full], [h_profile_response_all_fast_JEC], [h_profile_response_all_fast_JESup], [h_profile_response_all_fast_JESdown] ], texX = "gen p_{T} (jet) (GeV)", texY = "response"),
    plot_directory = plot_path,
    logX = False, logY = False, sorting = False,
    yRange = (0.9,1.2),
    #scaling = {1:0, 2:0},
    #ratio = {'histos': [(0, 1),(2,1)], 'texY': 'x / FullSim'},
)

plotting.draw(
    Plot.fromHisto(name = 'response_b', histos = [ [h_profile_response_b_fast], [h_profile_response_b_full], [h_profile_response_b_fast_JEC], [h_profile_response_b_fast_JESup], [h_profile_response_b_fast_JESdown] ], texX = "gen p_{T} (b-jet) (GeV)", texY = "response"),
    plot_directory = plot_path,
    logX = False, logY = False, sorting = False,
    yRange = (0.9,1.2),
    #scaling = {1:0, 2:0},
    #ratio = {'histos': [(0, 1),(2,1)], 'texY': 'x / FullSim'},
)

plotting.draw(
    Plot.fromHisto(name = 'response_ISR', histos = [ [h_profile_response_ISR_fast], [h_profile_response_ISR_full], [h_profile_response_ISR_fast_JEC], [h_profile_response_ISR_fast_JESup], [h_profile_response_ISR_fast_JESdown] ], texX = "gen p_{T} (light jet) (GeV)", texY = "response"),
    plot_directory = plot_path,
    logX = False, logY = False, sorting = False,
    yRange = (0.9,1.2),
    #scaling = {1:0, 2:0},
    #ratio = {'histos': [(0, 1),(2,1)], 'texY': 'x / FullSim'},
)

plotting.draw(
    Plot.fromHisto(name = 'MET_pt', histos = [ [h_MET_jec], [h_MET_full], [h_MET_JESup], [h_MET_JESdown] ], texX = "p_{T}^{miss} (GeV)", texY = "a.u."),
    plot_directory = plot_path,
    logX = False, logY = True, sorting = False,
    scaling = {1:0, 2:0, 3:0},
    ratio = {'histos': [(0,1), (2,1), (3,1)], 'texY': 'x / FullSim'},
)

plotting.draw(
    Plot.fromHisto(name = 'MET_pt_incl', histos = [ [h_MET_incl_reco], [h_MET_incl_jec], [h_MET_incl_full], [h_GenMET_reco], [h_MET_incl_JESup], [h_MET_incl_JESdown] ], texX = "p_{T}^{miss} (GeV)", texY = "a.u."),
    plot_directory = plot_path,
    logX = False, logY = True, sorting = False,
    scaling = {1:0, 2:0, 3:0, 4:0, 5:0},
    ratio = {'histos': [(0,2), (1,2), (3,2)], 'texY': 'x / FullSim'},
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

