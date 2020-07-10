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

from WH_studies.Tools.u_float import u_float as uf

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

year = 'combined'

dataDir_16 = '/home/users/dspitzba/wh_babies/babies_v33_4_2020_05_27/'
mcDir_16   = '/home/users/dspitzba/wh_babies/babies_v33_4_2020_05_27/s16v3/'
dataDir_17 = '/home/users/dspitzba/wh_babies/babies_v33_4_2020_05_27/'
mcDir_17   = '/home/users/dspitzba/wh_babies/babies_v33_4_2020_05_27/f17v2/'
dataDir_18 = '/home/users/dspitzba/wh_babies/babies_v33_4_2020_05_27/'
mcDir_18   = '/home/users/dspitzba/wh_babies/babies_v33_4_2020_05_27/a18v1/'


# w+jets
WJetsDirs_2016 =   glob.glob(mcDir_16+'slim_W*JetsToLNu_s16v3*.root') \
                + glob.glob(mcDir_16+"slim*W*Jets_NuPt200_s16v*.root")
WJetsDirs_2017   = glob.glob(mcDir_17+"*slim_W*JetsToLNu_f17v2*")\
                + glob.glob(mcDir_17+"slim*W*Jets_NuPt200_f17v*.root")
WJetsDirs_2018   = glob.glob(mcDir_18+'slim*W*JetsToLNu_a18v1*.root') \
                + glob.glob(mcDir_18+'slim*W*Jets_NuPt200_a18v*.root')


# WX
WXDirs_2016  = glob.glob(mcDir_16+'slim*WW*.root') \
            + glob.glob(mcDir_16+'slim*WZ*.root') \
            + glob.glob(mcDir_16+'slim*ZZ*.root') 
WXDirs_2017  = glob.glob(mcDir_17+'slim*WW*.root') \
            + glob.glob(mcDir_17+'slim*WZ*.root') \
            + glob.glob(mcDir_17+'slim*ZZ*.root') 
WXDirs_2018  = glob.glob(mcDir_18+'slim*WW*.root') \
            + glob.glob(mcDir_18+'slim*WZ*.root') \
            + glob.glob(mcDir_18+'slim*ZZ*.root') 



# tt/t
TTJetsDirs_2016 = glob.glob(mcDir_16+'slim*TTJets_1lep_top_s16v3*.root') \
                + glob.glob(mcDir_16+'slim*TTJets_1lep_tbar_s16v3*.root') \
                + glob.glob(mcDir_16+'slim*TTJets_1lep_*met150*.root') \
                + glob.glob(mcDir_16+'slim*TTJets_2lep_s16v3*.root')\
                + glob.glob(mcDir_16+'slim*TTJets_2lep_*met150*.root')\
                + glob.glob(mcDir_16+'slim*_ST_*.root') \
                + glob.glob(mcDir_16+'slim*TTW*.root') \
                + glob.glob(mcDir_16+'slim*TTZ*.root')
TTJetsDirs_2017 = glob.glob(mcDir_17+'slim*TTJets_1lep_top_f17v2*.root') \
                + glob.glob(mcDir_17+'slim*TTJets_1lep_tbar_f17v2*.root') \
                + glob.glob(mcDir_17+'slim*TTJets_1lep_*met150*.root') \
                + glob.glob(mcDir_17+'slim*TTJets_2lep_f17v2*.root')\
                + glob.glob(mcDir_17+'slim*TTJets_2lep_*met150*.root')\
                + glob.glob(mcDir_17+'slim*_ST_*.root')\
                + glob.glob(mcDir_17+'slim*TTW*.root') \
                + glob.glob(mcDir_17+'slim*TTZ*.root')
TTJetsDirs_2018 = glob.glob(mcDir_18+'slim*TTJets_1lep_top_a18v1*.root') \
                + glob.glob(mcDir_18+'slim*TTJets_1lep_tbar_a18v1*.root') \
                + glob.glob(mcDir_18+'slim*TTJets_1lep_*met150*.root') \
                + glob.glob(mcDir_18+'slim*TTJets_2lep_a18v1*.root')\
                + glob.glob(mcDir_18+'slim*TTJets_2lep_*met150*.root')\
                + glob.glob(mcDir_18+'slim*_ST_*.root') \
                + glob.glob(mcDir_18+'slim*TTW*.root') \
                + glob.glob(mcDir_18+'slim*TTZ*.root')





lumi = '137'

WJets = Sample.fromFiles('WJets', WJetsDirs_2016 + WJetsDirs_2017 + WJetsDirs_2018, "t")
WJets.setSelectionString("stitch")

WX = Sample.fromFiles('WX', WXDirs_2016 + WXDirs_2017 + WXDirs_2018, "t")

TTJets = Sample.fromFiles('TTJets', TTJetsDirs_2016 + TTJetsDirs_2017 + TTJetsDirs_2018, 't')
TTJets.setSelectionString("stitch")

DataDirs_2016   = glob.glob(dataDir_16+"slim*data_2016*met*.root")\
                + glob.glob(dataDir_16+"slim*data_2016*singlemu*.root")\
                + glob.glob(dataDir_16+"slim*data_2016*singleel*.root")
DataDirs_2017   = glob.glob(dataDir_17+"slim*data_2017*met*.root")\
                + glob.glob(dataDir_17+"slim*data_2017*singlemu*.root")\
                + glob.glob(dataDir_17+"slim*data_2017*singleel*.root")
DataDirs_2018   = glob.glob(dataDir_18+"slim*data_2018*met*.root")\
                + glob.glob(dataDir_18+"slim*data_2018*singlemu*.root")\
                + glob.glob(dataDir_18+"slim*data_2018*egamma*.root")

Data = Sample.fromFiles('Data', DataDirs_2016 + DataDirs_2017 + DataDirs_2018, 't')
Data.setSelectionString("pass&&(HLT_SingleEl==1||HLT_SingleMu==1) && (ngoodbtags<2||mbb<90||mbb>150)")


# CR selection without b-tags
WHSelection     = "(Sum$(abs(lep1_pdgid)==11&&(leps_pt[0]>30&&(lep1_relIso*leps_pt[0])<5)||abs(lep1_pdgid)==13&&(leps_pt[0]>25&&(lep1_relIso*leps_pt[0])<5&&abs(leps_eta[0])<2.1))+"
WHSelection    += "Sum$(abs(lep2_pdgid)==11&&(leps_pt[1]>30&&(lep2_relIso*leps_pt[1])<5)||abs(lep2_pdgid)==13&&(leps_pt[1]>25&&(lep2_relIso*leps_pt[1])<5&&abs(leps_eta[1])<2.1)))==1"
#selectionString = WHSelection+"&&pass&&nvetoleps==1&&PassTrackVeto&&PassTauVeto&&ngoodjets==2&&pfmet>125&&mt_met_lep>150&&mct>200&&mbb>90&&mbb<150"
selectionString = WHSelection+"&&pass&&nvetoleps==1&&PassTrackVeto&&PassTauVeto&&ngoodjets==3&&pfmet>125&&mt_met_lep>150&&mct>200&&mbb>90&&mbb<150"
#selectionString += "&&((year==2016)*Sum$(ak4pfjets_deepCSV<0.6321&&ak4pfjets_pt>300) + (year==2017)*Sum$(ak4pfjets_deepCSV<0.4941&&ak4pfjets_pt>300) + (year==2018)*Sum$(ak4pfjets_deepCSV<0.4184&&ak4pfjets_pt>300))==0"

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

# for systematics
reweight = '(1)'
#reweight = 'w_btagHFDown'

histogramPickle = 'histograms_%s_3jet.pkl'%(year)
#histogramPickle = 'histograms_%s%s_2jet.pkl'%(year, reweight)

yearWeight = "((year==2016)*35.9+((year==2017)*41.6)+((year==2018)*59.7))" # only need weight*w_pu in addition

if not os.path.isfile(histogramPickle):

    weights = '*'.join(['weight', 'w_pu', yearWeight] + [reweight])

    print "W+jets templates"
    WJets2D_pos = WJets.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString+"&&%s>0"%pdgid, weightString=weights, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
    WJets2D_neg = WJets.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString+"&&%s<0"%pdgid, weightString=weights, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
    
    WX2D_pos = WX.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString+"&&%s>0"%pdgid, weightString=weights, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
    WX2D_neg = WX.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString+"&&%s<0"%pdgid, weightString=weights, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
    
    
    print "tt+jets templates"
    TTJets2D = TTJets.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString, weightString=weights, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
    
    print "data templates"
    Data2D_pos = Data.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString+"&&%s>0"%pdgid, weightString='(1)', binningIsExplicit=True) # x-pfmet, y-ngoodbtags
    Data2D_neg = Data.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString+"&&%s<0"%pdgid, weightString='(1)', binningIsExplicit=True) # x-pfmet, y-ngoodbtags

    histograms = {'WJets2D_pos':WJets2D_pos, 'WJets2D_neg':WJets2D_neg, 'WX2D_pos':WX2D_pos, 'WX2D_neg':WX2D_neg, 'TTJets2D':TTJets2D, 'Data2D_pos':Data2D_pos, 'Data2D_neg':Data2D_neg}
    pickle.dump(histograms, file(histogramPickle, 'w'))

else:
    histograms = pickle.load(file(histogramPickle))
    WJets2D_pos     = histograms['WJets2D_pos']
    WJets2D_neg     = histograms['WJets2D_neg']
    WX2D_pos        = histograms['WX2D_pos']
    WX2D_neg        = histograms['WX2D_neg']
    TTJets2D        = histograms['TTJets2D']
    Data2D_pos      = histograms['Data2D_pos']
    Data2D_neg      = histograms['Data2D_neg']


metBins = [(125,200), (200,300), (300,400), (400,-1)]

W_pred = {}


for metBin in range(len(metBins)):
    W_pred[metBin] = {}
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
        
        wjets_pos = WJets2D_pos.GetBinContent(metBin+1, i+1) + WX2D_pos.GetBinContent(metBin+1, i+1)
        WJetsHist_pos.SetBinContent(i+1, wjets_pos)
        WJetsHist_pos.SetBinError(i+1,   0.0 * wjets_pos + math.sqrt(WJets2D_pos.GetBinError(metBin+1, i+1)**2 + WX2D_pos.GetBinError(metBin+1, i+1)**2))

        wjets_neg = WJets2D_neg.GetBinContent(metBin+1, i+1) + WX2D_neg.GetBinContent(metBin+1, i+1)
        WJetsHist_neg.SetBinContent(i+1, wjets_neg)
        WJetsHist_neg.SetBinError(i+1,   0.0 * wjets_neg + math.sqrt(WJets2D_neg.GetBinError(metBin+1, i+1)**2 + WX2D_neg.GetBinError(metBin+1, i+1)**2))

        TTJetsHist.SetBinContent(i+1, TTJets2D.GetBinContent(metBin+1, i+1))
        TTJetsHist.SetBinError(i+1,   0.0 * TTJets2D.GetBinContent(metBin+1, i+1) + TTJets2D.GetBinError(metBin+1, i+1))

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
    
    TTJets_prefit = TTJetsHist.GetBinContent(1) + TTJetsHist.GetBinContent(2)
    WJets_pos_prefit = WJetsHist_pos.GetBinContent(1) + WJetsHist_pos.GetBinContent(2)
    WJets_neg_prefit = WJetsHist_neg.GetBinContent(1) + WJetsHist_neg.GetBinContent(2)

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
        
        #Define yields as variable. Starting value, min, max
        yield_WJets_pos     = ROOT.RooRealVar("yield_WJets_pos","yield_WJets_pos",  WJets_pos_prefit, 0.5*WJets_pos_prefit, 1.5*WJets_pos_prefit)
        yield_WJets_neg     = ROOT.RooRealVar("yield_WJets_neg","yield_WJets_neg",  WJets_neg_prefit, 0.5*WJets_neg_prefit, 1.5*WJets_neg_prefit)
        yield_TTJets        = ROOT.RooRealVar("yield_TTJets","yield_TTJets",        TTJets_prefit,    0.5*TTJets_prefit,    1.5*TTJets_prefit)
        
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
            W_0b_fit    = f_pos*pos_val + f_neg*neg_val
            print W_0b_fit
            SF_W    = (pos_val+neg_val) / W_prefit
            print "yield_TTJets, again:",  yield_TTJets.getVal()
            SF_top  = af(yield_TTJets.getVal()*2, yield_TTJets.getErrorHi()*math.sqrt(2)) / tt_prefit
            f_top = af(TTJetsTemp.GetBinContent(1), TTJetsTemp.GetBinError(1))
            tt_0b = f_top*af(yield_TTJets.getVal()*2, yield_TTJets.getErrorHi()*math.sqrt(2))

            W_0b_pred = af(int(DataHist_pos.GetBinContent(1)+DataHist_neg.GetBinContent(1))) - tt_0b
            print af(int(DataHist_pos.GetBinContent(1)+DataHist_neg.GetBinContent(1)))
            print W_0b_pred

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

            Data_postFit = ROOT.TH1F("Data", "", 2, -0.5, 1.5)
            Data_postFit.SetBinContent(1, DataHist_pos.GetBinContent(1)+DataHist_neg.GetBinContent(1))
            Data_postFit.SetBinContent(2, DataHist_pos.GetBinContent(2)+DataHist_neg.GetBinContent(2))
            Data_postFit.style = styles.errorStyle(ROOT.kBlack, markerSize=1, width=1)
            #Data_postFit.SetLineColor(ROOT.kBlack)
            #Data_postFit.SetMarkerColor(ROOT.kBlack)
            #Data_postFit.SetMarkerSize(2)
            #Data_postFit.SetLineColor(ROOT.kBlack)
            Data_postFit.drawOption = 'e1p'
            Data_postFit.legendText = 'Data'
            
            WJetsHist_pos_postFit.style = styles.lineStyle(8, width=2, errors=False)
            TTJetsHist_postFit.style = styles.lineStyle(46, width=2, errors=False)
            Total_postFit.style = styles.lineStyle(ROOT.kBlue+1, width=2, errors=True)
            
            WJetsHist_pos_postFit.legendText = 'W+jets/VV'# (N=%.1f #pm %.1f)'%(W_0b_fit.central, W_0b_fit.up)
            TTJetsHist_postFit.legendText = 'top (postfit)'
            Total_postFit.legendText = 'Total (post-fit)'

            # store values
            W_pred[metBin]['W_0b'] = W_0b_fit
            W_pred[metBin]['tt_0b'] = tt_0b
            W_pred[metBin]['data_0b'] = DataHist_pos.GetBinContent(1)+DataHist_neg.GetBinContent(1)

            # prefit
            WJetsHist_pos.Add(WJetsHist_neg)
            
            WJetsHist_pos.style = styles.lineStyle(8, width=2, dashed=True)
            TTJetsHist.style = styles.lineStyle(46, width=2, dashed=True)

            WJetsHist_pos.legendText = 'W+jets/VV (prefit)'
            TTJetsHist.legendText = 'top (prefit)'

            plot_path = './'

            histos = [[WJetsHist_pos_postFit], [TTJetsHist_postFit], [Total_postFit], [WJetsHist_pos], [TTJetsHist], [Data_postFit] ]

            plotName = '%s_nBTagFitRes_nice_%s_3jet'%(year, MET_string) + reweight

            histos_for_pkl = {'tt_pre':TTJetsHist, 'tt_post':TTJetsHist_postFit, 'data':Data_postFit, 'wjets_pre':WJetsHist_pos, 'wjets_post':WJetsHist_pos_postFit, 'total_post':Total_postFit}

            pickle.dump(histos_for_pkl, file(plotName+'.pkl', 'w'))

            def drawObjects( isData=False, lumi=36 ):
                tex = ROOT.TLatex()
                tex.SetNDC()
                tex.SetTextSize(0.05)
                tex.SetTextAlign(11) # align right
                lines = [
                  (0.08, 0.945, 'CMS Simulation') if not isData else (0.15, 0.945, 'CMS #bf{#it{Preliminary}}'),
                  (0.60, 0.945, '#bf{%s fb^{-1} (13 TeV)}'%lumi ),
                  #(0.62,0.55,'SF_{W} = %.2f'%SF_W),
                  #(0.62,0.50,"SF_{top} = %.2f"%SF_top)
                ]
                return [tex.DrawLatex(*l) for l in lines]
            drawObjects = drawObjects( isData=True, lumi=lumi )

            plotting.draw(
                Plot.fromHisto(name = plotName, histos = histos, texX = "N_{b}", texY = "Events"),
                plot_directory = plot_path,
                #yRange = (0.0,6.5),
                #ratio = {'histos': [(1, 0)], 'texY': 'Data / pred', 'yRange':(0.1,1.9)},
                legend = (0.50,0.88-6*0.04,0.9,0.88),
                logX = False, logY = False, sorting = False,
                drawObjects = drawObjects,
            )

histogramPickle = histogramPickle.replace('histograms', 'results')
pickle.dump(W_pred, file(histogramPickle, 'w'))
