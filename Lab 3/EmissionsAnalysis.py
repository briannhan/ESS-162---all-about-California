# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 21:56:01 2021

@author: Brian Chung
This script analyzes how greenhouse gas emissions in California changes by year
"""
import pandas as pd
from scipy.stats import linregress
import os

# importing the excel spreadsheet of GHG emissions by category by year
cwd = os.getcwd()
files = os.listdir(cwd)
data = pd.read_excel(files[-3], skiprows=4)
# Units are in millions of tons of CO2 equivalent, which takes into account
# GWP of all GHGs

# %%
# Purpose: Analyzing the data to see trends over time

# Calculating emissions per year as percent of total emissions of a year
percentTot = data.copy()
percentTot.iloc[:, 1:] = percentTot.iloc[:, 1:]*100/percentTot.iloc[32, 1:]
dataColumns = data.columns.tolist()
years = dataColumns[1:]

# Calculating annual change of a source using linear regression as well as the
# annual change in emissions of a category as percent of initial emissions of
# that category in 2000
# Creating a for loop to do the linear regression
for index, row in data.iterrows():
    rowList = row.tolist()
    emissions = rowList[1:]
    results = linregress(x=years, y=emissions)
    slope = results[0]
    r2 = results[2]**2
    data.loc[index, "slope (Tg CO2e/yr)"] = slope
    data.loc[index, "R-squared"] = r2
    data.loc[index, "Percent change from 2000/yr"] = slope/row.loc[2000]

# Calculating change in emissions between 2000 and 2016
data["2000 - 2016"] = data[2000] - data[2016]
# %%
# Purpose: Sorting by the largest sources in 2016 to determine largest
# sources in 2016

newColumns = data.columns.tolist()
print(newColumns)
data = data.sort_values(by=2016, ascending=False)
percentTot = percentTot.sort_values(by=2016, ascending=False)

# %%
# Purpose: Sorting by the greatest reduction in emissions between 2000 and 2016
data = data.sort_values(by="2000 - 2016", ascending=False)
