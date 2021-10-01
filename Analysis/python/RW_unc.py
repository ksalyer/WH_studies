
import math

from WH_studies.Tools.u_float import u_float as uf

#fn = '/home/users/dspitzba/WH/wh_draw/RW_exp.txt'
fn = '/home/users/dspitzba/WH/wh_draw/RW_exp_ARC.txt'
fn_theory = '/home/users/dspitzba/WH/wh_draw/RW_theory.txt'


regions = [\
    ('nj2_lowmet_res',   2, 0, '125--200'),
    ('nj2_medmet_res',   2, 0, '200--300'),
    ('nj2_highmet_res',  2, 0, '300--400'),
    ('nj2_vhighmet_res', 2, 0, '$>400$'),
    ('nj3_lowmet_res',   3, 0, '125--200'),
    ('nj3_medmet_res',   3, 0, '200--300'),
    ('nj3_highmet_res',  3, 0, '300--400'),
    ('nj3_vhighmet_res', 3, 0, '$>400$'),
    ('nj2_lowmet_boos',  2, 1, '125--300'),
    ('nj2_medmet_boos',  2, 1, '$>300$'),
    ('nj3_lowmet_boos',  3, 1, '125--300'),
    ('nj3_medmet_boos',  3, 1, '$>300$')
    ]

datacard_order = [\
    ('nj2_lowmet_res',   2, 0, '125--200'),
    ('nj2_lowmet_boos',  2, 1, '125--300'),
    ('nj2_medmet_res',   2, 0, '200--300'),
    ('nj2_medmet_boos',  2, 1, '$>300$'),
    ('nj2_highmet_res',  2, 0, '300--400'),
    ('nj2_vhighmet_res', 2, 0, '$>400$'),
    ('nj3_lowmet_res',   3, 0, '125--200'),
    ('nj3_lowmet_boos',  3, 1, '125--300'),
    ('nj3_medmet_res',   3, 0, '200--300'),
    ('nj3_medmet_boos',  3, 1, '$>300$'),
    ('nj3_highmet_res',  3, 0, '300--400'),
    ('nj3_vhighmet_res', 3, 0, '$>400$'),
    ]

uncertainties = [\
    'central',
    'puUp', 'puDown',
    'btaglfUp', 'btaglfDown',
    'btaghfUp', 'btaghfDown',
    'jesUp', 'jesDown',
    'ResUp', 'ResDown',
    'HFUp', 'HFDown',
    'HiggsUp', 'HiggsDown',
    'VVUp', 'VVDown',
    ]

uncertainties_theory = [\
    'central',
    'Wq2Up', 'Wq2Down',
    'pdfUp', 'pdfDown',
    'alphasUp', 'alphasDown',
    ]

# I hate this, but what can I do
stat_uncertainties = {\
    'nj2_lowmet_res': 1.42,
    'nj2_lowmet_boos': 1.20,
    'nj2_medmet_res': 1.19,
    'nj2_medmet_boos': 1.45,
    'nj2_highmet_res': 1.19,
    'nj2_vhighmet_res': 1.28,
    'nj3_lowmet_res': 1.62,
    'nj3_lowmet_boos': 1.23,
    'nj3_medmet_res': 1.26,
    'nj3_medmet_boos': 1.57,
    'nj3_highmet_res': 1.28,
    'nj3_vhighmet_res': 1.29
    }

CR_yield = {\
    'nj2_lowmet_res': uf(384, 23),
    'nj2_medmet_res': uf(280, 19),
    'nj2_highmet_res': uf(181, 14),
    'nj2_vhighmet_res': uf(108, 11),
    'nj2_lowmet_boos': uf(384, 23)+uf(280, 19),
    'nj2_medmet_boos': uf(181, 14)+uf(108, 11),
    'nj3_lowmet_res': uf(262,19),
    'nj3_medmet_res': uf(120,14),
    'nj3_highmet_res': uf(74,10),
    'nj3_vhighmet_res': uf(40,7),
    'nj3_lowmet_boos': uf(262,19)+uf(120,14),
    'nj3_medmet_boos': uf(74,10)+uf(40,7),
    }



datacard_unc = ['pu', 'btaglf', 'btaghf', 'jes', 'Res', 'HF', 'Higgs', 'VV', 'Wq2', 'pdf', 'alphas']

results = {}

with open(fn, 'r') as f:
    RW = f.readlines()

signalRegion = 0
block = []
for l in RW:
    #results[regions[signalRegion]] = {}
    if len(l.split())>0:
        block.append(float(l.split()[1]))
    else:
        RW_values = []
        for i in range(len(block)/2):
            #print block[(2*i+1)]/block[2*i]
            RW_values.append(block[(2*i+1)]/block[2*i])
        results[regions[signalRegion]] = { uncertainties[i]:RW_values[i]/RW_values[0] for i in range(len(RW_values)) }
        #for i in range(len(block)/2):
        #    results[regions[signalRegion]][uncertainties[i]] = sigma[i]
        results[regions[signalRegion]]['central'] = block[1]/block[0]
        results[regions[signalRegion]]['stat'] = stat_uncertainties[regions[signalRegion][0]]
        results[regions[signalRegion]]['stat_abs'] = (stat_uncertainties[regions[signalRegion][0]]-1)*results[regions[signalRegion]]['central']
        
        

        block = []
        signalRegion += 1
#        break


### Now theory uncertainties ###
with open(fn_theory, 'r') as f:
    RW = f.readlines()

signalRegion = 0
for l in RW:
    if len(l.split())>0:
        block.append(float(l.split()[1]))
    else:
        RW_values = []
        for i in range(len(block)/2):
            RW_values.append(block[(2*i+1)]/block[2*i])
        results[regions[signalRegion]].update({ uncertainties_theory[i]:RW_values[i]/RW_values[0] for i in range(len(RW_values)) if not uncertainties_theory[i]=='central' })

        #print ( results[regions[signalRegion]].keys() )
        central = block[1]/block[0]
        #print ("Central:", central)
        total_var      = ((stat_uncertainties[regions[signalRegion][0]]-1) * central)**2
        syst_up        = math.sqrt( sum([ ((results[regions[signalRegion]][x]-1) * central)**2 for x in results[regions[signalRegion]].keys() if 'Up' in x ]) )
        syst_down      = math.sqrt( sum([ ((results[regions[signalRegion]][x]-1) * central)**2 for x in results[regions[signalRegion]].keys() if 'Down' in x ]) )
        total_var_up   = total_var + sum([ ((results[regions[signalRegion]][x]-1) * central)**2 for x in results[regions[signalRegion]].keys() if 'Up' in x ])
        total_var_down = total_var + sum([ ((results[regions[signalRegion]][x]-1) * central)**2 for x in results[regions[signalRegion]].keys() if 'Down' in x ])

        results[regions[signalRegion]]['total_abs_up']   = math.sqrt(total_var_up)
        results[regions[signalRegion]]['total_abs_down'] = math.sqrt(total_var_down)
        results[regions[signalRegion]]['syst_abs_up']    = syst_up
        results[regions[signalRegion]]['syst_abs_down']  = syst_down
        results[regions[signalRegion]]['syst_abs']       = ( syst_up + syst_down ) / 2
        results[regions[signalRegion]]['RW_syst']        = uf( central, ( syst_up + syst_down ) / 2 )
        results[regions[signalRegion]]['pred_stat']      = CR_yield[regions[signalRegion][0]] * uf( central, results[regions[signalRegion]]['stat_abs'] )
        results[regions[signalRegion]]['pred_syst']      = CR_yield[regions[signalRegion][0]].val * uf( central, ( syst_up + syst_down ) / 2 )
        results[regions[signalRegion]]['pred_total']     = CR_yield[regions[signalRegion][0]] * uf( central, ( math.sqrt(total_var_up) + math.sqrt(total_var_down) ) / 2 )
        results[regions[signalRegion]]['total_up']       = math.sqrt(total_var_up)/results[regions[signalRegion]]['central']
        results[regions[signalRegion]]['total_down']     = math.sqrt(total_var_down)/results[regions[signalRegion]]['central']

        block = []
        signalRegion += 1


import pandas as pd
df = pd.DataFrame(results)

#print pd.DataFrame(results)[['nj2_lowmet_res', 'nj2_medmet_res','nj2_highmet_res','nj2_vhighmet_res']].transpose()[['central','total_abs_down', 'total_abs_up']]*1000
print pd.DataFrame(results)[[r[0] for r in regions]].transpose()[['central','total_abs_down', 'total_abs_up']]*1000

for unc in datacard_unc:
    line = ''
    line += '{:23}'.format(unc + ' lnN')
    #line.append(unc + ' lnN')
    for region in datacard_order:
        #print region, unc
        up = round(results[region][unc+'Up'], 3)
        down = round(results[region][unc+'Down'], 3)
        unc_string = '%s/%s'%(down, up)
        #line.append('%s/%s'%(down, up))

    
        template = '{:17}'*4
        line += template.format('-', '-', unc_string, '-')

    #print line

import glob
import numpy as np
#datacards = glob.glob('/home/users/ksalyer/clean/temp/wh_draw/statistics/testdir/datacards/*.txt')
#datacards = glob.glob('/home/users/dspitzba/WH/wh_draw/statistics/unblind_dataCR/datacards/*.txt')
#datacards = glob.glob('/home/users/ksalyer/clean/temp/wh_draw/statistics/cardsforDaniel/datacards/*.txt')
#datacards = glob.glob('/home/users/ksalyer/clean/temp/wh_draw/statistics/cardsforDaniel/datacards/*.txt')
#datacards = glob.glob('/home/users/ksalyer/clean/temp/wh_draw/statistics/cardsNewSF/datacards/*.txt')
#datacards = glob.glob('/home/users/dspitzba/WH/wh_draw/statistics/unblind_dataCRfix_newSF_allSystUpdate/datacards/*.txt')
#datacards = glob.glob('/home/users/ksalyer/clean/temp/wh_draw/statistics/cardsNewSF/datacards/*.txt')
datacards = glob.glob('/home/users/dspitzba/WH/wh_draw/statistics/unblind_dataCRfix_newSF_extScan/datacards/*.txt')
#datacards = datacards[:1]

print datacards

import os
update_dir = '/home/users/dspitzba/WH/wh_draw/statistics/unblind_dataCRfix_newSF_extScan/datacards_updated_withSignalSyst/'
if not os.path.isdir(update_dir):
    os.makedirs(update_dir)

nNuisanceString = 'kmax {}  number of nuisance parameters'

removeNuisances = ['sig_flat', 'W_HF', 'VV_xsec', 'HiggsTag'] # if those are in, remove these nuisances

if True:

    for datacard in datacards:
        cardfile = datacard.split('/')[-1]
        print "Datacard:", cardfile
    
        with open(datacard, 'r') as f:
            card = f.readlines()
        
        header = card[:4]
        
        observation = [ l.split() for l in card[5:7] ]
        prediction = [ l.split() for l in card[8:12] ]

        nuisances = [ l.split()[0] for l in card if len(l)>1 and (l.split()[1]=='lnN') ]
        gmNtable = [ l.split() for l in card if len(l)>1 and (l.split()[1]=='gmN') ]
        lnNtable = [ l.split() for l in card if len(l)>1 and (l.split()[1]=='lnN') ]
        goodTable = np.array(lnNtable)
    
        for unc in datacard_unc:
            # update datacard if nuisance is already there
            if unc in nuisances:
                for i, region in enumerate(datacard_order):
                    up = round(results[region][unc+'Up'], 3)
                    down = round(results[region][unc+'Down'], 3)
                    unc_string = '%s/%s'%(down, up)
                    #print i, up, down, unc_string
                    lnNtable[nuisances.index(unc)][i*4+4] = unc_string
                
            else:
            # append otherwise
                newline = [unc, 'lnN']
                for region in datacard_order:
                    up = round(results[region][unc+'Up'], 3)
                    down = round(results[region][unc+'Down'], 3)
                    unc_string = '%s/%s'%(down, up)
                    newline += ['-', '-', unc_string, '-']
                lnNtable.append(newline)
                nuisances.append(unc)
    
        indicesToRemove = [ nuisances.index(lnN[0]) for lnN in lnNtable if lnN[0] in removeNuisances  ]
        for i in reversed(sorted(indicesToRemove)):
            lnNtable.pop(i)
            nuisances.pop(i)
    
        new_card = card[0:2]
        new_card.append('kmax {}  number of nuisance parameters\n'.format(len(lnNtable)+len(gmNtable)))
        new_card += card[3:13]
    
        # write the gmN nuisances
        gmNtemplate = "{:13} {:3} {:5}" + "{:17}"*(len(gmNtable[0])-3) + '\n'
        for gmN in gmNtable:
            new_card.append(gmNtemplate.format(*gmN))
    
        lnNtemplate = "{:17} {:5}" + "{:17}"*(len(lnNtable[0])-2) + '\n'
        for lnN in lnNtable:
            new_card.append(lnNtemplate.format(*lnN))
    
        with open(update_dir+cardfile, 'w') as f:
            f.writelines(new_card)
        
    
