import ROOT

inFiles = {}

inFiles[2016] = "/home/users/dspitzba/WH/CMSSW_10_2_9/src/WH_studies/Analysis/python/eff_pt_mass_S16_QCD_combined.root"
inFiles[2017] = "/home/users/dspitzba/WH/CMSSW_10_2_9/src/WH_studies/Analysis/python/eff_pt_mass_F17_QCD_combined.root"
inFiles[2018] = "/home/users/dspitzba/WH/CMSSW_10_2_9/src/WH_studies/Analysis/python/eff_pt_mass_A18_QCD_combined.root"

out_combined = "/home/users/dspitzba/WH/CMSSW_10_2_9/src/WH_studies/Analysis/python/eff_pt_mass_allYears_QCD_combined.root"

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

def writeObjToFile(fname, obj, update=False):
    gDir = ROOT.gDirectory.GetName()
    if update:
        f = ROOT.TFile(fname, 'UPDATE')
    else:
        f = ROOT.TFile(fname, 'recreate')
    objw = obj.Clone()
    objw.Write()
    f.Close()
    ROOT.gDirectory.cd(gDir+':/')
    return

for year in [2016,2017,2018]:
    for hist in ["eff_pt_mass_2b", "eff_pt_mass_1b", "eff_pt_mass_0b"]:
        tmp = getObjFromFile(inFiles[year], hist)
        tmp.SetName(hist+"_%s"%year)
        writeObjToFile(out_combined, tmp, update=True)

