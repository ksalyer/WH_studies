import os, sys
import ROOT

import glob

mcComb_sample = glob.glob("/home/users/dspitzba/wh_babies/babies_mc_s16v3_v33_4_2019_12_30/*TTJets_2lep_*.root")
mcComb_sample+=(glob.glob("/home/users/dspitzba/wh_babies/babies_mc_s16v3_v33_4_2019_12_30/*_ST_*.root"))
mcComb_sample+=(glob.glob("/home/users/dspitzba/wh_babies/babies_mc_f17v2_v33_4_2019_12_30/*TTJets_2lep_*.root"))
mcComb_sample+=(glob.glob("/home/users/dspitzba/wh_babies/babies_mc_f17v2_v33_4_2019_12_30/*_ST_*.root"))
mcComb_sample+=(glob.glob("/home/users/dspitzba/wh_babies/babies_mc_a18v1_v33_4_2019_12_30/slim*TTJets_2lep_*.root"))
mcComb_sample+=(glob.glob("/home/users/dspitzba/wh_babies/babies_mc_a18v1_v33_4_2019_12_30/slim*_ST_*.root"))

print('Loaded samples')

WHLepton = '((abs(lep1_pdgid)==11&&leps_pt[0]>30&&(lep1_relIso*leps_pt[0])<5)||(abs(lep1_pdgid)==13&&leps_pt[0]>25&&(lep1_relIso*leps_pt[0])<5&&abs(leps_eta[0])<2.1))'
WHLeptonCR = '(((abs(lep1_pdgid)==11&&leps_pt[0]>30&&(lep1_relIso*leps_pt[0])<5)||(abs(lep1_pdgid)==13&&leps_pt[0]>25&&(lep1_relIso*leps_pt[0])<5&&abs(leps_eta[0])<2.1))||((abs(lep2_pdgid)==11&&leps_pt[1]>30&&(lep2_relIso*leps_pt[1])<5)||(abs(lep2_pdgid)==13&&leps_pt[1]>25&&(lep2_relIso*leps_pt[1])<5&&abs(leps_eta[1])<2.1)))'
controlCuts = "stitch&&pass&&nvetoleps>=2&&ngoodjets==2&&mct>200&&mbb>90&&mbb<150&&mt_met_lep>150&&ngoodbtags==2"
signalCuts  = "stitch&&pass&&nvetoleps==1&&PassTrackVeto&&PassTauVeto&&ngoodjets==2&&mct>200&&mt_met_lep>150&&mbb>90&&mbb<150&&ngoodbtags==2"

print('Defined cuts')

from RootTools.core.standard import *

print('imported root tools')

myDataSample = Sample.fromFiles('myDataSample', mcComb_sample, 't')

print('plotting...')

numHisto = myDataSample.get1DHistoFromDraw('pfmet', [125,200,300,400,500], binningIsExplicit=True, weightString="weight*w_pu*137.2", selectionString=WHLepton+'&&'+signalCuts)
denHisto = myDataSample.get1DHistoFromDraw('pfmet', [125,200,300,400,500], binningIsExplicit=True, weightString="weight*w_pu*137.2", selectionString=WHLeptonCR+'&&'+controlCuts)
#numHisto_dup = myDataSample.get1DHistoFromDraw('pfmet', [125,200,300,400,500], binningIsExplicit=True, weightString="weight*w_pu*137.2", selectionString=WHLepton+'&&'+signalCuts)

numHisto.style = styles.lineStyle(ROOT.kOrange+1, width=2, error=True)

numHisto_dup = numHisto.Clone()
numHisto_dup.Divide(denHisto)
plot1 = Plot.fromHisto('transferfactor_plot_num', [[numHisto]], texX = 'MET', texY='counts')
plot2 = Plot.fromHisto('transferfactor_plot_den', [[denHisto]], texX = 'MET', texY='counts')
plot3 = Plot.fromHisto('transferfactor_plot_', [[numHisto_dup]], texX = 'MET', texY='Transfer Factor')
plotting.draw(plot1, plot_directory = './plots/',logX = False, logY=False)
plotting.draw(plot2, plot_directory = './plots/',logX = False, logY=False)
plotting.draw(plot3, plot_directory = './plots/',logX = False, logY=False)

print('plotted!')
