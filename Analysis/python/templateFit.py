'''
Some spaghetti code for W+jets estimation. Will at some point live in a different repository, too.

'''


import ROOT
import glob
import math
import os
import pickle

from ROOT import RooFit as rf
from RootTools.core.standard import *

from WH_studies.Tools.asym_float import asym_float as af


#!/usr/bin/env python
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--year",                 action='store',      default=2017, type="int", help='Which year?')
(options, args) = parser.parse_args()

def getRandomHistOfTemplate(hist, color=ROOT.kOrange):
    h = ROOT.TH1F()
    hist.Copy(h)
    h.Reset()
    h.Sumw2()
    h.SetLineColor(color)
    h.FillRandom(hist, int(hist.GetEntries()))
    h.Scale(1./h.Integral()*hist.Integral())
    res = h.Clone()
    del h
    return res

def getIntegralAndError(hist):
    err = ROOT.Double()
    val = hist.IntegralAndError(0,1000,err)
    return af(val,err)

year = int(options.year)

#if options.combined:
#    lumi = 137.2
#    mc[2016]      = '/home/users/dspitzba/wh_babies/babies_mc_s16v3_v33_4_2019_12_30/'
#    data[2016]    = '/home/users/dspitzba/wh_babies/babies_v33_4_2019_12_30/'



if year == 2016:
    # definitions
    mcDir   = '/home/users/dspitzba/wh_babies/babies_mc_s16v3_v33_4_2019_12_30/'
    dataDir = '/home/users/dspitzba/wh_babies/babies_v33_4_2019_12_30/'
    lumi = '35.9'
    
    #FIXME split off WX part because of low stats and negative weights
    # w+jets
    WJetsDirs_2016 =   glob.glob(mcDir+'slim_W*JetsToLNu_s16v3*.root') \
                + glob.glob(mcDir+"slim*W*Jets_NuPt200_s16v*.root") \

    WJets = Sample.fromFiles('WJets', WJetsDirs_2016, "t")
    WJets.setSelectionString("stitch")

    # WX
    WXDirs_2016  = glob.glob(mcDir+'slim*WW*.root') \
            + glob.glob(mcDir+'slim*WZ*.root') \
            + glob.glob(mcDir+'slim*ZZ*.root') \

    WX = Sample.fromFiles('WX', WXDirs_2016, "t")

    # DY for 2l - take all MC at once    
    DYJetsDirs  = glob.glob(mcDir+'slim_DYJetsToLL_M50_s16v3*.root')\
                + glob.glob(mcDir+'slim*WW*.root') \
                + glob.glob(mcDir+'slim*WZ*.root') \
                + glob.glob(mcDir+'slim*ZZ*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_top_s16v3*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_tbar_s16v3*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_*met150*.root') \
                + glob.glob(mcDir+'slim*TTJets_2lep_s16v3*.root')\
                + glob.glob(mcDir+'slim*TTJets_2lep_*met150*.root')\
                + glob.glob(mcDir+'slim*_ST_*.root') \
                + glob.glob(mcDir+'slim*TTW*.root') \
                + glob.glob(mcDir+'slim*TTZ*.root')
    DYJets = Sample.fromFiles("DYJets", DYJetsDirs, "t")
    DYJets.setSelectionString("stitch")

    # tt/t
    TTJetsDirs_2016 =  glob.glob(mcDir+'slim*TTJets_1lep_top_s16v3*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_tbar_s16v3*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_*met150*.root') \
                + glob.glob(mcDir+'slim*TTJets_2lep_s16v3*.root')\
                + glob.glob(mcDir+'slim*TTJets_2lep_*met150*.root')\
                + glob.glob(mcDir+'slim*_ST_*.root') \
                + glob.glob(mcDir+'slim*TTW*.root') \
                + glob.glob(mcDir+'slim*TTZ*.root')
    
    TTJets = Sample.fromFiles('TTJets', TTJetsDirs_2016, 't')
    TTJets.setSelectionString("stitch")
    
    # diboson + ttV. could also put ttV to tt/t
    DibosonDirs = glob.glob(mcDir+'slim*WW*.root') \
                + glob.glob(mcDir+'slim*WZ*.root') \
                + glob.glob(mcDir+'slim*ZZ*.root') \
                + glob.glob(mcDir+'slim*TTW*.root') \
                + glob.glob(mcDir+'slim*TTZ*.root')
    
    Diboson = Sample.fromFiles('Diboson', DibosonDirs, 't')
    
    # load data, but keep SR blinded
    Data = Sample.fromFiles('Data', glob.glob(dataDir+"*data_2016*single*.root") + glob.glob(dataDir+"*data_2016*met*.root"), 't')
    Data.setSelectionString("pass&&(HLT_SingleEl==1||HLT_SingleMu==1) && (ngoodbtags<2||mbb<90||mbb>150)")

elif year == 2017:
    # definitions
    mcDir   = '/home/users/dspitzba/wh_babies/babies_mc_f17v2_v33_4_2019_12_30/'
    dataDir = '/home/users/dspitzba/wh_babies/babies_Run2017_v33_4_2019_12_30/'
    lumi = '41.5'
    
    # w+jets
    WJetsDirs_2017   = glob.glob(mcDir+"*slim_W*JetsToLNu_f17v2*")\
                + glob.glob(mcDir+"slim*W*Jets_NuPt200_f17v*.root")\

    WJets = Sample.fromFiles('WJets', WJetsDirs_2017, "t")
    WJets.setSelectionString("stitch")

    # WX
    WXDirs_2017  = glob.glob(mcDir+'slim*WW*.root') \
            + glob.glob(mcDir+'slim*WZ*.root') \
            + glob.glob(mcDir+'slim*ZZ*.root') \

    WX = Sample.fromFiles('WX', WXDirs_2017, "t")

    # DY for 2l - take all MC at once    
    DYJetsDirs  = glob.glob(mcDir+'slim_DYJetsToLL_M50_f17v2*.root')\
                + glob.glob(mcDir+'slim*WW*.root') \
                + glob.glob(mcDir+'slim*WZ*.root') \
                + glob.glob(mcDir+'slim*ZZ*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_top_f17v2*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_tbar_f17v2*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_*met150*.root') \
                + glob.glob(mcDir+'slim*TTJets_2lep_f17v2*.root')\
                + glob.glob(mcDir+'slim*TTJets_2lep_*met150*.root')\
                + glob.glob(mcDir+'slim*_ST_*.root') \
                + glob.glob(mcDir+'slim*TTW*.root') \
                + glob.glob(mcDir+'slim*TTZ*.root')
    DYJets = Sample.fromFiles("DYJets", DYJetsDirs, "t")
    DYJets.setSelectionString("stitch")
    
    # tt/t
    TTJetsDirs_2017 =  glob.glob(mcDir+'slim*TTJets_1lep_top_f17v2*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_tbar_f17v2*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_*met150*.root') \
                + glob.glob(mcDir+'slim*TTJets_2lep_f17v2*.root')\
                + glob.glob(mcDir+'slim*TTJets_2lep_*met150*.root')\
                + glob.glob(mcDir+'slim*_ST_*.root')\
                + glob.glob(mcDir+'slim*TTW*.root') \
                + glob.glob(mcDir+'slim*TTZ*.root')
    
    TTJets = Sample.fromFiles('TTJets', TTJetsDirs_2017, 't')
    TTJets.setSelectionString("stitch")
    
    # diboson + ttV. could also put ttV to tt/t
    DibosonDirs = glob.glob(mcDir+'slim*WW*.root') \
                + glob.glob(mcDir+'slim*WZ*.root') \
                + glob.glob(mcDir+'slim*ZZ*.root') \
    
    Diboson = Sample.fromFiles('Diboson', DibosonDirs, 't')
    
    # load data, but keep SR blinded
    Data = Sample.fromFiles('Data', glob.glob(dataDir+"*data_2017*.root"), 't')
    Data.setSelectionString("pass&&(HLT_SingleEl==1||HLT_SingleMu==1) && (ngoodbtags<2||mbb<90||mbb>150)")

elif year == 2018:
    # definitions
    mcDir   = '/home/users/dspitzba/wh_babies/babies_mc_a18v1_v33_4_2019_12_30/'
    dataDir = '/home/users/dspitzba/wh_babies/babies_Run2018_v33_4_2019_12_30/'
    lumi = '60.0'
    
    WJetsDirs_2018   = glob.glob(mcDir+'slim*W*JetsToLNu_a18v1*.root') \
                + glob.glob(mcDir+'slim*W*Jets_NuPt200_a18v*.root')

    # w+jets
    WJets = Sample.fromFiles('WJets', WJetsDirs_2018, "t")
    WJets.setSelectionString("stitch")

    # WX
    WXDirs_2018  = glob.glob(mcDir+'slim*WW*.root') \
            + glob.glob(mcDir+'slim*WZ*.root') \
            + glob.glob(mcDir+'slim*ZZ*.root') \

    WX = Sample.fromFiles('WX', WXDirs_2018, "t")

    # DY for 2l - take all MC at once    
    DYJetsDirs  = glob.glob(mcDir+'slim_DYJetsToLL_madgraph_*.root')\
                + glob.glob(mcDir+'slim*WW*.root') \
                + glob.glob(mcDir+'slim*WZ*.root') \
                + glob.glob(mcDir+'slim*ZZ*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_top_a18v1*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_tbar_a18v1*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_*met150*.root') \
                + glob.glob(mcDir+'slim*TTJets_2lep_a18v1*.root')\
                + glob.glob(mcDir+'slim*TTJets_2lep_*met150*.root')\
                + glob.glob(mcDir+'slim*_ST_*.root') \
                + glob.glob(mcDir+'slim*TTW*.root') \
                + glob.glob(mcDir+'slim*TTZ*.root')
    DYJets = Sample.fromFiles("DYJets", DYJetsDirs, "t")
    DYJets.setSelectionString("stitch")
    
    # tt/t
    TTJetsDirs_2018 =  glob.glob(mcDir+'slim*TTJets_1lep_top_a18v1*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_tbar_a18v1*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_*met150*.root') \
                + glob.glob(mcDir+'slim*TTJets_2lep_a18v1*.root')\
                + glob.glob(mcDir+'slim*TTJets_2lep_*met150*.root')\
                + glob.glob(mcDir+'slim*_ST_*.root') \
                + glob.glob(mcDir+'slim*TTW*.root') \
                + glob.glob(mcDir+'slim*TTZ*.root')
    
    TTJets = Sample.fromFiles('TTJets', TTJetsDirs_2018, 't')
    TTJets.setSelectionString("stitch")
    
    # diboson + ttV. could also put ttV to tt/t
    DibosonDirs = glob.glob(mcDir+'slim*WW*.root') \
                + glob.glob(mcDir+'slim*WZ*.root') \
                + glob.glob(mcDir+'slim*ZZ*.root')
    
    Diboson = Sample.fromFiles('Diboson', DibosonDirs, 't')
    
    # load data, but keep SR blinded
    Data = Sample.fromFiles('Data', glob.glob(dataDir+"slim*data_2018*.root"), 't')
    Data.setSelectionString("pass&&(HLT_SingleEl==1||HLT_SingleMu==1) && (ngoodbtags<2||mbb<90||mbb>150)")

elif year == 'combined':
    dataDir_16 = '/home/users/dspitzba/wh_babies/babies_v33_4_2019_12_30/'
    dataDir_17 = '/home/users/dspitzba/wh_babies/babies_Run2017_v33_4_2019_12_30/'
    dataDir_18 = '/home/users/dspitzba/wh_babies/babies_Run2018_v33_4_2019_12_30/'

    lumi = '137'

    WJets = Sample.fromFiles('WJets', WJetsDirs_2016 + WJetsDirs_2017 + WJetsDirs_2018, "t")
    WJets.setSelectionString("stitch")

    WX = Sample.fromFiles('WX', WXDirs_2016 + WXDirs_2017 + WXDirs_2018, "t")

    TTJets = Sample.fromFiles('TTJets', TTJetsDirs_2016 + TTJetsDirs_2017 + TTJetsDirs_2018, 't')
    TTJets.setSelectionString("stitch")

    Data = Sample.fromFiles('Data', glob.glob(dataDir+"slim*data_2018*.root"), 't')
    Data.setSelectionString("pass&&(HLT_SingleEl==1||HLT_SingleMu==1) && (ngoodbtags<2||mbb<90||mbb>150)")


# CR selection without b-tags
WHSelection     = "(Sum$(abs(lep1_pdgid)==11&&(leps_pt[0]>30&&(lep1_relIso*leps_pt[0])<5)||abs(lep1_pdgid)==13&&(leps_pt[0]>25&&(lep1_relIso*leps_pt[0])<5&&abs(leps_eta[0])<2.1))+"
WHSelection    += "Sum$(abs(lep2_pdgid)==11&&(leps_pt[1]>30&&(lep2_relIso*leps_pt[1])<5)||abs(lep2_pdgid)==13&&(leps_pt[1]>25&&(lep2_relIso*leps_pt[1])<5&&abs(leps_eta[1])<2.1)))==1"
selectionString = WHSelection+"&&pass&&nvetoleps==1&&PassTrackVeto&&PassTauVeto&&ngoodjets==2&&pfmet>125&&mt_met_lep>150&&mct>200&&mbb>90&&mbb<150"
#selectionString = WHSelection+"&&pass&&nvetoleps==1&&PassTrackVeto&&PassTauVeto&&ngoodjets==3&&pfmet>125&&mt_met_lep>150&&mct>200&&mbb>90&&mbb<150 && Sum$(ak4pfjets_pt>100)<=3"
#selectionString = WHSelection+"&&pass&&nvetoleps==1&&PassTrackVeto&&PassTauVeto&&ngoodjets==2&&pfmet>125&&mt_met_lep>150&&mct>200&&((mbb<90&&mbb>30)||(mbb>150))"

WHLepton1 = "(abs(lep1_pdgid)==11&&(leps_pt[0]>30&&(lep1_relIso*leps_pt[0])<5)||abs(lep1_pdgid)==13&&(leps_pt[0]>25&&(lep1_relIso*leps_pt[0])<5&&abs(leps_eta[0])<2.1))"
WHLepton2 = "(abs(lep2_pdgid)==11&&(leps_pt[1]>30&&(lep2_relIso*leps_pt[1])<5)||abs(lep2_pdgid)==13&&(leps_pt[1]>25&&(lep2_relIso*leps_pt[1])<5&&abs(leps_eta[1])<2.1))"

pdgid1 = "MaxIf$(lep1_pdgid/abs(lep1_pdgid), abs(lep1_pdgid)==11&&(leps_pt[0]>30&&(lep1_relIso*leps_pt[0])<5)||abs(lep1_pdgid)==13&&(leps_pt[0]>25&&(lep1_relIso*leps_pt[0])<5&&abs(leps_eta[0])<2.1))"
pdgid2 = "MaxIf$(lep2_pdgid/abs(lep2_pdgid), abs(lep2_pdgid)==11&&(leps_pt[1]>30&&(lep2_relIso*leps_pt[1])<5)||abs(lep2_pdgid)==13&&(leps_pt[1]>25&&(lep2_relIso*leps_pt[1])<5&&abs(leps_eta[1])<2.1))"
pdgid = "((%s)+(%s))"%(pdgid1,pdgid2)

# 2l selection for systematics
dilepSelection     = "(Sum$(abs(lep1_pdgid)==11&&(leps_pt[0]>30&&(lep1_relIso*leps_pt[0])<5)||abs(lep1_pdgid)==13&&(leps_pt[0]>25&&(lep1_relIso*leps_pt[0])<5&&abs(leps_eta[0])<2.1))+"
dilepSelection    += "Sum$(abs(lep2_pdgid)==11&&(leps_pt[1]>30&&(lep2_relIso*leps_pt[1])<5)||abs(lep2_pdgid)==13&&(leps_pt[1]>25&&(lep2_relIso*leps_pt[1])<5&&abs(leps_eta[1])<2.1)))==2"

#raise NotImplementedError
    
## fancy reweighting for Higgs tag estimation
reweighting = "((ak8pfjets_pt[0]>170&&ak8pfjets_pt[0]<250)*0.05 + (ak8pfjets_pt[0]>250&&ak8pfjets_pt[0]<300)*0.15 + (ak8pfjets_pt[0]>300&&ak8pfjets_pt[0]<400)*0.27 + (ak8pfjets_pt[0]>400&&ak8pfjets_pt[0]<500)*0.35 + (ak8pfjets_pt[0]>500&&ak8pfjets_pt[0]<750)*0.40 + (ak8pfjets_pt[0]>750)*0.35)"

histogramPickle = 'histograms_%s.pkl'%year

if not os.path.isfile(histogramPickle):

    print "W+jets templates"
    WJets2D_pos = WJets.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString+"&&%s>0"%pdgid, weightString='weight * w_pu *'+lumi, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
    WJets2D_neg = WJets.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString+"&&%s<0"%pdgid, weightString='weight * w_pu *'+lumi, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
    
    WX2D_pos = WX.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString+"&&%s>0"%pdgid, weightString='weight * w_pu *'+lumi, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
    WX2D_neg = WX.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString+"&&%s<0"%pdgid, weightString='weight * w_pu *'+lumi, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
    
    WJets2D_Higgs = WJets.get2DHistoFromDraw('Sum$(ak8pfjets_deepdisc_hbb>0.8):pfmet', [[125,200,300,400,1000], [-0.5,0.5,10]], selectionString=selectionString+"&&ngoodbtags==2", weightString='weight * w_pu *'+lumi, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
    TTJets2D_Higgs = TTJets.get2DHistoFromDraw('Sum$(ak8pfjets_deepdisc_hbb>0.8):pfmet', [[125,200,300,400,1000], [-0.5,0.5,10]], selectionString=selectionString+"&&ngoodbtags==2", weightString='weight * w_pu *'+lumi, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
    
    ## what to do with boosted stuff in WX?? #FIXME
    WJets2D_Boosted = WJets.get2DHistoFromDraw('Sum$(ak8pfjets_pt>170):pfmet', [[125,200,300,400,1000], [-0.5,0.5,10]], selectionString=selectionString+"&&ngoodbtags==2", weightString='weight * w_pu *'+lumi, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
    WJets2D_BoostedRew = WJets.get2DHistoFromDraw('Sum$(ak8pfjets_pt>170):pfmet', [[125,200,300,400,1000], [-0.5,0.5,10]], selectionString=selectionString+"&&ngoodbtags==2", weightString='weight * w_pu *'+lumi+'*'+reweighting, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
    TTJets2D_Boosted = TTJets.get2DHistoFromDraw('Sum$(ak8pfjets_pt>170):pfmet', [[125,200,300,400,1000], [-0.5,0.5,10]], selectionString=selectionString+"&&ngoodbtags==2", weightString='weight * w_pu *'+lumi, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
    
    print "tt+jets templates"
    TTJets2D = TTJets.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString, weightString='weight * w_pu *'+lumi, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
    
    print "data templates"
    Data2D_pos = Data.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString+"&&%s>0"%pdgid, weightString='(1)', binningIsExplicit=True) # x-pfmet, y-ngoodbtags
    Data2D_neg = Data.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString+"&&%s<0"%pdgid, weightString='(1)', binningIsExplicit=True) # x-pfmet, y-ngoodbtags

    histograms = {'WJets2D_pos':WJets2D_pos, 'WJets2D_neg':WJets2D_neg, 'WX2D_pos':WX2D_pos, 'WX2D_neg':WX2D_neg, 'WJets2D_Higgs':WJets2D_Higgs, 'TTJets2D_Higgs':TTJets2D_Higgs, 'WJets2D_Boosted':WJets2D_Boosted, 'WJets2D_BoostedRew':WJets2D_BoostedRew, 'TTJets2D_Boosted':TTJets2D_Boosted, 'TTJets2D':TTJets2D, 'Data2D_pos':Data2D_pos, 'Data2D_neg':Data2D_neg}
    pickle.dump(histograms, file(histogramPickle, 'w'))

else:
    histograms = pickle.load(file(histogramPickle))
    WJets2D_pos     = histograms['WJets2D_pos']
    WJets2D_neg     = histograms['WJets2D_neg']
    WX2D_pos        = histograms['WX2D_pos']
    WX2D_neg        = histograms['WX2D_neg']
    WJets2D_Higgs   = histograms['WJets2D_Higgs']
    TTJets2D_Higgs  = histograms['TTJets2D_Higgs']
    WJets2D_Boosted = histograms['WJets2D_Boosted']
    WJets2D_BoostedRew = histograms['WJets2D_BoostedRew']
    TTJets2D_Boosted = histograms['TTJets2D_Boosted']
    TTJets2D        = histograms['TTJets2D']
    Data2D_pos      = histograms['Data2D_pos']
    Data2D_neg      = histograms['Data2D_neg']


metBins = [(125,200), (200,300), (300,400), (400,-1)]

W_pred = {}

yearWeight = "((year==2016)*35.9+((year==2017)*41.6)+((year==2018)*59.7))" # only need weight*w_pu in addition

for metBin in range(len(metBins)):
    print "Working on MET bin:",  metBins[metBin]
    WJetsHist_pos   = ROOT.TH1F("WJetsHist_pos", "", 2,-0.5,1.5)
    WJetsHist_neg   = ROOT.TH1F("WJetsHist_neg", "", 2,-0.5,1.5)
    TTJetsHist      = ROOT.TH1F("TTJetsHist", "", 2,-0.5,1.5)
    DataHist_pos    = ROOT.TH1F("DataHist_pos", "", 2,-0.5,1.5)
    DataHist_neg    = ROOT.TH1F("DataHist_neg", "", 2,-0.5,1.5)
    
    #for x,y in [(WJets2D_pos,WJetsHist_pos), (WJets2D_neg,WJetsHist_neg), (TTJets2D,TTJetsHist), (Data2D_pos,DataHist_pos), (Data2D_neg,DataHist_neg)]:
    #    for i in range(2):
    #        y.SetBinContent(i+1, x.GetBinContent(metBin+1, i+1))
    #        y.SetBinError(i+1, x.GetBinError(metBin+1, i+1))

    for i in range(2):
        WJetsHist_pos.SetBinContent(i+1, WJets2D_pos.GetBinContent(metBin+1, i+1) + WX2D_pos.GetBinContent(metBin+1, i+1))
        WJetsHist_pos.SetBinError(i+1,   math.sqrt(WJets2D_pos.GetBinError(metBin+1, i+1)**2 + WX2D_pos.GetBinError(metBin+1, i+1)**2))

        WJetsHist_neg.SetBinContent(i+1, WJets2D_neg.GetBinContent(metBin+1, i+1) + WX2D_neg.GetBinContent(metBin+1, i+1))
        WJetsHist_neg.SetBinError(i+1,   math.sqrt(WJets2D_neg.GetBinError(metBin+1, i+1)**2 + WX2D_neg.GetBinError(metBin+1, i+1)**2))

        TTJetsHist.SetBinContent(i+1, TTJets2D.GetBinContent(metBin+1, i+1))
        TTJetsHist.SetBinError(i+1,   TTJets2D.GetBinError(metBin+1, i+1))

        DataHist_pos.SetBinContent(i+1, Data2D_pos.GetBinContent(metBin+1, i+1))
        DataHist_pos.SetBinError(i+1,   Data2D_pos.GetBinError(metBin+1, i+1))

        DataHist_neg.SetBinContent(i+1, Data2D_neg.GetBinContent(metBin+1, i+1))
        DataHist_neg.SetBinError(i+1,   Data2D_neg.GetBinError(metBin+1, i+1))
    
    W_prefit = getIntegralAndError(WJetsHist_pos) + getIntegralAndError(WJetsHist_neg)
    tt_prefit = getIntegralAndError(TTJetsHist)
    print "## Prefit Values ##"
    print "W+jets, pos", WJetsHist_pos.GetBinContent(1), WJetsHist_pos.GetBinContent(2)
    print "W+jets, neg", WJetsHist_neg.GetBinContent(1), WJetsHist_neg.GetBinContent(2)
    print "tt+jets", TTJetsHist.GetBinContent(1), TTJetsHist.GetBinContent(2)
    print "Data, pos", DataHist_pos.GetBinContent(1), DataHist_pos.GetBinContent(2)
    print "Data, neg", DataHist_neg.GetBinContent(1), DataHist_neg.GetBinContent(2)
    
    # get templates (= normalized prefit histograms)
    WJetsTemp_pos = WJetsHist_pos.Clone()
    WJetsTemp_pos.Scale(1./WJetsTemp_pos.Integral())
    WJetsTemp_neg = WJetsHist_neg.Clone()
    WJetsTemp_neg.Scale(1./WJetsTemp_neg.Integral())
    TTJetsTemp = TTJetsHist.Clone()
    TTJetsTemp.Scale(1./TTJetsTemp.Integral())

    # do the bootstrap
    yields_WJets_0b_postFit = []
    for i in range(1):
        if i == 0:
            WJetsTemp_pos_ = WJetsTemp_pos
            WJetsTemp_neg_ = WJetsTemp_neg
            TTJetsTemp_ = TTJetsTemp
    
        else:
            WJetsTemp_pos_ = getRandomHistOfTemplate(WJetsTemp_pos)
            WJetsTemp_neg_ = getRandomHistOfTemplate(WJetsTemp_neg)
            TTJetsTemp_ = getRandomHistOfTemplate(TTJetsTemp)
    
        # do the fit --> can also split in lepton flavor
        
        x = ROOT.RooRealVar('ngoodbtags','ngoodbtags',-0.5,1.5)
        data_hist_pos       = ROOT.RooDataHist("data", "data", ROOT.RooArgList(x), DataHist_pos)
        data_hist_neg       = ROOT.RooDataHist("data", "data", ROOT.RooArgList(x), DataHist_neg)
        wjets_hist_pos      = ROOT.RooDataHist("wjets", "wjets", ROOT.RooArgList(x), WJetsHist_pos)
        wjets_hist_neg      = ROOT.RooDataHist("wjets", "wjets", ROOT.RooArgList(x), WJetsHist_neg)
        ttjets_hist         = ROOT.RooDataHist("ttjets", "ttjets", ROOT.RooArgList(x), TTJetsHist)
        
        #Define yields as variable
        yield_WJets_pos     = ROOT.RooRealVar("yield_WJets_pos","yield_WJets_pos",0.1,0,10**5)
        yield_WJets_neg     = ROOT.RooRealVar("yield_WJets_neg","yield_WJets_neg",0.1,0,10**5)
        yield_TTJets        = ROOT.RooRealVar("yield_TTJets","yield_TTJets",0.1,0,10**5)
        
        #Make PDF from MC histograms
        model_WJets_pos     = ROOT.RooHistPdf("model_WJets_pos", "model_WJets_pos", ROOT.RooArgSet(x), wjets_hist_pos)
        model_WJets_neg     = ROOT.RooHistPdf("model_WJets_neg", "model_WJets_neg", ROOT.RooArgSet(x), wjets_hist_neg)
        model_TTJets        = ROOT.RooHistPdf("model_TTJets", "model_TTJets", ROOT.RooArgSet(x), ttjets_hist)
        
        #Make combined PDF of all MC Backgrounds
        model_total_pos = ROOT.RooAddPdf("model_total_pos", "model_total_pos", ROOT.RooArgList(model_WJets_pos, model_TTJets), ROOT.RooArgList(yield_WJets_pos, yield_TTJets))
        model_total_neg = ROOT.RooAddPdf("model_total_neg", "model_total_neg", ROOT.RooArgList(model_WJets_neg, model_TTJets), ROOT.RooArgList(yield_WJets_neg, yield_TTJets))
        
        print "starting to perform fit"
        
        #model.fitTo(data)#It is this fitTo command that gives the statistical output
        nllComponents = ROOT.RooArgList("nllComponents")
        nll_pos = model_total_pos.createNLL(data_hist_pos,rf.NumCPU(1))
        nll_neg = model_total_neg.createNLL(data_hist_neg,rf.NumCPU(1))
        nllComponents.add(nll_pos)
        nllComponents.add(nll_neg)
        
        #pll_phi=nll.createProfile(r.RooArgSet(mc1_yield))#anotherwayofdoingthefitTo
        sumNLL = ROOT.RooAddition("sumNLL","sumNLL", nllComponents)
        
        ROOT.RooMinuit(sumNLL).migrad()
        ROOT.RooMinuit(sumNLL).hesse()
        ROOT.RooMinuit(sumNLL).minos()#optional
        
        print "## Post-fit ##"
        print "yield_WJets_pos:" , yield_WJets_pos.getVal()
        print "yield_WJets_neg:" , yield_WJets_neg.getVal()
        print "yield_TTJets:" , yield_TTJets.getVal()
        
        yield_WJets_0b_postFit  = yield_WJets_pos.getVal()*WJetsTemp_pos_.GetBinContent(1)+yield_WJets_neg.getVal()*WJetsTemp_neg_.GetBinContent(1)
        yield_WJets_0b_preFit   = WJetsHist_pos.GetBinContent(1)+WJetsHist_neg.GetBinContent(1)
        
        yields_WJets_0b_postFit.append(yield_WJets_0b_postFit)
        print "W+Jets scaled by: ", yield_WJets_0b_postFit/yield_WJets_0b_preFit
        
        fitFrame_PosPdg=x.frame(rf.Bins(50),rf.Title("FitModel"))
        
        model_total_pos.paramOn(fitFrame_PosPdg,rf.Layout(0.42,0.9,0.9))
        data_hist_pos.plotOn(fitFrame_PosPdg,rf.LineColor(ROOT.kRed))
        model_total_pos.plotOn(fitFrame_PosPdg,rf.LineStyle(ROOT.kDashed))
        model_total_pos.plotOn(fitFrame_PosPdg,rf.Components("model_WJets_pos"),rf.LineColor(ROOT.kGreen))
        model_total_pos.plotOn(fitFrame_PosPdg,rf.Components("model_TTJets"),rf.LineColor(ROOT.kBlue))
        #model_total_pos.plotOn(fitFrame_PosPdg,rf.Components("model_Diboson_pos"),rf.LineColor(ROOT.kOrange+7))
        
        fitFrame_NegPdg=x.frame(rf.Bins(50),rf.Title("FitModel"))
        model_total_neg.paramOn(fitFrame_NegPdg,rf.Layout(0.42,0.9,0.9))
        data_hist_neg.plotOn(fitFrame_NegPdg,rf.LineColor(ROOT.kRed))
        model_total_neg.plotOn(fitFrame_NegPdg,rf.LineStyle(ROOT.kDashed))
        model_total_neg.plotOn(fitFrame_NegPdg,rf.Components("model_WJets_neg"),rf.LineColor(ROOT.kGreen))
        model_total_neg.plotOn(fitFrame_NegPdg,rf.Components("model_TTJets"),rf.LineColor(ROOT.kBlue))
        #model_total_neg.plotOn(fitFrame_NegPdg,rf.Components("model_Diboson_neg"),rf.LineColor(ROOT.kOrange+7))
        
        if i == 0:
            pos_val = af(yield_WJets_pos.getVal(), yield_WJets_pos.getErrorHi(), -yield_WJets_pos.getErrorLo())
            neg_val = af(yield_WJets_neg.getVal(), yield_WJets_neg.getErrorHi(), -yield_WJets_neg.getErrorLo())
            f_pos   = af(WJetsTemp_pos.GetBinContent(1), WJetsTemp_pos.GetBinError(1))
            f_neg   = af(WJetsTemp_neg.GetBinContent(1), WJetsTemp_neg.GetBinError(1))
            W_0b    = f_pos*pos_val + f_neg*neg_val
            SF_W    = (pos_val+neg_val) / W_prefit
            print "yield_TTJets, again:",  yield_TTJets.getVal()
            SF_top  = af(yield_TTJets.getVal()*2, yield_TTJets.getErrorHi()*math.sqrt(2)) / tt_prefit

            #c1=ROOT.TCanvas("c1","FitModel",650,1000)
            #ROOT.gROOT.SetStyle("Plain")
            #c1.Divide(1,2)
            #c1.cd(1)
            #ROOT.gROOT.SetStyle("Plain")#Removesgraybackgroundfromplots
            #ROOT.gPad.SetLeftMargin(0.15)
            #fitFrame_PosPdg.GetYaxis().SetTitleOffset(1.4)
            #fitFrame_PosPdg.GetXaxis().SetTitle("N_{b}")
            #fitFrame_PosPdg.Draw()
            #
            #c1.cd(2)
            #ROOT.gROOT.SetStyle("Plain")#Removesgraybackgroundfromplots
            #ROOT.gPad.SetLeftMargin(0.15)
            #fitFrame_NegPdg.GetYaxis().SetTitleOffset(1.4)
            #fitFrame_NegPdg.GetXaxis().SetTitle("N_{b}")
            #fitFrame_NegPdg.Draw()
            #
            #
            #c1.Print('./%s_nBTagFitRes_%s.png'%(year, MET_string))
            #c1.Print('./%s_nBTagFitRes_%s.pdf'%(year, MET_string))
            #c1.Print('./%s_nBTagFitRes_%s.root'%(year, MET_string))

            # make the more beautiful plot
            MET_string = "%s_%s"%(metBins[metBin][0], metBins[metBin][1])
            
            WJetsHist_pos_postFit = WJetsTemp_pos.Clone()
            WJetsHist_pos_postFit.Scale(yield_WJets_pos.getVal())
            WJetsHist_neg_postFit = WJetsTemp_neg.Clone()
            WJetsHist_neg_postFit.Scale(yield_WJets_neg.getVal())
            WJetsHist_pos_postFit.Add(WJetsHist_neg_postFit)
            TTJetsHist_postFit = TTJetsTemp.Clone()
            TTJetsHist_postFit.Scale(2*yield_TTJets.getVal())
            Total_postFit = WJetsHist_pos_postFit.Clone()
            Total_postFit.Add(TTJetsHist_postFit)
            
            Data_postFit = DataHist_pos.Clone()
            Data_postFit.Add(DataHist_neg)
            #Data_postFit.syle = styles.errorStyle(ROOT.kBlack, markerSize=2, width=1)
            Data_postFit.drawOption = 'e1p'
            Data_postFit.legendText = 'Data'
            
            WJetsHist_pos_postFit.style = styles.lineStyle(8, width=2, errors=False)
            TTJetsHist_postFit.style = styles.lineStyle(46, width=2, errors=False)
            Total_postFit.style = styles.lineStyle(ROOT.kBlue+1, width=2, errors=True)
            
            WJetsHist_pos_postFit.legendText = 'W+jets/VV (postfit)'
            TTJetsHist_postFit.legendText = 'top (postfit)'
            Total_postFit.legendText = 'Total (post-fit)'


            # prefit
            WJetsHist_pos.Add(WJetsHist_neg)
            
            WJetsHist_pos.style = styles.lineStyle(8, width=2, dashed=True)
            TTJetsHist.style = styles.lineStyle(46, width=2, dashed=True)

            WJetsHist_pos.legendText = 'W+jets/VV (prefit)'
            TTJetsHist.legendText = 'top (prefit)'

            plot_path = './'

            histos = [[Data_postFit], [WJetsHist_pos_postFit], [TTJetsHist_postFit], [Total_postFit], [WJetsHist_pos], [TTJetsHist] ]

            def drawObjects( isData=False, lumi=36 ):
                tex = ROOT.TLatex()
                tex.SetNDC()
                tex.SetTextSize(0.05)
                tex.SetTextAlign(11) # align right
                lines = [
                  (0.08, 0.945, 'CMS Simulation') if not isData else (0.15, 0.945, 'CMS #bf{#it{Preliminary}}'),
                  (0.60, 0.945, '#bf{%s fb^{-1} (13 TeV)}'%lumi ),
                  (0.62,0.55,'SF_{W} = %.2f'%SF_W),
                  (0.62,0.50,"SF_{top} = %.2f"%SF_top)
                ]
                return [tex.DrawLatex(*l) for l in lines]
            drawObjects = drawObjects( isData=True, lumi=lumi )

            plotting.draw(
                Plot.fromHisto(name = '%s_nBTagFitRes_nice_%s'%(year, MET_string), histos = histos, texX = "N_{b}", texY = "Events"),
                plot_directory = plot_path,
                #yRange = (0.0,6.5),
                #ratio = {'histos': [(1, 0)], 'texY': 'Data / pred', 'yRange':(0.1,1.9)},
                logX = False, logY = False, sorting = False,
                drawObjects = drawObjects,
            )

            
            #latex1 = ROOT.TLatex()
            #latex1.SetNDC()
            #latex1.SetTextSize(0.04)
            #latex1.SetTextAlign(11)

            #latex1.DrawLatex(0.16,0.96,'CMS #bf{#it{Preliminary}}')
            #latex1.DrawLatex(0.71,0.96,"#bf{%s fb^{-1} (13 TeV)}"%lumi)

            #latex2 = ROOT.TLatex()
            #latex2.SetNDC()
            #latex2.SetTextSize(0.04)
            #latex2.SetTextAlign(11)
            #latex1.DrawLatex(0.62,0.55,'SF_{W} = %.2f'%SF_W)
            #latex1.DrawLatex(0.62,0.50,"SF_{top} = %.2f"%SF_top)

            #can.Print('./%s_nBTagFitRes_nice_%s.png'%(year, MET_string))
            #can.Print('./%s_nBTagFitRes_nice_%s.pdf'%(year, MET_string))
            #can.Print('./%s_nBTagFitRes_nice_%s.root'%(year, MET_string))


    results = sorted(yields_WJets_0b_postFit)
    
    #print "Central:", results[50]
    #print "Min:", results[15]
    #print "Max:", results[83]

    WX_contrib = max((WX2D_pos.GetBinContent(metBin+1, 3)+WX2D_neg.GetBinContent(metBin+1, 3)), 0)
    if WX_contrib > 0: WX_contrib = af(WX_contrib, math.sqrt(WX2D_pos.GetBinError(metBin+1, 3)**2+WX2D_neg.GetBinError(metBin+1, 3)**2))
    else: WX_contrib = af(0, 0.001)
    R_W_denom   = af(WJets2D_pos.GetBinContent(metBin+1, 3), WJets2D_pos.GetBinError(metBin+1, 3)) + af(WJets2D_neg.GetBinContent(metBin+1, 3), WJets2D_neg.GetBinError(metBin+1, 3)) + WX_contrib
    R_W_num     = af(WJets2D_pos.GetBinContent(metBin+1, 1), WJets2D_pos.GetBinError(metBin+1, 1)) + af(WJets2D_neg.GetBinContent(metBin+1, 1), WJets2D_neg.GetBinError(metBin+1, 1)) + af(WX2D_pos.GetBinContent(metBin+1, 1), WX2D_pos.GetBinError(metBin+1, 1)) + af(WX2D_neg.GetBinContent(metBin+1, 1), WX2D_neg.GetBinError(metBin+1, 1))
    R_W         = R_W_denom/R_W_num
    y_inclH = af(WJets2D_Higgs.GetBinContent(metBin+1, 2), WJets2D_Higgs.GetBinError(metBin+1, 2)) + af(WJets2D_Higgs.GetBinContent(metBin+1, 1), WJets2D_Higgs.GetBinError(metBin+1, 1))
    R_1H = af(WJets2D_Higgs.GetBinContent(metBin+1, 2), WJets2D_Higgs.GetBinError(metBin+1, 2))/y_inclH
    R_0H = af(WJets2D_Higgs.GetBinContent(metBin+1, 1), WJets2D_Higgs.GetBinError(metBin+1, 1))/y_inclH
    numerator = af(WJets2D_Boosted.GetBinContent(metBin+1,1)+WJets2D_Boosted.GetBinContent(metBin+1,2), 0.01) # stat uncertainty of W+jets already in R_W
    R_1H_mistag = af(WJets2D_BoostedRew.GetBinContent(metBin+1,2), WJets2D_BoostedRew.GetBinError(metBin+1,2))/numerator
    R_0H_mistag = af(1,0.01) - R_1H_mistag
    R_H_unc = af(1.0, 0.10)
    R_W_unc = af(1.0, 0.30)
    W_pred[metBins[metBin]] = {'0b':W_0b, 'SF_W':SF_W, 'SF_top':SF_top, 'R_W':R_W, '0b_all':results, '2b':W_0b*R_W, '2b,1H':W_0b*R_W*R_1H, '2b,0H':W_0b*R_W*R_0H,
        '2b,1Hm':W_0b*R_W*R_1H_mistag, '2b,0Hm':W_0b*R_W*R_0H_mistag,
        '2b,1Hm_unc':W_0b*R_W*R_1H_mistag*R_H_unc*R_W_unc, '2b,0Hm_unc':W_0b*R_W*R_0H_mistag*R_H_unc*R_W_unc,
    }
    
    # need to set the uncertainty for 0 to 1.8410*weight -> which weight? inclusive Fall17 W+jets sample has weight of >20 for 41.5/fb. Need to check!
    
    #FIXME
    # no delta uncertainty in here yet! 
    print "R_W:", R_W

pickle.dump(W_pred, file("estimate_%s.pkl"%year, 'w'))

WJetsHist_pred = ROOT.TH1F('WJetsHist_pred', '', 8,0,8)
TTJetsHist_pred = ROOT.TH1F('TTJetsHist_pred', '', 8,0,8)
DataHist_obs = ROOT.TH1F('Data_obs', '', 8,0,8)

## needed for legend
WJetsHist_pred.SetLineColor(ROOT.kGreen+1)
WJetsHist_pred.SetLineWidth(2)

# style for plots
WJetsHist_pred.style = styles.lineStyle(ROOT.kGreen+1, width=2)
TTJetsHist_pred.style = styles.fillStyle(ROOT.kBlue+1)
DataHist_obs.style = styles.errorStyle(ROOT.kBlack)

WJetsHist_pred.legendText = "W+jets (predicted)"
TTJetsHist_pred.legendText = "tt+jets (MC)"
DataHist_obs.legendText = "Data %s"%year

for i,metBin in enumerate(metBins):
    TTJetsHist_pred.SetBinContent(2*i+1, TTJets2D_Higgs.GetBinContent(i+1, 1))
    TTJetsHist_pred.SetBinError(2*i+1, TTJets2D_Higgs.GetBinError(i+1, 1))
    TTJetsHist_pred.SetBinContent(2*i+2, TTJets2D_Higgs.GetBinContent(i+1, 2))
    TTJetsHist_pred.SetBinError(2*i+2, TTJets2D_Higgs.GetBinError(i+1, 2))
    WJetsHist_pred.SetBinContent(2*i+1, W_pred[metBin]['2b,0Hm_unc'].central)
    WJetsHist_pred.SetBinError(2*i+1, W_pred[metBin]['2b,0Hm_unc'].up)
    WJetsHist_pred.SetBinContent(2*i+2, W_pred[metBin]['2b,1Hm_unc'].central)
    WJetsHist_pred.SetBinError(2*i+2, W_pred[metBin]['2b,1Hm_unc'].up)
    DataHist_obs.SetBinContent(i+1, Data2D_pos.GetBinContent(i+1,3)+Data2D_neg.GetBinContent(i+1,3))

binLabels = ['0H','1H']*4

def setBinLabels( hist ):
    for i in range(1, hist.GetNbinsX()+1):
        hist.GetXaxis().SetBinLabel(i, binLabels[i-1])

def drawDivisions(nRegions):
    #print len(regions)
    min = 0.15
    max = 0.95
    diff = (max-min) / nRegions
    lines = []
    lines2 = []
    line = ROOT.TLine()
#   line.SetLineColor(38)
    line.SetLineWidth(1)
    line.SetLineStyle(2)
    lines  = [ (min+2*diff,  0.15, min+2*diff, 0.90) ]
    lines += [ (min+4*diff,  0.15, min+4*diff, 0.80) ]
    lines += [ (min+6*diff,  0.15, min+6*diff, 0.80) ]
    return [line.DrawLineNDC(*l) for l in lines] + [tex.DrawLatex(*l) for l in []] + [tex2.DrawLatex(*l) for l in lines2]

def drawLabelsRot( nRegions ):
    tex = ROOT.TLatex()
    tex.SetNDC()
    tex.SetTextSize(0.032)
    tex.SetTextAngle(90)
    tex.SetTextAlign(12) # align right
    min = 0.15
    max = 0.95
    diff = (max-min) / nRegions
    #lines = [(min+(i*4+2.7)*diff, 0.545 if i<3 else 0.285,  r.texStringForVar('dl_mt2blbl')) for i, r in enumerate(regions[::2]) if i < 6]
    lines  = [(min+(1.5)*diff, 0.5, "E_{T}^{miss} 125-200 GeV")]
    lines += [(min+(3.5)*diff, 0.5, "E_{T}^{miss} 200-300 GeV")]
    lines += [(min+(5.5)*diff, 0.5, "E_{T}^{miss} 300-400 GeV")]
    lines += [(min+(7.5)*diff, 0.5, "E_{T}^{miss} #geq 400 GeV")]
    return [tex.DrawLatex(*l) for l in lines] 

def getLegendRight():
    leg = ROOT.TLegend(0.60,0.80,0.90,0.88)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetShadowColor(ROOT.kWhite)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.035)
    leg.AddEntry(WJetsHist_pred, 'W+jets (pred)', 'l')
    leg.AddEntry(boxes[0], 'Uncertainty', 'f')
    return [leg]

def drawObjects( isData=False, lumi=36. ):
    tex = ROOT.TLatex()
    tex.SetNDC()
    tex.SetTextSize(0.05)
    tex.SetTextAlign(11) # align right
    lines = [
      (0.15, 0.945, 'CMS Simulation') if not isData else (0.15, 0.945, 'CMS #bf{#it{Preliminary}}'),
      (0.60, 0.945, '#bf{%s fb^{-1} (13 TeV)}'%lumi )
    ]
    return [tex.DrawLatex(*l) for l in lines]

boxes = []
ratio_boxes = []
for ib in range(1,9):
    #val = TTJetsHist_pred.GetBinContent(ib) + WJetsHist_pred.GetBinContent(ib)
    val = WJetsHist_pred.GetBinContent(ib)
    if val<0: continue
    #sys = math.sqrt(TTJetsHist_pred.GetBinError(ib)**2 + WJetsHist_pred.GetBinError(ib)**2)
    sys = WJetsHist_pred.GetBinError(ib)
    if val > 0:
        sys_rel = sys/val
    else:
        sys_rel = 1.
    
    # uncertainty box in main histogram
    box = ROOT.TBox( WJetsHist_pred.GetXaxis().GetBinLowEdge(ib),  max([0.006, val-sys]), WJetsHist_pred.GetXaxis().GetBinUpEdge(ib), max([0.006, val+sys]) )
    box.SetLineColor(ROOT.kGray+1)
    box.SetFillStyle(3244)
    box.SetFillColor(ROOT.kGray+1)
    
    ## uncertainty box in ratio histogram
    #r_box = ROOT.TBox( hists[2016]['total_background'].GetXaxis().GetBinLowEdge(ib),  max(0.11, 1-sys_rel), hists[2016]['total_background'].GetXaxis().GetBinUpEdge(ib), min(1.9, 1+sys_rel) )
    #r_box.SetLineColor(ROOT.kGray+1)
    #r_box.SetFillStyle(3244)
    #r_box.SetFillColor(ROOT.kGray+1)

    boxes.append( box )
    #hists[2016]['total_background'].SetBinError(ib, 0)
    #ratio_boxes.append( r_box )

plot_path = './'

plotting.draw(
    #Plot.fromHisto(name = 'Closure_%s'%year, histos = [[ WJetsHist_pred,TTJetsHist_pred ], [ DataHist_obs] ], texX = "p_{T}^{miss} bins", texY = "Events"),
    Plot.fromHisto(name = 'Closure_%s'%year, histos = [ [ WJetsHist_pred] ], texX = "", texY = "Events"),
    plot_directory = plot_path,
    yRange = (0.0,1.0),
    legend = None,
    #ratio = {'histos': [(1, 0)], 'texY': 'Data / pred', 'yRange':(0.1,1.9)},
    logX = False, logY = False, sorting = False,
    histModifications = [ lambda h: setBinLabels(h) ],
    drawObjects = boxes + drawDivisions(8) + drawLabelsRot(8) + getLegendRight() + drawObjects(isData=True, lumi=lumi),
)

plotting.draw(
    #Plot.fromHisto(name = 'Closure_log_%s'%year, histos = [[ WJetsHist_pred,TTJetsHist_pred ], [ DataHist_obs] ], texX = "p_{T}^{miss} bins", texY = "Events"),
    Plot.fromHisto(name = 'Closure_log_%s'%year, histos = [ [WJetsHist_pred] ], texX = "", texY = "Events"),
    plot_directory = plot_path,
    yRange = (0.01,20),
    legend = None,
    #ratio = {'histos': [(1, 0)], 'texY': 'Data / pred', 'yRange':(0.1,1.9)},
    logX = False, logY = True, sorting = False,
    histModifications = [ lambda h: setBinLabels(h) ],
    drawObjects = boxes + drawDivisions(8) + drawLabelsRot(8) + getLegendRight() + drawObjects(isData=True, lumi=lumi),
)

## systematics
#selectionString_2l  = dilepSelection+"&&pass&&nvetoleps==2&&PassTrackVeto&&PassTauVeto&&ngoodjets>=2&&mct>200&&mbb>90&&mbb<150&&(lep1_pdgid*lep2_pdgid<0)"
selectionString_2l  = dilepSelection+"&&pass&&nvetoleps==2&&PassTrackVeto&&PassTauVeto&&ngoodjets==2&&mct>200&&mbb>90&&mbb<150&&(lep1_pdgid*lep2_pdgid<0)"
invariantMass       = "sqrt(2*leps_pt[0]*leps_pt[1]*(cosh(leps_eta[0]-leps_eta[1])-cos(leps_phi[0]-leps_phi[1])))"
selectionString_2l += "&&abs(%s-91.2)<5"%invariantMass

selectionString_2l_loose  = dilepSelection+"&&pass&&nvetoleps==2&&PassTrackVeto&&PassTauVeto&&ngoodjets==2&&mbb>90&&mbb<150&&(lep1_pdgid*lep2_pdgid<0)"
selectionString_2l_loose += "&&abs(%s-91.2)<5"%invariantMass

Data.setSelectionString("pass&&(HLT_SingleEl==1||HLT_SingleMu==1)")

## first double ratio for mbb extrapolation - only mbb selection to be determined
print "Working on b-tagging double ratio"
mc_2b = DYJets.getYieldFromDraw(selectionString_2l+"&&ngoodbtags==2",'weight * w_pu *'+yearWeight)
mc_0b = DYJets.getYieldFromDraw(selectionString_2l+"&&ngoodbtags==0",'weight * w_pu *'+yearWeight)
data_2b = Data.getYieldFromDraw(selectionString_2l+"&&ngoodbtags==2",'(1)')
data_0b = Data.getYieldFromDraw(selectionString_2l+"&&ngoodbtags==0",'(1)')

mc_2b = af(mc_2b['val'], mc_2b['sigma'])
mc_0b = af(mc_0b['val'], mc_0b['sigma'])
data_2b = af(data_2b['val'], data_2b['sigma'])
data_0b = af(data_0b['val'], data_0b['sigma'])

delta_b = (data_2b/data_0b)/(mc_2b/mc_0b)
print "2l b-tag double ratio:", delta_b

## second double ratio for higgs tagging - under devolpment
mc_1h = DYJets.getYieldFromDraw(selectionString_2l+"&&ngoodbtags>=2&&Sum$(ak8pfjets_deepdisc_hbb>0.8)==1",'weight * w_pu *'+lumi)
mc_rew = DYJets.getYieldFromDraw(selectionString_2l+"&&ngoodbtags>=2&&Sum$(ak8pfjets_pt>0)==1",'weight * w_pu *'+lumi+'*'+reweighting)
mc_0h = DYJets.getYieldFromDraw(selectionString_2l+"&&ngoodbtags>=2&&Sum$(ak8pfjets_deepdisc_hbb>0.8)==0",'weight * w_pu *'+lumi)

data_1h = Data.getYieldFromDraw(selectionString_2l+"&&ngoodbtags>=2&&Sum$(ak8pfjets_deepdisc_hbb>0.8)==1",'(1)')
data_0h = Data.getYieldFromDraw(selectionString_2l+"&&ngoodbtags>=2&&Sum$(ak8pfjets_deepdisc_hbb>0.8)==0",'(1)')

mc_1h = af(mc_1h['val'], mc_1h['sigma'])
mc_0h = af(mc_0h['val'], mc_0h['sigma'])
data_1h = af(data_1h['val'], data_1h['sigma'])
data_0h = af(data_0h['val'], data_0h['sigma'])

print "MC 1h/incl:", (mc_1h/mc_2b)
print "MC 0h/incl:", (mc_0h/mc_2b)
print "2l Higgs-tag double ratio:", (data_1h/data_0h)/(mc_1h/mc_0h)


## third double ratio for higgs tagging - under devolpment
mc_1h  = DYJets.getYieldFromDraw(selectionString_2l_loose+"&&ngoodbtags>=2&&Sum$(ak8pfjets_deepdisc_hbb>0.8)==1",'weight * w_pu *'+lumi)
mc_rew = DYJets.getYieldFromDraw(selectionString_2l_loose+"&&ngoodbtags>=2&&Sum$(ak8pfjets_pt>0)==1",'weight * w_pu *'+lumi+'*'+reweighting)
mc_0h  = DYJets.getYieldFromDraw(selectionString_2l_loose+"&&ngoodbtags>=2&&Sum$(ak8pfjets_deepdisc_hbb>0.8)==0",'weight * w_pu *'+lumi)

data_1h = Data.getYieldFromDraw(selectionString_2l_loose+"&&ngoodbtags>=2&&Sum$(ak8pfjets_deepdisc_hbb>0.8)==1",'(1)')
data_0h = Data.getYieldFromDraw(selectionString_2l_loose+"&&ngoodbtags>=2&&Sum$(ak8pfjets_deepdisc_hbb>0.8)==0",'(1)')

mc_1h = af(mc_1h['val'], mc_1h['sigma'])
mc_0h = af(mc_0h['val'], mc_0h['sigma'])
data_1h = af(data_1h['val'], data_1h['sigma'])
data_0h = af(data_0h['val'], data_0h['sigma'])

print "MC 1h/incl:", (mc_1h/mc_2b)
print "MC 0h/incl:", (mc_0h/mc_2b)
print "2l Higgs-tag double ratio:", (data_1h/data_0h)/(mc_1h/mc_0h)



## Closure test

#print "W+jets templates"
#WJets2D_SB = WJets.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString_SB+"&&%s>0"%pdgid, weightString='weight * w_pu *'+lumi, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
#
#print "tt+jets templates"
#TTJets2D_SB = TTJets.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString_SB, weightString='weight * w_pu *'+lumi, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
#
#print "data templates"
#Data2D_SB = Data.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString_SB+"&&%s>0"%pdgid, weightString='(1)', binningIsExplicit=True) # x-pfmet, y-ngoodbtags
#
#for i,metBin in enumerate(metBins):
#    R_W_1b = af(WJets2D_SB.GetBinContent(i+1, 2), WJets2D_SB.GetBinError(i+1, 2))/af(WJets2D_SB.GetBinContent(i+1, 1), WJets2D_SB.GetBinError(i+1, 1))
#    
#    SM_pred = af(TTJets2D_SB.GetBinContent(i+1, 2),TTJets2D_SB.GetBinError(i+1, 2)) + R_W_1b*W_pred[metBin]['0b']
#    print SM_pred
#    print Data2D_SB.GetBinContent(i+1, 2)

    


