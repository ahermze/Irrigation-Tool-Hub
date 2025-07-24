import numpy as np
from pandas import read_excel, concat, DataFrame, Index, MultiIndex, date_range
from numpy import empty, full
import matplotlib.pyplot as plt
from pathlib import Path


from pandas import read_excel, concat, DataFrame, Index, MultiIndex, date_range
from numpy import empty, full
import matplotlib.pyplot as plt

from datetime import datetime, timedelta

def loadetr(file_name, sheet):
    return read_excel(file_name, sheet_name=sheet)

def load_fileetr(file_name):

    #### Loading the information
    st = loadetr(file_name, 'sites')
    wx = loadetr(file_name, 'weather')
    idx = loadetr(file_name, 'index')

    return st, wx, idx
#     return st, wx, ir, swd, gs

# equation is from https://edis.ifas.ufl.edu/publication/AE459 its not very readable here
# def theEquation(Ta, Rh, u2, Rs, elevation):
#     A = (4098*(0.6108*(2.7183**((17.27*Ta)/(Ta+237.3))))) / ((Ta+273.3)**2)
#     y = 0.000665*101.3*(((293-0.0065*elevation)/(293))**5.26)
#     es = 0.6108*(2.7183**((17.27*Ta)/(Ta+237.3)))
#     ea = es + Rh
#     G = 0

#     return (0.408*A*(Rs-G) + y*((900/24)/(Ta+273))*u2*(es-ea)) / (A + y*(1+0.34*u2))

# def processfileetr():
#     path = "./static/data.xlsx"
#     st, wx, idx = load_fileetr(path)
#     site_name = st['site']
#     elevation = st["elev"]
#     # equation is from https://edis.ifas.ufl.edu/publication/AE459 its not very readable here
#     def theEquation(Ta, Rh, u2, Rs, elevation):
#         A = (4098*(0.6108*(2.7183**((17.27*Ta)/(Ta+237.3))))) / ((Ta+273.3)**2)
#         y = 0.000665*101.3*(((293-0.0065*elevation)/(293))**5.26)
#         es = 0.6108*(2.7183**((17.27*Ta)/(Ta+237.3)))
#         ea = es + Rh
#         G = 0
#         output = (0.408*A*(Rs-G) + y*((900/24)/(Ta+273))*u2*(es-ea)) / (A + y*(1+0.34*u2))
#         output = np.where(output < 0, 0, output)
#         return output
#     result = []
#     for index, row in wx.iterrows():
#         Ta = row["Ta"]
#         Rh = row["RH"]
#         u2 = row["u2"]
#         Rs = row["Rs"]
#         result.append(theEquation(Ta,Rh,u2,Rs,elevation))
#     plt.figure(figsize=(25, 6))
#     plt.plot(wx.index, result, marker='.', label="ET reference")
#     plt.title(f"Evapotranspiration Reference Values (ETr)    Site: {site_name.iloc[0]}")
#     plt.xlabel('Hours')
#     plt.ylabel("mm/hr")
#     plt.tight_layout()    
#     plt.legend()
#     plt.savefig(f"./static/ETreference.png")


#     # plt.show()
#     print(st["elev"].loc[0])
def theEquation(Ta, Rh, u2, Rs, elevation):
    A = (4098*(0.6108*(2.7183**((17.27*Ta)/(Ta+237.3))))) / ((Ta+273.3)**2)
    y = 0.000665*101.3*(((293-0.0065*elevation)/(293))**5.26)
    es = 0.6108*(2.7183**((17.27*Ta)/(Ta+237.3)))
    ea = es + Rh
    G = 0
    output = (0.408*A*(Rs-G) + y*((900/24)/(Ta+273))*u2*(es-ea)) / (A + y*(1+0.34*u2))
    output = np.where(output < 0, 0, output)
    return output

def processfileetr():
    path = "./static/data.xlsx"
    st, wx, idx = load_fileetr(path)
    site_name = st['site']
    elevation = st["elev"]


    # result = []
    # date = []
    # for index, row in wx.iterrows():
    #     Ta = row["Ta"]
    #     Rh = row["RH"]
    #     u2 = row["u2"]
    #     Rs = row["Rs"]
    #     year = row["year"]
    #     day = row["day"]
    #     hour = row["hour"]

    #     year_start = datetime(year,1,1)
    #     dt = year_start + timedelta(days=day - 1, hours=hour)
    #     dt.replace(minute=0, second=0)
        
    #     date.append(dt)
    #     result.append(theEquation(Ta,Rh,u2,Rs,elevation))

    the_dictionary={}

    for index, row in wx.iterrows():
        Ta = row["Ta"]
        Rh = row["RH"]
        u2 = row["u2"]
        Rs = row["Rs"]
        day = row["day"]
            
        output = theEquation(Ta,Rh,u2,Rs,elevation)

        if day in the_dictionary:
            the_dictionary[day] += output
        else:
            the_dictionary[day] = output

    plt.figure(figsize=(25, 6))
    plt.plot(the_dictionary.keys(), the_dictionary.values(), marker='.', label="ET reference")
    plt.title(f"Evapotranspiration Reference Values (ETr)    Site: {site_name.iloc[0]}")
    plt.xlabel('Date')
    plt.ylabel("mm/hr")
    plt.tight_layout()    
    plt.legend()

    plt.savefig(f"./static/ETreference.png")
    # plt.show()
    # print(st["elev"].loc[0])


def get_ETr(st, wx):
    elevation = st["elev"]
    
    the_dictionary={}

    for index, row in wx.iterrows():
        Ta = row["Ta"]
        Rh = row["RH"]
        u2 = row["u2"]
        Rs = row["Rs"]
        day = row["day"]
            
        output = theEquation(Ta,Rh,u2,Rs,elevation)

        if day in the_dictionary:
            the_dictionary[day] += output
        else:
            the_dictionary[day] = output

    # print(the_dictionary.keys())
    return the_dictionary
