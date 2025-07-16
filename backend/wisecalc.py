# import numpy as np
# from pandas import read_excel, concat, DataFrame, Index, MultiIndex, date_range
# from numpy import empty, full
# import matplotlib.pyplot as plt



# # returns water deficit for current day, in mm (how much you should water)
# #
# # parameters are: 
# #   - deficit for previous day (mm), 
# #   - current crop evapotranspiration rate (mm), 
# #   - gross precipitation, 
# #   - net irrigation for current day (mm),
# #   - and surface runnof (mm).
# def getCurrentDeficit(defp, etc, p, irr, sro):

#     defc = defp + etc - p - irr + sro
#     if (defc < 0):
#         defc = 0.0
#     return defc


# # returns evapotranspiration rate for current day
# #
# # parameters 
# #   - evapotranspiration rate (mm/d) from tall reference crop?, 
# #   - crop coefficeint (alfalfa based, changes by development stage from 0-1)
# #   - water stress coefficent (from 0-1)
# def getCurrentET(etr, kcr, ks):
#     print()

# # get available water capacity
# # units are water (mm) per soild depth (mm)
# #       or m^3 water per m^3 soil
# # soil info from USDA Soil Survey Geographic (SSURGO) Database
# def getAWC(field_capacity, p_wilting_point):
#     return field_capacity - p_wilting_point


# # Net irrigation amount is gross amount watered multiplied
# # by the irrigation application efficiency
# def getNetIrrigation(gross, efficiency):
#     return gross * efficiency
