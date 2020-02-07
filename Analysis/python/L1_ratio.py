import ROOT

from RootTools.core.standard import *

def getObjFromFile(fname, hname):
    f = ROOT.TFile(fname)
    assert not f.IsZombie()
    f.cd()
    htmp = f.Get(hname)
    if not htmp:  return htmp
    ROOT.gDirectory.cd('PyROOT:/')
    res = htmp.Clone()
    f.Close()
    return res

def GetHistogram(fname):
    # custom made function to get the histograms from the root files
    rf1 = ROOT.TFile(fname)
    primitiveNames = [ x.GetName() for x in rf1.GetListOfKeys() ]
    canvasName = primitiveNames[0]
    c1 = getObjFromFile(fname, canvasName)
    primitiveNames = [ x.GetName() for x in c1.GetListOfPrimitives() if x.GetName().count('top') ]
    padName = primitiveNames[0]
    p1 = c1.GetPrimitive(padName)
    primitiveNames = [ x.GetName() for x in p1.GetListOfPrimitives() if x.GetName().count('bkg') ]
    h1 = p1.GetPrimitive(primitiveNames[0])
    h1_tmp = h1.Clone()
    rf1.Close()
    return h1_tmp


f_L1weight      ='/home/users/dspitzba/WH/wh_draw/plots/y2017_L1Study_signalSel__mt_met_lep__nvetoleps1_PassTrackVeto_PassTauVeto_ngoodjets2_pfmetg125_mt_met_lepg150_mctg200_WHLeptons1__weightxw_pux1__lumi_lin.root'
f_noL1weight    ='/home/users/dspitzba/WH/wh_draw/plots/y2017_L1Study_signalSel__mt_met_lep__nvetoleps1_PassTrackVeto_PassTauVeto_ngoodjets2_pfmetg125_mt_met_lepg150_mctg200_WHLeptons1__weightxw_pux1dw_L1__lumi_lin.root'

#f_L1weight      ='/home/users/dspitzba/WH/wh_draw/plots/y2017_L1Study_signalSel__pfmet__nvetoleps1_PassTrackVeto_PassTauVeto_ngoodjets2_pfmetg125_mt_met_lepg150_mctg200_WHLeptons1__weightxw_pux1__lumi_lin.root'
#f_noL1weight    ='/home/users/dspitzba/WH/wh_draw/plots/y2017_L1Study_signalSel__pfmet__nvetoleps1_PassTrackVeto_PassTauVeto_ngoodjets2_pfmetg125_mt_met_lepg150_mctg200_WHLeptons1__weightxw_pux1dw_L1__lumi_lin.root'

#f_L1weight      ='/home/users/dspitzba/WH/wh_draw/plots/y2017_L1Study_signalSel__mct__nvetoleps1_PassTrackVeto_PassTauVeto_ngoodjets2_pfmetg125_mt_met_lepg150_mctg200_WHLeptons1__weightxw_pux1__lumi_lin.root'
#f_noL1weight    ='/home/users/dspitzba/WH/wh_draw/plots/y2017_L1Study_signalSel__mct__nvetoleps1_PassTrackVeto_PassTauVeto_ngoodjets2_pfmetg125_mt_met_lepg150_mctg200_WHLeptons1__weightxw_pux1dw_L1__lumi_lin.root'

#f_L1weight      ='/home/users/dspitzba/WH/wh_draw/plots/y2017_L1Study_signal_700_1_signalSel__mbb__nvetoleps1_PassTrackVeto_PassTauVeto_ngoodjets2_pfmetg125_mt_met_lepg150_mctg200_WHLeptons1__weightxw_pux1__lumi_lin.root'
#f_noL1weight    ='/home/users/dspitzba/WH/wh_draw/plots/y2017_L1Study_signal_700_1_signalSel__mbb__nvetoleps1_PassTrackVeto_PassTauVeto_ngoodjets2_pfmetg125_mt_met_lepg150_mctg200_WHLeptons1__weightxw_pux1dw_L1__lumi_lin.root'

#f_L1weight      ='/home/users/dspitzba/WH/wh_draw/plots/y2017_L1Study_signalSel__mbb__nvetoleps1_PassTrackVeto_PassTauVeto_ngoodjets2_pfmetg125_mt_met_lepg150_mctg200_WHLeptons1__weightxw_pux1__lumi_lin.root'
#f_noL1weight    ='/home/users/dspitzba/WH/wh_draw/plots/y2017_L1Study_signalSel__mbb__nvetoleps1_PassTrackVeto_PassTauVeto_ngoodjets2_pfmetg125_mt_met_lepg150_mctg200_WHLeptons1__weightxw_pux1dw_L1__lumi_lin.root'

h_noL1weight    = GetHistogram( f_noL1weight )
h_L1weight      = GetHistogram( f_L1weight )

h_L1weight.style     = styles.lineStyle( ROOT.kRed,  width=2 )
h_noL1weight.style   = styles.lineStyle( ROOT.kBlue, width=2 )

h_L1weight.legendText   = "L1 reweight"
h_noL1weight.legendText = "central"


plot_path = './'

plotting.draw(
    Plot.fromHisto(name = 'Bkg_pfmet_L1', histos = [[ h_L1weight ], [ h_noL1weight] ], texX = "p_{T}^{miss} (GeV)", texY = "Events"),
    plot_directory = plot_path,
#    yRange = (0.003,3),
    ratio = {'histos': [(0, 1)], 'texY': 'L1 weight / no L1', 'yRange':(0.88,1.02)},
    logX = False, logY = True, sorting = False,
)

#plotting.draw(
#    Plot.fromHisto(name = 'Bkg_mt_met_lep_L1', histos = [[ h_L1weight ], [ h_noL1weight] ], texX = "M_{T} (GeV)", texY = "Events"),
#    plot_directory = plot_path,
##    yRange = (0.003,3),
#    ratio = {'histos': [(0, 1)], 'texY': 'L1 weight / no L1', 'yRange':(0.88,1.02)},
#    logX = False, logY = True, sorting = False,
#)

#plotting.draw(
#    Plot.fromHisto(name = 'Bkg_MCT_L1', histos = [[ h_L1weight ], [ h_noL1weight] ], texX = "M_{CT} (GeV)", texY = "Events"),
#    plot_directory = plot_path,
##    yRange = (0.003,3),
#    ratio = {'histos': [(0, 1)], 'texY': 'L1 weight / no L1', 'yRange':(0.88,1.02)},
#    logX = False, logY = True, sorting = False,
#)

#plotting.draw(
#    Plot.fromHisto(name = 'Bkg_Mbb_L1', histos = [[ h_L1weight ], [ h_noL1weight] ], texX = "M_{bb} (GeV)", texY = "Events"),
#    plot_directory = plot_path,
##    yRange = (0.003,3),
#    ratio = {'histos': [(0, 1)], 'texY': 'L1 weight / no L1', 'yRange':(0.88,1.02)},
#    logX = False, logY = True, sorting = False,
#)
