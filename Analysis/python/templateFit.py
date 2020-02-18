'''
Some spaghetti code for W+jets estimation. Will at some point live in a different repository, too.

'''


import ROOT
import glob
import math

from ROOT import RooFit as rf
from RootTools.core.standard import *

from WH_studies.Tools.asym_float import asym_float as af

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

year = 2018

if year == 2016:
    # definitions
    mcDir   = '/home/users/dspitzba/wh_babies/babies_mc_s16v3_v33_4_2019_12_30/'
    dataDir = '/home/users/dspitzba/wh_babies/babies_v33_4_2019_12_30/'
    lumi = '35.9'
    
    # w+jets
    WJetsDirs =   glob.glob(mcDir+'slim_W*JetsToLNu_s16v3*.root') \
                + glob.glob(mcDir+"slim*W*Jets_NuPt200_s16v*.root") \
                + glob.glob(mcDir+'slim*WW*.root') \
                + glob.glob(mcDir+'slim*WZ*.root') \
                + glob.glob(mcDir+'slim*ZZ*.root') \

    WJets = Sample.fromFiles('WJets', WJetsDirs, "t")
    WJets.setSelectionString("stitch")

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
    TTJetsDirs =  glob.glob(mcDir+'slim*TTJets_1lep_top_s16v3*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_tbar_s16v3*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_*met150*.root') \
                + glob.glob(mcDir+'slim*TTJets_2lep_s16v3*.root')\
                + glob.glob(mcDir+'slim*TTJets_2lep_*met150*.root')\
                + glob.glob(mcDir+'slim*_ST_*.root') \
                + glob.glob(mcDir+'slim*TTW*.root') \
                + glob.glob(mcDir+'slim*TTZ*.root')
    
    TTJets = Sample.fromFiles('TTJets', TTJetsDirs, 't')
    TTJets.setSelectionString("stitch")
    
    # diboson + ttV. could also put ttV to tt/t
    DibosonDirs = glob.glob(mcDir+'slim*WW*.root') \
                + glob.glob(mcDir+'slim*WZ*.root') \
                + glob.glob(mcDir+'slim*ZZ*.root') \
                + glob.glob(mcDir+'slim*TTW*.root') \
                + glob.glob(mcDir+'slim*TTZ*.root')
    
    Diboson = Sample.fromFiles('Diboson', DibosonDirs, 't')
    
    # load data, but keep SR blinded
    Data = Sample.fromFiles('Data', glob.glob(dataDir+"*data_2016*.root"), 't')
    Data.setSelectionString("pass&&(HLT_SingleEl==1||HLT_SingleMu==1) && (ngoodbtags<2||mbb<90||mbb>150)")

elif year == 2017:
    # definitions
    mcDir   = '/home/users/dspitzba/wh_babies/babies_mc_f17v2_v33_4_2019_12_30/'
    dataDir = '/home/users/dspitzba/wh_babies/babies_Run2017_v33_4_2019_12_30/'
    lumi = '41.5'
    
    # w+jets
    WJetsDirs   = glob.glob(mcDir+"*slim_W*JetsToLNu_f17v2*")\
                + glob.glob(mcDir+"slim*W*Jets_NuPt200_f17v*.root")\
                + glob.glob(mcDir+'slim*WW*.root') \
                + glob.glob(mcDir+'slim*WZ*.root') \
                + glob.glob(mcDir+'slim*ZZ*.root') \

    WJets = Sample.fromFiles('WJets', WJetsDirs, "t")
    WJets.setSelectionString("stitch")

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
    TTJetsDirs =  glob.glob(mcDir+'slim*TTJets_1lep_top_f17v2*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_tbar_f17v2*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_*met150*.root') \
                + glob.glob(mcDir+'slim*TTJets_2lep_f17v2*.root')\
                + glob.glob(mcDir+'slim*TTJets_2lep_*met150*.root')\
                + glob.glob(mcDir+'slim*_ST_*.root')\
                + glob.glob(mcDir+'slim*TTW*.root') \
                + glob.glob(mcDir+'slim*TTZ*.root')
    
    TTJets = Sample.fromFiles('TTJets', TTJetsDirs, 't')
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
    
    WJetsDirs   = glob.glob(mcDir+'slim*WW*.root') \
                + glob.glob(mcDir+'slim*WZ*.root') \
                + glob.glob(mcDir+'slim*ZZ*.root') \
                + glob.glob(mcDir+'slim*W*JetsToLNu_a18v1*.root') \
                + glob.glob(mcDir+'slim*W*Jets_NuPt200_a18v*.root')

    # w+jets
    WJets = Sample.fromFiles('WJets', WJetsDirs, "t")
    WJets.setSelectionString("stitch")

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
    TTJetsDirs =  glob.glob(mcDir+'slim*TTJets_1lep_top_a18v1*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_tbar_a18v1*.root') \
                + glob.glob(mcDir+'slim*TTJets_1lep_*met150*.root') \
                + glob.glob(mcDir+'slim*TTJets_2lep_a18v1*.root')\
                + glob.glob(mcDir+'slim*TTJets_2lep_*met150*.root')\
                + glob.glob(mcDir+'slim*_ST_*.root') \
                + glob.glob(mcDir+'slim*TTW*.root') \
                + glob.glob(mcDir+'slim*TTZ*.root')
    
    TTJets = Sample.fromFiles('TTJets', TTJetsDirs, 't')
    TTJets.setSelectionString("stitch")
    
    # diboson + ttV. could also put ttV to tt/t
    DibosonDirs = glob.glob(mcDir+'slim*WW*.root') \
                + glob.glob(mcDir+'slim*WZ*.root') \
                + glob.glob(mcDir+'slim*ZZ*.root')
    
    Diboson = Sample.fromFiles('Diboson', DibosonDirs, 't')
    
    # load data, but keep SR blinded
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

print "W+jets templates"
WJets2D_pos = WJets.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString+"&&%s>0"%pdgid, weightString='weight * w_pu *'+lumi, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
WJets2D_neg = WJets.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString+"&&%s<0"%pdgid, weightString='weight * w_pu *'+lumi, binningIsExplicit=True) # x-pfmet, y-ngoodbtags

WJets2D_Higgs = WJets.get2DHistoFromDraw('Sum$(ak8pfjets_deepdisc_hbb>0.8):pfmet', [[125,200,300,400,1000], [-0.5,0.5,10]], selectionString=selectionString+"&&ngoodbtags==2", weightString='weight * w_pu *'+lumi, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
TTJets2D_Higgs = TTJets.get2DHistoFromDraw('Sum$(ak8pfjets_deepdisc_hbb>0.8):pfmet', [[125,200,300,400,1000], [-0.5,0.5,10]], selectionString=selectionString+"&&ngoodbtags==2", weightString='weight * w_pu *'+lumi, binningIsExplicit=True) # x-pfmet, y-ngoodbtags

## fancy reweighting for Higgs tag estimation
reweighting = "((ak8pfjets_pt[0]>170&&ak8pfjets_pt[0]<250)*0.05 + (ak8pfjets_pt[0]>250&&ak8pfjets_pt[0]<300)*0.15 + (ak8pfjets_pt[0]>300&&ak8pfjets_pt[0]<400)*0.27 + (ak8pfjets_pt[0]>400&&ak8pfjets_pt[0]<500)*0.35 + (ak8pfjets_pt[0]>500&&ak8pfjets_pt[0]<750)*0.40 + (ak8pfjets_pt[0]>750)*0.35)"

WJets2D_Boosted = WJets.get2DHistoFromDraw('Sum$(ak8pfjets_pt>170):pfmet', [[125,200,300,400,1000], [-0.5,0.5,10]], selectionString=selectionString+"&&ngoodbtags==2", weightString='weight * w_pu *'+lumi, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
WJets2D_BoostedRew = WJets.get2DHistoFromDraw('Sum$(ak8pfjets_pt>170):pfmet', [[125,200,300,400,1000], [-0.5,0.5,10]], selectionString=selectionString+"&&ngoodbtags==2", weightString='weight * w_pu *'+lumi+'*'+reweighting, binningIsExplicit=True) # x-pfmet, y-ngoodbtags
TTJets2D_Boosted = TTJets.get2DHistoFromDraw('Sum$(ak8pfjets_pt>170):pfmet', [[125,200,300,400,1000], [-0.5,0.5,10]], selectionString=selectionString+"&&ngoodbtags==2", weightString='weight * w_pu *'+lumi, binningIsExplicit=True) # x-pfmet, y-ngoodbtags

print "tt+jets templates"
TTJets2D = TTJets.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString, weightString='weight * w_pu *'+lumi, binningIsExplicit=True) # x-pfmet, y-ngoodbtags

print "data templates"
Data2D_pos = Data.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString+"&&%s>0"%pdgid, weightString='(1)', binningIsExplicit=True) # x-pfmet, y-ngoodbtags
Data2D_neg = Data.get2DHistoFromDraw('ngoodbtags:pfmet', [[125,200,300,400,1000], [-0.5,0.5,1.5,2.5,3.5]], selectionString=selectionString+"&&%s<0"%pdgid, weightString='(1)', binningIsExplicit=True) # x-pfmet, y-ngoodbtags

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
    
    for x,y in [(WJets2D_pos,WJetsHist_pos), (WJets2D_neg,WJetsHist_neg), (TTJets2D,TTJetsHist), (Data2D_pos,DataHist_pos), (Data2D_neg,DataHist_neg)]:
        for i in range(2):
            y.SetBinContent(i+1, x.GetBinContent(metBin+1, i+1))
            y.SetBinError(i+1, x.GetBinError(metBin+1, i+1))
            #print y.GetBinContent(i+1)
            #print y.GetBinError(i+1)

    ## get prefit histograms. could cache this?
    #print "W+jets templates"
    #WJetsHist_pos   = WJets.get1DHistoFromDraw('ngoodbtags', [2,-0.5,1.5], selectionString=selectionString+"&&%s>0"%pdgid, weightString='weight * w_pu *'+lumi)
    #WJetsHist_neg   = WJets.get1DHistoFromDraw('ngoodbtags', [2,-0.5,1.5], selectionString=selectionString+"&&%s<0"%pdgid, weightString='weight * w_pu *'+lumi)
    #print "tt+jets templates"
    #TTJetsHist      = TTJets.get1DHistoFromDraw('ngoodbtags', [2,-0.5,1.5], selectionString=selectionString, weightString='weight * w_pu *'+lumi)
    ##print "diboson templates"
    ##DibosonHist_pos = Diboson.get1DHistoFromDraw('ngoodbtags', [2,-0.5,1.5], selectionString=selectionString+"&&%s>0"%pdgid, weightString='weight * w_pu *'+lumi)
    ##DibosonHist_neg = Diboson.get1DHistoFromDraw('ngoodbtags', [2,-0.5,1.5], selectionString=selectionString+"&&%s<0"%pdgid, weightString='weight * w_pu *'+lumi)
    #print "data templates"
    #DataHist_pos    = Data.get1DHistoFromDraw('ngoodbtags', [2,-0.5,1.5], selectionString=selectionString+"&&%s>0"%pdgid, weightString='(1)')
    #DataHist_neg    = Data.get1DHistoFromDraw('ngoodbtags', [2,-0.5,1.5], selectionString=selectionString+"&&%s<0"%pdgid, weightString='(1)')
    
    print "## Prefit Values ##"
    print WJetsHist_pos.GetBinContent(1), WJetsHist_pos.GetBinContent(2)
    print WJetsHist_neg.GetBinContent(1), WJetsHist_neg.GetBinContent(2)
    print TTJetsHist.GetBinContent(1), TTJetsHist.GetBinContent(2)
    #print DibosonHist_pos.GetBinContent(1), DibosonHist_pos.GetBinContent(2)
    #print DibosonHist_neg.GetBinContent(1), DibosonHist_neg.GetBinContent(2)
    print DataHist_pos.GetBinContent(1), DataHist_pos.GetBinContent(2)
    print DataHist_neg.GetBinContent(1), DataHist_neg.GetBinContent(2)
    
    # get templates (= normalized prefit histograms)
    WJetsTemp_pos = WJetsHist_pos.Clone()
    WJetsTemp_pos.Scale(1./WJetsTemp_pos.Integral())
    WJetsTemp_neg = WJetsHist_neg.Clone()
    WJetsTemp_neg.Scale(1./WJetsTemp_neg.Integral())
    TTJetsTemp = TTJetsHist.Clone()
    TTJetsTemp.Scale(1./TTJetsTemp.Integral())
    #DibosonTemp_pos = DibosonHist_pos.Clone()
    #DibosonTemp_pos.Scale(1./DibosonTemp_pos.Integral())
    #DibosonTemp_neg = DibosonHist_neg.Clone()
    #DibosonTemp_neg.Scale(1./DibosonTemp_neg.Integral())
    
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
    #    diboson_hist_pos    = ROOT.RooDataHist("diboson", "diboson", ROOT.RooArgList(x), DibosonHist_pos)
    #    diboson_hist_neg    = ROOT.RooDataHist("diboson", "diboson", ROOT.RooArgList(x), DibosonHist_neg)
        
        #Define yields as variable
        yield_WJets_pos     = ROOT.RooRealVar("yield_WJets_pos","yield_WJets_pos",0.1,0,10**5)
        yield_WJets_neg     = ROOT.RooRealVar("yield_WJets_neg","yield_WJets_neg",0.1,0,10**5)
        yield_TTJets        = ROOT.RooRealVar("yield_TTJets","yield_TTJets",0.1,0,10**5)
    #    yield_Diboson_pos   = ROOT.RooRealVar("yield_Diboson_pos","yield_Diboson_pos", DibosonHist_pos.Integral(), DibosonHist_pos.Integral(), DibosonHist_pos.Integral())
    #    yield_Diboson_neg   = ROOT.RooRealVar("yield_Diboson_neg","yield_Diboson_neg", DibosonHist_neg.Integral(), DibosonHist_neg.Integral(), DibosonHist_neg.Integral())
    #    yield_Diboson_pos.setConstant() # to be tested
    #    yield_Diboson_neg.setConstant() # to be tested
        
        #Make PDF from MC histograms
        model_WJets_pos     = ROOT.RooHistPdf("model_WJets_pos", "model_WJets_pos", ROOT.RooArgSet(x), wjets_hist_pos)
        model_WJets_neg     = ROOT.RooHistPdf("model_WJets_neg", "model_WJets_neg", ROOT.RooArgSet(x), wjets_hist_neg)
        model_TTJets        = ROOT.RooHistPdf("model_TTJets", "model_TTJets", ROOT.RooArgSet(x), ttjets_hist)
    #    model_Diboson_pos   = ROOT.RooHistPdf("model_Diboson_pos", "model_Diboson_pos", ROOT.RooArgSet(x), diboson_hist_pos)
    #    model_Diboson_neg   = ROOT.RooHistPdf("model_Diboson_neg", "model_Diboson_neg", ROOT.RooArgSet(x), diboson_hist_neg)
        
        #Make combined PDF of all MC Backgrounds
        #model_total_pos = ROOT.RooAddPdf("model_total_pos", "model_total_pos", ROOT.RooArgList(model_WJets_pos, model_TTJets, model_Diboson_pos), ROOT.RooArgList(yield_WJets_pos, yield_TTJets, yield_Diboson_pos))
        #model_total_neg = ROOT.RooAddPdf("model_total_neg", "model_total_neg", ROOT.RooArgList(model_WJets_neg, model_TTJets, model_Diboson_neg), ROOT.RooArgList(yield_WJets_neg, yield_TTJets, yield_Diboson_neg))
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
        #print "yield_Dibosoon_pos:" , yield_Diboson_pos.getVal()
        #print "yield_Dibosoon_neg:" , yield_Diboson_neg.getVal()
        
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
            f_pos = af(WJetsTemp_pos.GetBinContent(1), WJetsTemp_pos.GetBinError(1))
            f_neg = af(WJetsTemp_neg.GetBinContent(1), WJetsTemp_neg.GetBinError(1))
            W_0b = f_pos*pos_val + f_neg*neg_val

            c1=ROOT.TCanvas("c1","FitModel",650,1000)
            ROOT.gROOT.SetStyle("Plain")
            c1.Divide(1,2)
            c1.cd(1)
            ROOT.gROOT.SetStyle("Plain")#Removesgraybackgroundfromplots
            ROOT.gPad.SetLeftMargin(0.15)
            fitFrame_PosPdg.GetYaxis().SetTitleOffset(1.4)
            fitFrame_PosPdg.GetXaxis().SetTitle("N_{b}")
            fitFrame_PosPdg.Draw()
            
            c1.cd(2)
            ROOT.gROOT.SetStyle("Plain")#Removesgraybackgroundfromplots
            ROOT.gPad.SetLeftMargin(0.15)
            fitFrame_NegPdg.GetYaxis().SetTitleOffset(1.4)
            fitFrame_NegPdg.GetXaxis().SetTitle("N_{b}")
            fitFrame_NegPdg.Draw()
            
            MET_string = "%s_%s"%(metBins[metBin][0], metBins[metBin][1])
            
            c1.Print('./%s_nBTagFitRes_%s.png'%(year, MET_string))
            c1.Print('./%s_nBTagFitRes_%s.pdf'%(year, MET_string))
            c1.Print('./%s_nBTagFitRes_%s.root'%(year, MET_string))
    
    results = sorted(yields_WJets_0b_postFit)
    
    #print "Central:", results[50]
    #print "Min:", results[15]
    #print "Max:", results[83]

    R_W = (af(WJets2D_pos.GetBinContent(metBin+1, 3), WJets2D_pos.GetBinError(metBin+1, 3))+af(WJets2D_neg.GetBinContent(metBin+1, 3), WJets2D_neg.GetBinError(metBin+1, 3)))/(af(WJets2D_pos.GetBinContent(metBin+1, 1), WJets2D_pos.GetBinError(metBin+1, 1))+af(WJets2D_neg.GetBinContent(metBin+1, 1), WJets2D_neg.GetBinError(metBin+1, 1)))
    y_inclH = af(WJets2D_Higgs.GetBinContent(metBin+1, 2), WJets2D_Higgs.GetBinError(metBin+1, 2)) + af(WJets2D_Higgs.GetBinContent(metBin+1, 1), WJets2D_Higgs.GetBinError(metBin+1, 1))
    R_1H = af(WJets2D_Higgs.GetBinContent(metBin+1, 2), WJets2D_Higgs.GetBinError(metBin+1, 2))/y_inclH
    R_0H = af(WJets2D_Higgs.GetBinContent(metBin+1, 1), WJets2D_Higgs.GetBinError(metBin+1, 1))/y_inclH
    numerator = af(WJets2D_Boosted.GetBinContent(metBin+1,1)+WJets2D_Boosted.GetBinContent(i,2), 0) # stat uncertainty of W+jets already in R_W
    R_1H_mistag = af(WJets2D_BoostedRew.GetBinContent(metBin+1,2), WJets2D_BoostedRew.GetBinError(metBin+1,2))/numerator
    R_0H_mistag = af(1,0) - R_1H_mistag 
    W_pred[metBins[metBin]] = {'0b':W_0b, 'R_W':R_W, '0b_all':results, '2b':W_0b*R_W, '2b,1H':W_0b*R_W*R_1H, '2b,0H':W_0b*R_W*R_0H, '2b,1Hm':W_0b*R_W*R_1H_mistag, '2b,0Hm':W_0b*R_W*R_0H_mistag}
    
    # need to set the uncertainty for 0 to 1.8410*weight -> which weight? inclusive Fall17 W+jets sample has weight of >20 for 41.5/fb. Need to check!
    
    print "R_W:", R_W

WJetsHist_pred = ROOT.TH1F('WJetsHist_pred', '', 8,0,8)
TTJetsHist_pred = ROOT.TH1F('TTJetsHist_pred', '', 8,0,8)
DataHist_obs = ROOT.TH1F('Data_obs', '', 8,0,8)

WJetsHist_pred.style = styles.fillStyle(ROOT.kGreen+1)
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
    WJetsHist_pred.SetBinContent(2*i+1, W_pred[metBin]['2b,0H'].central)
    WJetsHist_pred.SetBinError(2*i+1, W_pred[metBin]['2b,0H'].up)
    WJetsHist_pred.SetBinContent(2*i+2, W_pred[metBin]['2b,1H'].central)
    WJetsHist_pred.SetBinError(2*i+2, W_pred[metBin]['2b,1H'].up)
    DataHist_obs.SetBinContent(i+1, Data2D_pos.GetBinContent(i+1,3)+Data2D_neg.GetBinContent(i+1,3))

boxes = []
ratio_boxes = []
for ib in range(1,9):
    val = TTJetsHist_pred.GetBinContent(ib) + WJetsHist_pred.GetBinContent(ib)
    if val<0: continue
    sys = math.sqrt(TTJetsHist_pred.GetBinError(ib)**2 + WJetsHist_pred.GetBinError(ib)**2)
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
    Plot.fromHisto(name = 'Closure_%s'%year, histos = [[ WJetsHist_pred,TTJetsHist_pred ], [ DataHist_obs] ], texX = "p_{T}^{miss} bins", texY = "Events"),
    plot_directory = plot_path,
    yRange = (0.0,6.5),
    ratio = {'histos': [(1, 0)], 'texY': 'Data / pred', 'yRange':(0.1,1.9)},
    logX = False, logY = False, sorting = False,
    drawObjects = boxes,
)

## systematics
#selectionString_2l  = dilepSelection+"&&pass&&nvetoleps==2&&PassTrackVeto&&PassTauVeto&&ngoodjets>=2&&mct>200&&mbb>90&&mbb<150&&(lep1_pdgid*lep2_pdgid<0)"
selectionString_2l  = dilepSelection+"&&pass&&nvetoleps==2&&PassTrackVeto&&PassTauVeto&&ngoodjets==2&&mct>200&&mbb>90&&mbb<150&&(lep1_pdgid*lep2_pdgid<0)"
invariantMass       = "sqrt(2*leps_pt[0]*leps_pt[1]*(cosh(leps_eta[0]-leps_eta[1])-cos(leps_phi[0]-leps_phi[1])))"
selectionString_2l += "&&abs(%s-91.2)<5"%invariantMass

Data.setSelectionString("pass&&(HLT_SingleEl==1||HLT_SingleMu==1)")

## first double ratio for mbb extrapolation - only mbb selection to be determined
print "Working on b-tagging double ration"
mc_2b = DYJets.getYieldFromDraw(selectionString_2l+"&&ngoodbtags==2",'weight * w_pu *'+yearWeight)
mc_0b = DYJets.getYieldFromDraw(selectionString_2l+"&&ngoodbtags==0",'weight * w_pu *'+yearWeight)
data_2b = Data.getYieldFromDraw(selectionString_2l+"&&ngoodbtags==2",'(1)')
data_0b = Data.getYieldFromDraw(selectionString_2l+"&&ngoodbtags==0",'(1)')

mc_2b = af(mc_2b['val'], mc_2b['sigma'])
mc_0b = af(mc_0b['val'], mc_0b['sigma'])
data_2b = af(data_2b['val'], data_2b['sigma'])
data_0b = af(data_0b['val'], data_0b['sigma'])

print "2l b-tag double ratio:", (data_2b/data_0b)/(mc_2b/mc_0b)

## second double ratio for higgs tagging - under devolpment
mc_1h = DYJets.getYieldFromDraw(selectionString_2l+"&&ngoodbtags>=2&&Sum$(ak8pfjets_deepdisc_hbb>0.8)==1",'weight * w_pu *'+lumi)
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

    


