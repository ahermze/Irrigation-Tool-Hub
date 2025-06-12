import numpy as np
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
    ir = load(file_name, 'irrigation') \
            .merge(idx, on='plot', how='right') \
            .groupby(['DOY', 'hour', 'treatment', "Igross"]) \
            .reset_index()
            
    ### soil water deficit
    swd = load(file_name, 'soil water deficit') \
            .merge(idx, on='plot', how='right') \
            .groupby(['DOY', 'SWD_15', 'SWD_30', 'SWD_60', 'SWD_90', 'SWD_120', 'SWD_150', 'SWD_200']) \
            .reset_index()

    ## growth stage 
    gs = load(file_name, 'growth stage') \
        .merge(idx, on='plot', how='right') \

    return st, wx, ir, swd, gs


def setup(st, wx, ir, swd, gs):
    print()




def plot_wise_stuff(file_name):
    st, wx, ir, swd, gs = load_file(file_name)
    setup(st, wx, ir, swd, gs)








































































# returns water deficit for current day, in mm (how much you should water)
#
# parameters are: 
#   - deficit for previous day (mm), 
#   - current crop evapotranspiration rate (mm), 
#   - gross precipitation, 
#   - net irrigation for current day (mm),
#   - and surface runnof (mm).
def getCurrentDeficit(defp, etc, p, irr, sro):

    defc = defp + etc - p - irr + sro
    if (defc < 0):
        defc = 0.0
    return defc


# returns evapotranspiration rate for current day
#
# parameters 
#   - evapotranspiration rate (mm/d) from tall reference crop?, 
#   - crop coefficeint (alfalfa based, changes by development stage from 0-1)
#   - water stress coefficent (from 0-1)
def getCurrentET(etr, kcr, ks):
    print()

# get available water capacity
# units are water (mm) per soild depth (mm)
#       or m^3 water per m^3 soil
# soil info from USDA Soil Survey Geographic (SSURGO) Database
def getAWC(field_capacity, p_wilting_point):
    return field_capacity - p_wilting_point


# Net irrigation amount is gross amount watered multiplied
# by the irrigation application efficiency
def getNetIrrigation(gross, efficiency):
    return gross * efficiency


