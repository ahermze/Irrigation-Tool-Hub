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


def get_Kc(start_day, end_day):
    length = end_day - start_day
    the_dictionary = {}

    # Values from page 65:
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
           