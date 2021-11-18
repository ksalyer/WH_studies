'''
Get a signal region plot from the fitDiagnostics workspace
'''

#!/usr/bin/env python
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--signal",               dest='signal',  action='store', default='T2tt',    choices=["T2tt", "T2bW", "ttHinv"], help="which signal?")
parser.add_option("--massPoints",           dest='massPoints',  action='store', default='800_100,350_150', help="which masspoints??")
parser.add_option("--version",              dest='version', action='store', default='v8',    help="Which version of estimates should be used?")
parser.add_option('--logLevel',             dest="logLevel",              default='INFO',              action='store',      help="log level?", choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'])
parser.add_option('--blinded',              action="store_true")
parser.add_option('--postFit',              dest="postFit", default = False, action = "store_true", help="Apply pulls?")
parser.add_option('--expected',             action = "store_true", help="Run expected?")
parser.add_option('--preliminary',          action = "store_true", help="Run expected?")
parser.add_option('--testGrayscale',        action = "store_true", help="Do the most important test for this collaboration?")
parser.add_option("--postFix",              action='store',      default="", help='Add sth?')
(options, args) = parser.parse_args()

# Standard imports
import ROOT
import os
import sys
import pickle
import math
import yaml

# Analysis
from WH_studies.Tools.u_float           import u_float
from WH_studies.Tools.asym_float           import asym_float as af
from WH_studies.Tools.getPostFit        import *

#regions = range(12)
regions = range(20)

from RootTools.core.standard import *
# logger
import WH_studies.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   options.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(options.logLevel, logFile = None)

lumiStr = 137

isData = True if not options.expected else False
massPoints = options.massPoints.split(',')

#workspace  = 'data/fitDiagnostics_750_1.root'
#workspace  = 'data/fitDiagnostics_800_100.root'
#workspace  = 'data/fitDiagnostics_800_100_ARC.root'
#workspace  = 'data/fitDiagnostics_800_100_ARC_update.root'
#workspace  = 'data/datacard_mChi-800_mLSP-100__fix.root'
workspace = 'fitDiagnostics.root'

# get the results
postFitResults = getPrePostFitFromMLF(workspace)
covariance = getCovarianceFromMLF(workspace, postFit=options.postFit)

preFitHist={}
postFitHist={}
bhistos=[]
hists={}
histos={}
bkgHist=[]
processes = [('rares', 'SM SS'),
            ('fakes_mc', 'Nonprompt'),
            ('flips_mc', 'Charge Flip'),
            ('total_background', 'total'), # for uncertainties
            ('data', 'Total'),
            ('signal', 'tqH'),
            #('sig', 'TChiWH(750,1)'),
            #('sig2', 'TChiWH(425,150)'),
            #('sig3', 'TChiWH(225,75)'),\
            ]

## need to sort the regions somehow
#regions = postFitResults['hists']['shapes_prefit'].keys()
regions = [\
    ('bin_0'),
    ('bin_1'),
    ('bin_2'),
    ('bin_3'),
    ('bin_4'),
    ('bin_5'),
    ('bin_6'),
    ('bin_7'),
    ('bin_8'),
    ('bin_9'),
    ('bin_10'),
    ('bin_11'),
    ('bin_12'),
    ('bin_13'),
    ('bin_14'),
    ('bin_15'),
    ('bin_16'),
    ('bin_17'),
    ('bin_18'),
    ('bin_19'),
    ]


hists = { p:ROOT.TH1F(p,tex,len(regions),0,len(regions)) for p,tex in processes }

shapes = 'shapes_prefit' if not options.postFit else 'shapes_fit_s'

res = []

import copy

dict_for_table = []
for ibin, region in enumerate(regions):
    binName = region
    row = {'fakes_mc':0, 'rares':0, 'flips_mc':0, 'total_background':0, 'signal':0, 'data':0}
    dict_for_table.append(copy.deepcopy(row))
    res.append(copy.deepcopy(row))

total_pred = 0

for p,tex in processes:
    hists[p].legendText = tex
    for ibin, region in enumerate(regions):
        binName = region
        shapesKey = 'shapes_prefit' if p.count('sig') else shapes
        if p == 'data':
            pred = int(round(postFitResults['hists'][shapesKey][binName][p].Eval(1),0))
            #hists[p].SetBinContent(ibin+1, obs)
            #hists[p].SetBinError(ibin+1, af(obs)
        else:
            try:
                print p, shapesKey
                pred = postFitResults['hists'][shapesKey][binName][p].GetBinContent(1)
                err  = postFitResults['hists'][shapesKey][binName][p].GetBinError(1)
            except KeyError:
                pred, err = 0, 0

        hists[p].SetBinContent(ibin+1, pred)
        if not p == 'data':
            hists[p].SetBinError(ibin+1, err)

        if p == 'data':
             pred_str = "%s"%int(pred)
        elif pred<0.02:
            pred_str = '$\leq 0.01$'
        elif pred<1.0:
        #elif p=='other':
            pred_str = "${:.2f} \pm {:.2f}$".format(pred, err)
        else:
            pred_str = "${:.1f} \pm {:.1f}$".format(pred, err)
        dict_for_table[ibin][p] = pred_str
        res[ibin][p] = pred

#test = ROOT.TColor(2021, 0.6, 0.6, 1.0)  # old
test = ROOT.TColor(2021, 0.647, 0.53, 1.0)
#colors = {'top':ROOT.kAzure+1, 'wjets':ROOT.kGreen+1, 'other':ROOT.kOrange+7} # single-t would be kOrange
colors = {'fakes_mc':ROOT.kAzure+1, 'flips_mc':ROOT.kGreen+1, 'rares':2021} # single-t would be kOrange

hists['fakes_mc'].style = styles.fillStyle(ROOT.kAzure+1)
hists['flips_mc'].style = styles.fillStyle(ROOT.kGreen+1)
#hists['other'].style = styles.fillStyle(ROOT.kOrange+7)
hists['rares'].style = styles.fillStyle(2021)
hists['signal'].style = styles.lineStyle(ROOT.kRed, width=3)
hists['data'].SetBinErrorOption(ROOT.TH1F.kPoisson)
#hists['data'].style = styles.errorStyle( ROOT.kBlack, markerSize = 1., drawOption='e0' )
hists['data'].style = styles.errorStyle( ROOT.kBlack, markerSize = 1. )

total_pred = hists['total_background'].Integral()

ymin = 0.006

boxes = []
ratio_boxes = []

for ib, region in enumerate(regions):
    binName = region
    val = hists['total_background'].GetBinContent(ib+1)
    sys = hists['total_background'].GetBinError(ib+1)
    sys_rel = sys/val
    print "Bin {:25} pred: {:.3} +/- {:.3}, obs: +/-".format(binName, val, sys)
    box = ROOT.TBox( hists['total_background'].GetXaxis().GetBinLowEdge(ib+1),  max([ymin, val-sys]), hists['total_background'].GetXaxis().GetBinUpEdge(ib+1), max([ymin, val+sys]) )
    #box.SetLineColor(ROOT.kGray+1)
    #box.SetFillStyle(3244)
    box.SetFillStyle(1001)
    #box.SetFillColor(ROOT.kGray+1)
    box.SetFillColorAlpha(ROOT.kBlack, 0.2)
    boxes.append(box)

    r_box = ROOT.TBox( hists['total_background'].GetXaxis().GetBinLowEdge(ib+1),  max(0.11, 1-sys_rel), hists['total_background'].GetXaxis().GetBinUpEdge(ib+1), min(1.9, 1+sys_rel) )
    #r_box.SetLineColor(ROOT.kGray+1)
    r_box.SetFillStyle(1001)
    r_box.SetFillColorAlpha(ROOT.kBlack, 0.2)
    #r_box.SetFillStyle(3244)
    #r_box.SetFillColor(ROOT.kGray+1)
    ratio_boxes.append(r_box)


binLabels = ['bin_'+str(x) for x in range(20)]
def setBinLabels( hist ):
    for i in range(1, hist.GetNbinsX()+1):
        hist.GetXaxis().SetBinLabel(i, '%s       '%binLabels[i-1])

def drawDivisions(regions):
    # divisions in main plot
    min = 0.15
    max = 0.95
    diff = (max-min) / len(regions)
    lines = []
    lines2 = []
    line = ROOT.TLine()
    line.SetLineWidth(1)
    line.SetLineStyle(2)
    lines  = [ (min+4*diff,  0.005, min+4*diff, 0.57) ]
    lines += [ (min+6*diff,  0.005, min+6*diff, 0.65) ]
    lines += [ (min+10*diff,  0.005, min+10*diff, 0.57) ]
    return [line.DrawLineNDC(*l) for l in lines] + [tex.DrawLatex(*l) for l in []] + [tex2.DrawLatex(*l) for l in lines2]

def drawDivisionsRatio(regions):
    # divisons in ratio plot
    min = 0.15
    max = 0.95
    diff = (max-min) / len(regions)
    lines = []
    lines2 = []
    line = ROOT.TLine()
    line.SetLineWidth(1)
    line.SetLineStyle(2)
    lines  = [ (min+4*diff,  0.45, min+4*diff, 0.90) ]
    lines += [ (min+6*diff,  0.45, min+6*diff, 0.90) ]
    lines += [ (min+10*diff, 0.45, min+10*diff, 0.90) ]
    return [line.DrawLineNDC(*l) for l in lines] + [tex.DrawLatex(*l) for l in []] + [tex2.DrawLatex(*l) for l in lines2]

def drawTexLabels( regions ):
    tex = ROOT.TLatex()
    tex.SetNDC()
    tex.SetTextSize(0.042)
    tex.SetTextAngle(0)
    tex.SetTextAlign(12) # align right
    min = 0.15
    max = 0.95
    diff = (max-min) / len(regions)
    lines  = [ (min + (7./2)*diff-0.02, 0.60, "#bf{N_{jets} = 2}"), (min + (3./2)*diff, 0.55, "#bf{N_{H} = 0}"), (min + (9./2)*diff, 0.55, "#bf{N_{H} = 1}") ] 
    lines += [ (min + (19./2)*diff-0.02, 0.60, "#bf{N_{jets} = 3}"), (min + (15./2)*diff, 0.55, "#bf{N_{H} = 0}"), (min + (21./2)*diff, 0.55, "#bf{N_{H} = 1}")] 
    return [tex.DrawLatex(*l) for l in lines]

def getLegend():
    leg = ROOT.TLegend(0.17,0.90-5*0.050, 0.44, 0.90)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetShadowColor(ROOT.kWhite)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.040)
    for p,tex in processes:
        if p.count('sig') or p=='data' or p=='total_background': continue
        hists[p].SetFillColor(colors[p])
        hists[p].SetLineColor(ROOT.kBlack)
        leg.AddEntry(hists[p], '#bf{%s}'%tex, 'f' )
    hists['data'].SetLineColor(1)
    hists['data'].SetLineWidth(1)
    hists['data'].SetMarkerStyle(8)
    leg.AddEntry(hists['data'], '#bf{Observed}', 'e1p')
    boxes[0].SetLineWidth(0)
    leg.AddEntry(boxes[0], '#bf{Uncertainty}', 'f')
    return [leg]

dummy = ROOT.TH1F('dummy','dummy', 1,0,1)
def getSignalLegend():
    leg = ROOT.TLegend(0.40,0.90-4*0.050, 0.80, 0.90)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetShadowColor(ROOT.kWhite)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.040)
    # add the description
    #boxes[0].SetLineWidth(0)
    #boxes[0].SetFillColor(0)
    dummy.SetLineWidth(0)
    dummy.SetMarkerSize(0)
    #leg.AddEntry(dummy, '#bf{#tilde{#chi}^{0}_{2} #rightarrow H #tilde{#chi}^{0}_{1},  #tilde{#chi}^{#pm}_{1} #rightarrow W^{#pm} #tilde{#chi}^{0}_{1}}')
    # add the entries
    hists['signal'].SetLineColor(ROOT.kRed)
    hists['signal'].SetLineWidth(3)
    hists['signal'].SetLineStyle(1)
    leg.AddEntry(hists['signal'], 'tqH', 'l')
    #hists['sig2'].SetLineColor(ROOT.kRed)
    #hists['sig2'].SetLineWidth(3)
    #hists['sig2'].SetLineStyle(3)
    #leg.AddEntry(hists['sig2'], '#bf{m_{#tilde{#chi}^{0}_{2}/#tilde{#chi}^{#pm}_{1}} = 425 GeV, m_{#tilde{#chi}^{0}_{1}} = 150 GeV}', 'l')
    #hists['sig3'].SetLineColor(ROOT.kRed)
    #hists['sig3'].SetLineWidth(3)
    #hists['sig3'].SetLineStyle(2)
    #leg.AddEntry(hists['sig3'], '#bf{m_{#tilde{#chi}^{0}_{2}/#tilde{#chi}^{#pm}_{1}} = 225 GeV, m_{#tilde{#chi}^{0}_{1}} = 75 GeV}', 'l')
    return [leg]

def drawObjects( isData=False, lumi=137 ):
    tex = ROOT.TLatex()
    tex.SetNDC()
    tex.SetTextSize(0.05)
    tex.SetTextAlign(11) # align right
    lines = [
      (0.15, 0.945, 'CMS Simulation') if not isData else ( (0.15, 0.945, 'CMS') if not options.preliminary else (0.15, 0.945, 'CMS #bf{#it{Preliminary}}')),
      (0.70, 0.945, '#bf{%s fb^{-1} (13 TeV)}'%lumi )
    ]
    return [tex.DrawLatex(*l) for l in lines]

#drawObjects = drawObjects(isData) + boxes + drawDivisions(regions) + drawTexLabels(regions) + getLegend() + getSignalLegend()
drawObjects = drawObjects(isData) + boxes + getLegend() + getSignalLegend()

plots = [ [hists['fakes_mc'], hists['rares'], hists['flips_mc']], [hists['data']], [hists['signal']] ]
#plots = [ [hists['top'], hists['wjets'], hists['other']], [hists['data']], [hists['sig']] ]

for log, l in [(False,'lin'),(True,'log')]:

    postFix = ''
    if options.postFit:
        postFix += '_postFit'

    postFix += '_%s'%l
    
    plotting.draw(
        Plot.fromHisto('signalRegions'+postFix,
                    plots,
                    texX = "Signal Region",
                    texY = 'Events',
                ),
        plot_directory = os.path.join('/home/users/ksalyer/public_html/', "signalRegions_unblind_ref"),
        logX = False, logY = log, sorting = False, 
        legend = None,
        widths = {'x_width':800, 'y_width':600, 'y_ratio_width':250},
        yRange = (0.1,300000) if log else (0.01,3000),
        drawObjects = drawObjects,
        #histModifications = [lambda h: h.GetYaxis().SetTitleSize(32), lambda h: h.GetYaxis().SetLabelSize(28), lambda h: h.GetYaxis().SetTitleOffset(1.2)],
        histModifications = [lambda h: h.GetYaxis().SetTitleSize(32), lambda h: h.GetYaxis().SetLabelSize(28)],
        ratio = {
            'yRange': (0.11, 2.19), 
            'texY':'#frac{Obs.}{Pred.}', 
            'histos':[(1,0)], 
            'histModifications': [lambda h: setBinLabels(h), lambda h: h.GetYaxis().SetTitleSize(32), lambda h: h.GetYaxis().SetLabelSize(28), lambda h: h.GetXaxis().SetTitleSize(32), lambda h: h.GetXaxis().SetLabelSize(27), lambda h: h.GetXaxis().SetLabelOffset(0.025), lambda h: h.GetXaxis().SetTitleOffset(4.2)], 
            #'drawObjects':drawDivisionsRatio(regions)+ratio_boxes
            'drawObjects':ratio_boxes
        },
        copyIndexPHP = True,
    )

import pandas as pd

df = pd.DataFrame(dict_for_table)

#print df.to_latex(columns=['nJet','nHiggs', 'MET','top','wjets','other','total_background', 'data', 'sig', 'sig2', 'sig3'], index=False, escape=False)

#print
#print "######################################################"
#print "######## PAPER VERSION OF THE TABLE ##################"
#print "######################################################"
#print

#print df.to_latex(columns=['nJet','nHiggs', 'MET','total_background', 'data', 'sig', 'sig2', 'sig3'], index=False, escape=False)

#print
#print
#print
#print
#print "######################################################"
#print "######### NOTE VERSION OF THE TABLE ##################"
#print "######################################################"
#print

#print df.to_latex(columns=['nJet','nHiggs', 'MET','top','wjets','other','total_background', 'data', 'sig', 'sig2', 'sig3'], index=False, escape=False)

