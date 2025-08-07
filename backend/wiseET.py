import numpy as np
from pandas import read_excel, concat, DataFrame, Index, MultiIndex, date_range
from numpy import empty, full
import matplotlib.pyplot as plt
from pathlib import Path


from pandas import read_excel, concat, DataFrame, Index, MultiIndex, date_range
from numpy import empty, full
import matplotlib.pyplot as plt

from datetime import datetime, timedelta

def load(file_name, sheet):
    return read_excel(file_name, sheet_name=sheet)

def load_the_file(file_name):

    #### Loading the information
    st = load(file_name, 'sites')
    wx = load(file_name, 'weather')
    idx = load(file_name, 'index')

    ## irrigation
    ir = load(file_name, 'irrigation')
            
    ### soil water deficit
    swd = load(file_name, 'soil water deficit') \
            .merge(idx, on='plot', how='right')
  
    return idx, st, swd, wx, ir


def wiseET_processfile():
    path = "./static/data.xlsx"

    df = read_excel(path)

    idx, st, swd, wx, ir = load_the_file(path)

    swd_dictionary = {}

    for index, row in swd.iterrows():
        total = row["SWD_15"] + row["SWD_30"] + row["SWD_60"] + row["SWD_90"] + row["SWD_120"] + row["SWD_150"] + row["SWD_200"]
        swd_dictionary.setdefault(row["plot"], {})[row["DOY"]] = total

    irr_dictionary = {}

    for index, row in ir.iterrows():
        if row["DOY"] in irr_dictionary:
            irr_dictionary[row["DOY"]] += row["Igross"]
        else:
            irr_dictionary[row["DOY"]] = row["Igross"]

    pre_dictionary = {}

    for index, row in wx.iterrows():
        if row["day"] in pre_dictionary:
            pre_dictionary[row["day"]] += row["pp"]
        else:
            pre_dictionary[row["day"]] = row["pp"]
    

    all_plots = {}

    for plot in swd_dictionary.keys():

        dictionary = swd_dictionary[plot]

        days_available = list(dictionary.keys())
        new_thing = {}

        for day in range(min(dictionary.keys()),max(dictionary.keys()) + 1):
            if day not in pre_dictionary.keys():
                pre_dictionary[day] = 0
            if day not in irr_dictionary.keys():
                irr_dictionary[day] = 0

            if day not in dictionary.keys():

                start = 0
                end = 0

                found = False
                for i, available in enumerate(days_available):
                    if not found and day > available and day < days_available[i+1]:
                        start = available
                        end = days_available[i+1]

                        found = True

                output = dictionary[start] + ((dictionary[end]-dictionary[start])/(end-start)) * (day-start)
                dictionary[day] = output

            if day != days_available[0]:
                if dictionary[day] < 0:
                    dictionary[day] = 0
                final = dictionary[day] - dictionary[day-1] + pre_dictionary[day] + irr_dictionary[day]
                new_thing[day] = final
                
        all_plots[plot] = new_thing

        # plt.plot(new_thing.keys(), new_thing.values(), 'orange', label="ET")
        # plt.title(f"Plot: {plot}")
        # plt.legend()
        # plt.show()


    plt.figure(figsize=(20, 6))
    for plot in all_plots.keys():
        plt.plot(all_plots[plot].keys(), all_plots[plot].values(), label=plot)

    plt.xlabel('Days')
    plt.ylabel('Crop ET rate (mm)')
    plt.title(f"WISE ET Rate At {st["site"].iloc[0]}, Per Plot")
    plt.tight_layout()
    plt.legend()
    # plt.show()
    plt.savefig("./static/wiseET.png")

# processfile()