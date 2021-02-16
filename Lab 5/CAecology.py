# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 21:08:24 2021

@author: Brian Chung
This script analyzes an excel file that contains certain pieces of ecological
data about California.
"""
import pandas as pd
import matplotlib.pyplot as py
import os
import numpy as np
from scipy.stats import linregress

# Loading in file
cwd = os.getcwd()
files = os.listdir(cwd)
ecologyDF = pd.read_excel("CAecology.xlsx")
ecologyDF = ecologyDF.dropna(axis="columns")
# %%
# Purpose: analyzing the ecological dataset
# Tasks:
# (1) Calculating elevation bands
# (2) Calculating mean values of various variables in each elevation band
# (3) Creating a function for plotting the dataframe
# (4) Create plots of how these various variables vary with raw elevation
# (5) Create plots of how these variables vary with elevation bands
# (6) Visualize how AET varies with biomass

# (1) Calculating elevation bands
oldCols = ecologyDF.columns.tolist()
ecologyDF["Elevation bands"] = (ecologyDF["Elevation (m)"]/200) + 1
ecologyDF["Elevation bands"] = ecologyDF["Elevation bands"].apply(np.floor)
ecologyDF = ecologyDF.sort_values(by="Elevation (m)")
newCols = ecologyDF.columns.tolist()

# (2) Calculating mean values of various variables in each elevation band
elevGroups = ecologyDF.groupby("Elevation bands")
means = elevGroups["Elevation (m)", "Precip (mm/yr)", "Tmax (oC)", "Tmin (oC)",
                   "AET", "biomass", "P_ET", "2015 tree death"].mean()
means.reset_index(inplace=True)

# (3) Creating a function for plotting the dataframe


def plotData(x, y, dataframe, plotOrder, xTitle, yTitle, figureTitle,
             subplotTitle, plotFormat, labelLegend=None):
    """
    Plots the specified variables from the main dataframe onto a single
    subplot of a figure

    Parameters
    ----------
    x : str
        String that indicates the dataframe column intended to be the x-values
    y : str
        String that indicates the dataframe column intended to be the x-values
    dataframe : Pandas dataframe
        Dataframe containing the data intended to be plotted
    plotOrder : list of integers
        A list of 3 integers to describe the plot order in the format of
        [row, column, plotIndex]
    xTitle : str
        The label for the x-axis of a subplot
    yTitle : str
        The label for the y-axis of a subplot
    figureTitle : str
        Title of the main figure. Will be used to either create a new figure
        or activate an existing figure for edits
    subplotTitle : str
        Title of a subplot of the main figure. Will be used to create a new
        subplot or activate an existing subplot for edits
    plotFormat : str
        How the data will be formatted in each subplot, e.g. the marker type,
        colors, etc
    labelLegend : str, optional
        The label of a dataset that had been ploted on a subplot.
        The default is None.

    Returns
    -------
    None.

    """
    py.figure(num=figureTitle)
    py.subplot(plotOrder[0], plotOrder[1], plotOrder[2])
    py.plot(x, y, plotFormat, data=dataframe, label=labelLegend)
    py.title(subplotTitle)
    py.xlabel(xTitle)
    py.ylabel(yTitle)
    return


# (4) Create plots of how these various variables vary with raw elevation
elevationFigTitle = "Elevation and ecological variables"
py.figure(num=elevationFigTitle, figsize=(20, 15))
plotData("Elevation (m)", "Precip (mm/yr)", ecologyDF, [2, 4, 1],
         "Elevation (m)", "Precipitation (mm/yr)", elevationFigTitle,
         "Precipitation", ".b")
plotData("Elevation (m)", "Tmax (oC)", ecologyDF, [2, 4, 2],
         "Elevation (m)", "Mean annual maximum temperature (degrees Celsius)",
         elevationFigTitle, "Mean annual maximum temperature", ",r")
plotData("Elevation (m)", "Tmin (oC)", ecologyDF, [2, 4, 3],
         "Elevation (m)", "Mean annual minimum temperature (degrees Celsius)",
         elevationFigTitle, "Mean annual minimum temperature", ",g")
plotData("Elevation (m)", "AET", ecologyDF, [2, 4, 4], "Elevation (m)",
         "Actual evapotranspiration (mm/yr)", elevationFigTitle,
         "Actual evapotranspiration", "^c")
plotData("Elevation (m)", "biomass", ecologyDF, [2, 4, 5], "Elevation (m)",
         "Biomass (tons C/ha)", elevationFigTitle, "Biomass", "ok")
plotData("Elevation (m)", "P_ET", ecologyDF, [2, 4, 6], "Elevation (m)",
         "Runoff (mm/yr)", elevationFigTitle, "Runoff", "sm")
plotData("Elevation (m)", "2015 tree death", ecologyDF, [2, 4, 7],
         "Elevation (m)", "Tree death (unitless)", elevationFigTitle,
         "2015 tree death", "1y")
'''The only variables with obvious relationships with elevation are
max and min temperatures. No obvious relationships with elevation can be seen
with other variables'''

# (5) Create plots of how these variables vary with elevation bands
elevBandFig = "Bands of elevation and ecological variables"
py.figure(num=elevBandFig, figsize=(20, 15))
plotData("Elevation bands", "Precip (mm/yr)", means, [2, 4, 1],
         "Elevation band", "Precipitation (mm/yr)", elevBandFig,
         "Precipitation", ".b")
plotData("Elevation bands", "Tmax (oC)", means, [2, 4, 2],
         "Elevation band", "Mean annual maximum temperature (degrees Celsius)",
         elevBandFig, "Mean annual maximum temperature", "or")
plotData("Elevation bands", "Tmin (oC)", means, [2, 4, 3],
         "Elevation band", "Mean annual minimum temperature (degrees Celsius)",
         elevBandFig, "Mean annual minimum temperature", "og")
plotData("Elevation bands", "AET", means, [2, 4, 4], "Elevation band",
         "Actual evapotranspiration (mm/yr)", elevBandFig,
         "Actual evapotranspiration", "^c")
plotData("Elevation bands", "biomass", means, [2, 4, 5], "Elevation band",
         "Biomass (tons C/ha)", elevBandFig, "Biomass", "ok")
plotData("Elevation bands", "P_ET", means, [2, 4, 6], "Elevation band",
         "Runoff (mm/yr)", elevBandFig, "Runoff", "sm")
plotData("Elevation bands", "2015 tree death", means, [2, 4, 7],
         "Elevation band", "Tree death (unitless)", elevBandFig,
         "2015 tree death", "1y")

# (6) Visualize how AET varies with biomass
biomassAET = "Vegetation biomass and AET"
biomassAETregress = linregress(ecologyDF["biomass"], ecologyDF["AET"])
m = biomassAETregress[0]
b = biomassAETregress[1]
r = biomassAETregress[2]
r2 = r**2
r2str = "R-squared: {0:.3f}".format(r2)
ecologyDF["Predicted AET"] = m*ecologyDF["biomass"] + b
print(r2)
py.figure(num=biomassAET, figsize=(8, 6))
plotData("biomass", "AET", ecologyDF, [1, 1, 1],
         "Vegetation biomass (tons C/ha)", "Actual evapotranspiration (mm/yr)",
         biomassAET, biomassAET, "og", "Original data")
plotData("biomass", "Predicted AET", ecologyDF, [1, 1, 1],
         "Vegetation biomass (tons C/ha)", "Actual evapotranspiration (mm/yr)",
         biomassAET, biomassAET, "-m", "Regression")
py.text(320, 210, r2str)
py.legend()
