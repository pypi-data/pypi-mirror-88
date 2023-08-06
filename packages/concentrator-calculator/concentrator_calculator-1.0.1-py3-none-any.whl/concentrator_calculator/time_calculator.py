import pandas as pd
import numpy as np
from scipy.stats import linregress
from datetime import timedelta



## function to calculate concentrator runtime from time data
def calculate_time(data, concentrator, liquid, temperature, st_vol, des_vol):
    ## import the data
    data = pd.read_excel(data, sheet_name = concentrator)

    ## filter data to selected subset of liquid / temperature combination
    data = data.loc[(data['Temperature [°C]'] == int(temperature)) & (data['Liquid'] == liquid)]

    ## fit a curve to the data - may need to be optimized with more data if available
    z = np.polyfit(x = data['Volume [μl]'], y = data['time [s]'], deg = 3)
    p = np.poly1d(z)

    ## return difference only if desired volume != 0
    if st_vol == 0 and des_vol == 0:
        return ''
    elif des_vol != 0:
        return str(timedelta(seconds = int(p(st_vol) - p(des_vol))))
    else:
        return str(timedelta(seconds = int(p(st_vol))))
