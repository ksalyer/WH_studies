'''
Plot the 2D maps for the Higgs tagging efficiency
'''
import ROOT as r
from plottery import plottery as ply

from WH_studies.Tools.helpers import getObjFromFile

h_eff = getObjFromFile('../../Analysis/python/eff_pt_mass_F17_QCD_combined.root', 'eff_pt_mass_2b')

ply.plot_hist_2d(
        h_eff,
        options = {
            "cms_label": "Preliminary",
            "xaxis_log": True,
            "yaxis_log": True,
            "zaxis_log": False,
            "bin_text_smart": True,
            "bin_text_format": ".2f",
            "draw_option_2d": "colz texte",

            "xaxis_label": "p_{T} (GeV)",
            "yaxis_label": "M (GeV)",
            "xaxis_noexponents": True,
            "yaxis_noexponents": True,
            "zaxis_noexponents": True,
            "output_name": "plottery/efficiencies/F17_QCD_combined.pdf",
            }
        )

