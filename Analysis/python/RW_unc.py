fn = '/home/users/dspitzba/WH/wh_draw/RW3.txt'


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
    'pileupUp', 'pileupDown',
    'btagLFUp', 'btagLFDown',
    'btagHFUp', 'btagHFDown',
    'JESUp', 'JESDown',
    'ResUp', 'ResDown',
    'HFUp', 'HFDown',
    'HiggsUp', 'HiggsDown',
    'VVUp', 'VVDown',
    ]

datacard_unc = ['pileup', 'btagLF', 'btagHF', 'JES', 'Res', 'HF', 'Higgs', 'VV']

results = {}

with open(fn, 'r') as f:
    RW = f.readlines()

signalRegion = 0
block = []
for l in RW:
    results[regions[signalRegion]] = {}
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
        block = []
        signalRegion += 1
#        break

import pandas as pd
df = pd.DataFrame(results)

for unc in datacard_unc:
    line = ''
    line += '{:23}'.format(unc + ' lnN')
    #line.append(unc + ' lnN')
    for region in datacard_order:
        up = round(results[region][unc+'Up'], 3)
        down = round(results[region][unc+'Down'], 3)
        unc_string = '%s/%s'%(down, up)
        #line.append('%s/%s'%(down, up))

    
        template = '{:17}'*4
        line += template.format('-', '-', unc_string, '-')

    print line

