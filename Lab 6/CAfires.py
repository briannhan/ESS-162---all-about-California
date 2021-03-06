# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 17:06:06 2021

@author: Brian Chung
Analyzes time-series burned area data in California
"""
import pandas as pd
import os
import matplotlib.pyplot as py
from pathlib import Path
from scipy.stats import linregress
import numpy as np

# %%
# Reading in data
cwd = Path(os.getcwd())
folders = os.listdir(cwd)
firePerimeterFolder = cwd/"Fire Perimeter"
firePerimeterFiles = os.listdir(firePerimeterFolder)
fireHistoryPath = firePerimeterFolder/'Fire history.xlsx'
fireHistory = pd.read_excel(io=fireHistoryPath)

# %%
# Purpose: Cleaning data
# Tasks:
# (1) Dropping unnecessary columns
# (2) Converting area from square meters to hectares
# (3) Filtering out any data before 1900. Data before 1900 were sparse with
# data present for the years 1878, 1895, 1896, 1898

# (1) Dropping unnecessary columns
fireHistory = fireHistory.dropna(axis="index", subset=["YEAR_", "Shape_Area"])
'''It seems like dropping NA rows based on "YEAR_" is enough, no need to
add in "Shape_Area", although adding in "Shape_Area" doesn't change the
eventual number of rows'''
fireHistory = fireHistory[fireHistory["STATE"] == "CA"]
oldColumns = fireHistory.columns.tolist()
columnsToRemove = ["OBJECTID", "STATE", "AGENCY", "UNIT_ID", "FIRE_NAME",
                   "INC_NUM", "COMMENTS", "REPORT_AC", "FIRE_NUM", "C_METHOD",
                   "Shape_Length"]
fireHistory = fireHistory.drop(labels=columnsToRemove, axis="columns")
newColumns = fireHistory.columns.tolist()

# (2) Converting area from square meters to hectares
fireHistory["Shape_Area"] = fireHistory["Shape_Area"]/10000

# (3) Filtering out any data before 1900
fireHistory = fireHistory[fireHistory["YEAR_"] >= 1900]
# %%
# Making yearly calculations
groupByObject = fireHistory.groupby("YEAR_")
totalBurnedArea = groupByObject["Shape_Area"].sum()
avgFireSize = groupByObject["Shape_Area"].mean()
numOfFires = groupByObject["YEAR_"].count()

# To get the most common causes each year, that's a bit difficult, so...
causesNum = fireHistory.groupby(["YEAR_", "CAUSE"])["YEAR_"].count()
# This counts the number of fires by their causes each year

# %%
# Making plots
# Tasks:
# (1) Write a function to plot simple series with only 1 index
# (2) Plot total and mean burned area and the number of fires against time


# (1) Write a function to plot simple series with only 1 index


def plotSimpleSeries(figTitle, figSize, subplotTitle, subplotOrder, series,
                     xAxis, yAxis, markers, subplotLegend=None):
    """
    Plots time-series data from a simple series with only 1 index. Can make 1
    or multiple subplots on 1 figure.

    Parameters
    ----------
    figTitle : str
        The title of the overall figure to be plotted. When called with
        py.figure(), the figure with this title is either constructed from
        scratch if not existing or activated if already created.
    figSize : tuple of 2 integers
        Tuple that specifies the width and height of the figure in the format
        of (length, width).
    subplotTitle : str
        The title of the subplot to be plotted. When called with py.plot(),
        will either create a new subplot with this title or activate an
        existing subplot for modifications
    subplotOrder : list of 3 integers
        Specifies the order of a subplot in the order of
        [row, column, subplot position]
    series : Pandas series
        The Pandas series for which time-series data will be plotted
    xAxis : str
        The title of the x-axis
    yAxis : str
        The title of the y-axis
    markers : str
        The marker type and color of the data to be plotted
    subplotLegend : str
        What will be displayed in the subplot legend should the subplot have
        a legend

    Returns
    -------
    None.

    """
    py.figure(num=figTitle, figsize=figSize)
    py.subplot(subplotOrder[0], subplotOrder[1], subplotOrder[2])
    py.title(subplotTitle)
    py.xlabel(xAxis)
    py.ylabel(yAxis)
    py.plot(series.index, series, markers, label=subplotLegend)
    if type(subplotLegend) is not None:
        py.legend()
    return


# (2) Plot total and mean burned area and the number of fires against time
areaFireNumFig = "Burned area and number of fires time series"
areaTimeSeries = "Burned area"
fireNumTimeSeries = "Number of fires"
meanFireSize = "Mean fire size"
'''
plotSimpleSeries(areaFireNumFig, (20, 10), areaTimeSeries, [2, 2, 1],
                 totalBurnedArea, "Year", "Burned Area (ha)", "o-r",
                 "Total burned area")  # Total burned area
plotSimpleSeries(areaFireNumFig, (20, 10), areaTimeSeries, [2, 2, 1],
                 avgFireSize, "Year", "Burned Area (ha)",
                 ".-k", "Mean fire size")  # Mean burned area per fire
plotSimpleSeries(areaFireNumFig, (20, 10), fireNumTimeSeries, [2, 2, 2],
                 numOfFires, "Year", "Number of fires", "o-g",
                 "Number of fires")  # Number of fires
plotSimpleSeries(areaFireNumFig, (20, 10), meanFireSize, [2, 2, 3],
                 avgFireSize, "Year", "Mean fire size (ha)",
                 "o-k", "Mean fire size")  # Mean burned area per fire'''
# %%
# Purpose: Perform and plot linear regressions
# Tasks:
# (1) Perform time-series linear regressions of total burned area, average fire
# size, and number of fires and linear regressions of total burned area vs
# fire size and total area vs number of fires
# (2) Plot time-series linear regressions of all on original time-series
# (3) Create a function to plot 2 numpy arrays, lists, or Pandas series
# (4) Plot relationships between total burned area, number of fires, and fire
# size


# (1) Perform linear regressions of total burned area, average fire size, and
# number of fires
totalBurnedRegress = linregress(totalBurnedArea.index, totalBurnedArea)
r2total = totalBurnedRegress[2]**2
r2strTotal = "R-squared: {0:.3f}".format(r2total)
fireSizeRegress = linregress(avgFireSize.index, avgFireSize)
r2fireSize = fireSizeRegress[2]**2
r2strFireSize = "R-squared: {0:.3f}".format(r2fireSize)
fireNumRegress = linregress(numOfFires.index, numOfFires)
r2fireNum = fireNumRegress[2]**2
r2strFireNum = "R-squared: {0:.3f}".format(r2fireNum)
totalVsFireNum = linregress(numOfFires, totalBurnedArea)
totalVsSize = linregress(avgFireSize, totalBurnedArea)
years = np.array(totalBurnedArea.index.tolist())

# (2) Plot time-series linear regressions of all on original time-series
'''
totalBurnedEstimate = totalBurnedRegress[0]*years + totalBurnedRegress[1]
py.subplot(2, 2, 1)
py.plot(years, totalBurnedEstimate, "-m", label="Total burned area regression")
# py.legend()
py.text(1898, 490000, r2strTotal)
fireNumEstimate = fireNumRegress[0]*years + fireNumRegress[1]
py.subplot(2, 2, 2)
py.plot(years, fireNumEstimate, "-m", label="Number of fires regression")
# py.legend()
py.text(1898, 500, r2strFireNum)
fireSizeEstimate = fireSizeRegress[0]*years + fireSizeRegress[1]
py.subplot(2, 2, 3)
py.plot(years, fireSizeEstimate, "-m", label="Fire size regression")
py.legend()
py.text(1898, 1350, r2strFireSize)'''

# (3) Create a function to plot 2 numpy arrays, lists, or Pandas series


def plot2Vars(figTitle, figSize, subplotTitle, subplotOrder, xValues, yValues,
              xTitle, yTitle, markers, labelLegend=None,
              r=None, r2Coords=None):
    """
    Plots 2 numpy arrays or lists or Pandas series. Can plot on a figure with
    a single subplot or a figure with multiple subplots. Can plot on existing
    plots or create new plots altogether.

    Parameters
    ----------
    figTitle : str
        The title of the overall figure to be plotted. When called with
        py.figure(), the figure with this title is either constructed from
        scratch if not existing or activated if already created.
    figSize : tuple of 2 integers
        Tuple that specifies the width and height of the figure in the format
        of (length, width).
    subplotTitle : str
        The title of the subplot to be plotted. When called with py.plot(),
        will either create a new subplot with this title or activate an
        existing subplot for modifications
    subplotOrder : list of 3 integers
        Specifies the order of a subplot in the order of
        [row, column, subplot position]
    xValues : 1-D Numpy array, list of integers or floats, or Pandas series
        The values to be plotted on the x-axis
    yArray : 1-D Numpy array, list of integers or floats, or Pandas series
        The values to be plotted on the y-axis
    xTitle : str
        The title of the x-axis
    yTitle : str
        The title of the y-axis
    markers : str
        The marker type and color of the data to be plotted
    labelLegend : str, OPTIONAL
        What will be displayed in the subplot legend should the subplot have
        a legend. Default is None because this is optional
    r : float, OPTIONAL
        The correlation coefficient between the x & y values
    r2Coords : list of 2 numbers, OPTIONAL
        r2 will be annotated onto a subplot. This list represents the
        [x, y] coordinates of the left-hand side of the annotation that
        contains r2.

    Returns
    -------
    None.

    """
    py.figure(num=figTitle, figsize=figSize)
    py.subplot(subplotOrder[0], subplotOrder[1], subplotOrder[2])
    py.title(subplotTitle)
    py.xlabel(xTitle)
    py.ylabel(yTitle)
    py.plot(xValues, yValues, markers, label=labelLegend)
    if type(labelLegend) is not None:
        py.legend()
    if type(r) == np.float64:
        r = r**2
        r2str = "R-squared: {0:.3f}".format(r)
        py.text(r2Coords[0], r2Coords[1], r2str)
    return


# (4) Plot relationships between total burned area, number of fires, and fire
# size
totalBurnedAreaFig = "Components of total burned area"
totalVsNumEstimate = totalVsFireNum[0]*numOfFires + totalVsFireNum[1]
numOfFiresSubplot = "Total burned area vs number of fires"
'''
plot2Vars(totalBurnedAreaFig, (20, 15), numOfFiresSubplot, [1, 2, 1],
          numOfFires, totalBurnedArea, "Number of fires per year",
          "Total burned area per year (ha)", "og", "Original data")
plot2Vars(totalBurnedAreaFig, (20, 15), numOfFiresSubplot, [1, 2, 1],
          numOfFires, totalVsNumEstimate, "Number of fires per year",
          "Total burned area per year (ha)", "-m", "Regression",
          totalVsFireNum[2], [500, 600000])

totalVsSizeEstimate = totalVsSize[0]*avgFireSize + totalVsSize[1]
numOfFiresSubplot = "Total burned area vs fire size"
plot2Vars(totalBurnedAreaFig, (20, 15), numOfFiresSubplot, [1, 2, 2],
          avgFireSize, totalBurnedArea, "Mean fire size per year (ha)",
          "Total burned area per year (ha)", "og", "Original data")
plot2Vars(totalBurnedAreaFig, (20, 15), numOfFiresSubplot, [1, 2, 2],
          avgFireSize, totalVsSizeEstimate, "Mean fire size per year (ha)",
          "Total burned area per year (ha)", "-m", "Regression",
          totalVsSize[2], [0, 600000])'''
# %%
# Purpose: Analyzing how the causes of wildfires change over time
# Tasks:
# (1) Calculating the fire size and total burned area by fire causes annually
# (2) Wrangling the fire size, total burned area, and number of fires by
# causes into a single dataframe
# (3) Distinguishing between all human causes and natural causes (lightning)
# (4) Performing regressions over time of each individual cause and the
# combined human & natural causes
#   (4a) Creating a function to do the regression
#   (4b) Call the function on the causes dataframes
# (5) Visualizing the causes over time

# (1) Calculating the fire size and total burned area by fire causes annually
# The number of fires by cause had already been calculated by this point
sizeByCause = fireHistory.groupby(["YEAR_", "CAUSE"])["Shape_Area"].mean()
totalAbyCause = fireHistory.groupby(["YEAR_", "CAUSE"])["Shape_Area"].sum()

# (2) Wrangling the fire size, total burned area, and number of fires
causesPath = firePerimeterFolder/'Causes description.xlsx'
causesDescribed = pd.read_excel(causesPath).dropna(axis=1)
causesDict = {}
for index, row in causesDescribed.iterrows():
    cause = row["Cause Code"]
    description = row["Description"]
    causesDict[cause] = description
causesNum = causesNum.to_frame().unstack().droplevel(level=0, axis=1)
causesNum = causesNum.reset_index().fillna(value=0, axis="columns")
sizeByCause = sizeByCause.to_frame().unstack().droplevel(level=0, axis=1)
sizeByCause = sizeByCause.reset_index().fillna(value=0, axis="columns")
totalAbyCause = totalAbyCause.to_frame().unstack()
totalAbyCause = totalAbyCause.droplevel(level=0, axis=1).reset_index()
totalAbyCause = totalAbyCause.fillna(value=0, axis="columns")

# (3) Distinguishing between all human causes and natural causes (lightning)
'''Each integer in the following cases represents a column since the original
data values for causes are integers
'''
causesNum["Manmade"] = (causesNum[2] + causesNum[3] + causesNum[4]
                        + causesNum[5] + causesNum[6] + causesNum[7]
                        + causesNum[8] + causesNum[10] + causesNum[11]
                        + causesNum[12] + causesNum[13] + causesNum[15]
                        + causesNum[16] + causesNum[18] + causesNum[19])
causesNum["Natural"] = causesNum[1]
causesNum["Miscellaneous/Unknown"] = causesNum[9] + causesNum[14]
causesNum = causesNum.rename(mapper=causesDict, axis="columns")

totalAbyCause["Manmade"] = (totalAbyCause[2] + totalAbyCause[3]
                            + totalAbyCause[4] + totalAbyCause[5]
                            + totalAbyCause[6] + totalAbyCause[7]
                            + totalAbyCause[8] + totalAbyCause[10]
                            + totalAbyCause[11] + totalAbyCause[12]
                            + totalAbyCause[13] + totalAbyCause[15]
                            + totalAbyCause[16] + totalAbyCause[18]
                            + totalAbyCause[19])
totalAbyCause["Natural"] = totalAbyCause[1]
totalAbyCause["Miscellaneous/Unknown"] = totalAbyCause[9] + totalAbyCause[14]
totalAbyCause = totalAbyCause.rename(mapper=causesDict, axis="columns")

sizeByCause["Manmade"] = totalAbyCause["Manmade"]/causesNum["Manmade"]
sizeByCause = sizeByCause.fillna(value=0, axis="columns")
sizeByCause["Natural"] = sizeByCause[1]
sizeByCause["Miscellaneous/Unknown"] = sizeByCause[9] + sizeByCause[14]
sizeByCause = sizeByCause.rename(mapper=causesDict, axis=1)
causesColumns = causesNum.columns.tolist()[1:]

# (4) Performing regressions over time of each individual cause and the
# combined human & natural causes
#   (4a) Creating a function to do the regression
for cause in causesColumns:
    regress = linregress(causesNum["YEAR_"], causesNum[cause])
    indexList = causesDescribed[causesDescribed["Description"] == cause].index.tolist()
    print(indexList)
    '''causesDescribed[indexVal, "m_fireNum"] = regress[0]
    causesDescribed[indexVal, "b_fireNum"] = regress[1]
    causesDescribed[indexVal, "r_fireNum"] = regress[2]
    causesDescribed[indexVal, "r2_fireNum"] = regress[2]**2
    causesDescribed[indexVal, "p_fireNum"] = regress[3]'''
