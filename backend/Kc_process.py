import numpy as np
from pandas import read_excel, concat, DataFrame, Index, MultiIndex, date_range
from numpy import empty, full
import matplotlib.pyplot as plt
from pathlib import Path


from pandas import read_excel, concat, DataFrame, Index, MultiIndex, date_range
from numpy import empty, full
import matplotlib.pyplot as plt

from datetime import datetime, timedelta

def loadit(file_name, sheet):
    return read_excel(file_name, sheet_name=sheet)

def load_filegs(file_name):
    #### Loading the information
    return loadit(file_name, 'canopy temperature'), loadit(file_name, 'sites')

def process_Kc():
    
    path = "./static/data.xlsx"
    tc, st = load_filegs(path)
    
    site_name = st['site']
    year = tc["year"].iloc[0]

    start_day = int(tc.iloc[0]["DOY"])
    end_day = int(tc.iloc[-1]["DOY"])
    length = end_day - start_day

    # Values from:
    # https://asabe.org/portals/0/apubs/books/ism/irrigationsystemsmanagement.pdf
    initial = 0.15
    top = 1.15
    end = 0.15


    # stable
    fs1 = 0.18 * length
    # increasing
    fs2 = 0.41 * length
    # stable
    fs3 = 0.71 * length
    # decreasing

    fs1 = float(int(fs1*24))/24 + start_day
    fs2 = float(int(fs2*24))/24 + start_day
    fs3 = float(int(fs3*24))/24 + start_day

    kc = []
    date = []

    for day in range(length):
        day = day + start_day
        for hour in range(24):
            hour = hour + 1
            time = day + (hour/24)

            if time <= fs1:
                kc.append(initial)
            elif time <= fs2:
                span = fs2 - fs1
                current = time - fs1
                percentage = current / span
                kc.append((top - initial) * percentage + initial)
            elif time <= fs3:
                kc.append(top)
            else:
                span = end_day - fs3
                current = time - fs3
                percentage = current / span
                kc.append(top - ((top - end) * percentage))

            year_start = datetime(year,1,1)
            dt = year_start + timedelta(days=day - 1, hours=hour)
            dt.replace(minute=0, second=0)
            date.append(dt)

    plt.figure(figsize=(25, 6))  # Width of 12 inches and height of 6 inches
    plt.plot(date, kc, label="Crop Coefficient")

    plt.title(f"Crop Coefficient Values (Kc)    Site: {site_name.iloc[0]}")
    plt.xlabel('Date')
    plt.legend()
    plt.grid()
    plt.savefig(f"./static/Kc_values.png")
    # plt.show()

def get_Kc(start_day, end_day):
    length = end_day - start_day
    the_dictionary = {}

    # Values from:
    # https://asabe.org/portals/0/apubs/books/ism/irrigationsystemsmanagement.pdf
    initial = 0.15
    top = 1.15
    end = 0.15

    fs1 = 0.18 * length
    fs2 = 0.41 * length
    fs3 = 0.71 * length

    fs1 = float(int(fs1*24))/24 + start_day
    fs2 = float(int(fs2*24))/24 + start_day
    fs3 = float(int(fs3*24))/24 + start_day

    for day in range(length):

        day = day + start_day

        if day <= fs1:
            output = initial
        elif day <= fs2:
            span = fs2 - fs1
            current = day - fs1
            percentage = current / span
            output = (top - initial) * percentage + initial
        elif day <= fs3:
            output = top
        else:
            span = end_day - fs3
            current = day - fs3
            percentage = current / span
            output = top - ((top - end) * percentage)

        if day in the_dictionary:
            the_dictionary[day] += output
        else:
            the_dictionary[day] = output
    
    return the_dictionary
           