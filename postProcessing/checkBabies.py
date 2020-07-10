import glob
from RootTools.core.standard import *


#path = '/home/users/dspitzba/wh_babies/babies_v33_4_2020_05_27/a18v1/'
#path = '/home/users/dspitzba/wh_babies/babies_v33_4_2020_05_27/f17v2/'
#path = '/home/users/dspitzba/wh_babies/babies_v33_4_2020_05_27/s16v3/'
#path = '/home/users/dspitzba/wh_babies/babies_v33_4_2020_05_27/'
path = '/home/users/dspitzba/wh_babies/babies_v33_4_2020_07_09/'

files = glob.glob(path+'slim_*.root')

nMissing = 0

for f in sorted(files):
    if f.count('muoneg') or f.count('jetht') or f.count('DYJets') or f.count('amcnlo'): continue
    print "Working on file:", f
    sample = Sample.fromFiles('test', [f], 't')
    h = sample.get1DHistoFromDraw('hasNano', binning = [2, -0.5, 1.5], selectionString='(1)', weightString='(1)')
    if h.GetBinContent(1)>0:
        print "  |---> File incomplete. %s events without nanoAOD, out of %s total. That makes %s percent."%(h.GetBinContent(1), h.Integral(), float(h.GetBinContent(1)/h.Integral())*100)
        nMissing += 1

if nMissing == 0:
    print '### Congrats! All good. ###'
else:
    print '%s files seem to have a problem'%nMissing
