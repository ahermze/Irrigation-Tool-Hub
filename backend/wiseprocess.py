import numpy as np
from pandas import read_excel, concat, DataFrame, Index, MultiIndex, date_range
from numpy import empty, full
import matplotlib.pyplot as plt
from pathlib import Path
from pandas import read_excel, concat, DataFrame, Index, MultiIndex, date_range
from numpy import empty, full
import matplotlib.pyplot as plt

def load(file_name, sheet):
    return read_excel(file_name, sheet_name=sheet)

def load_file(file_name):

    #### Loading the information
    st = load(file_name, 'sites')
    wx = load(file_name, 'weather')
    idx = load(file_name, 'index')

    ### irrigation
#     ir = load(file_name, 'irrigation') \
#             .merge(idx, on='plot', how='right') \
#             .groupby(['DOY', 'hour', 'treatment', "Igross"]) \
#             .reset_index()
            
    ### soil water deficit
    swd = load(file_name, 'soil water deficit') \
            .merge(idx, on='plot', how='right') \
            .groupby(['plot'])
            # .groupby(['DOY', 'SWD_15', 'SWD_30', 'SWD_60', 'SWD_90', 'SWD_120', 'SWD_150', 'SWD_200']) \
            # .reset_index()

    ## growth stage 
    gs = load(file_name, 'growth stage') \
        .merge(idx, on='plot', how='right') \

    return idx, st, swd
#     return st, wx, ir, swd, gs

def processfile():
    # path = Path(__file__).parent / "../static/data.xlsx"
    path = "./static/data.xlsx"

    df = read_excel(path)

    # grps = plot_wise_stuff(path)
    idx, st, swd = load_file(path)
    theplots = swd['plot'].all().index.tolist()

    alist = []
    for thing in theplots:
        alist.append(swd.get_group((str(thing),)))

    for i in range(len(theplots)):
        site_name = alist[i]['site'].iloc[0]
        the_year = alist[i]['year'].iloc[0]
        alist[i].plot(x='DOY', y=['SWD_15', 'SWD_30', 'SWD_60', 'SWD_90', 'SWD_120', 'SWD_150', 'SWD_200'], label=['SWD_15, 0-15cm', 'SWD_30, 15-45cm', 'SWD_60, 45-75cm', 'SWD_90, 75-105cm', 'SWD_120, 105-135cm', 'SWD_150, 135-165cm', 'SWD_200, 185-215cm'], title=f"Site: {site_name}      Plot: {theplots[i]}")
        plt.xlabel(f"DOY (Day of Year, in {the_year})")
        plt.ylabel("Soil Water Deficit (mm)")

        legend = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), frameon=True, ncol=3)
        for text in legend.get_texts():
            text.set_alpha(1.0)  # Set the transparency of the legend text to fully opaque

        plt.tight_layout()
        plt.savefig(f"./static/plot{i}.png")

        # plt.show()
