# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 16:59:43 2021

@author: Brian Chung
This script analyzes California's hydrology
"""
import pandas as pd
import os
import matplotlib.pyplot as py
from scipy.stats import linregress
import numpy as np

# Reading in and cleaning data
cwd = os.getcwd()
filesLab4 = os.listdir(cwd)
hydroData = pd.read_excel(io="CAwater balance 2.xlsx")
hydroData = hydroData.dropna(axis=1)
# %%
# Purpose: Analyzing the data for the state as a whole
# Tasks:
# (1) Adding columns for calculating the difference between precipitation
# and evapotranspiration (the amount of water that remains in an ecosystem
# after precipitation and evapotranspiration) and this difference as a fraction
# of precipitation (how much of precipitation remains in an ecosystem)
# (2) Analyzing the relationship between air temperature & PET by conducting
# a regression and plotting the relationship
# (3) Summing P - ET in the Sierra Nevada ecoregion

oldCols = hydroData.columns.tolist()

# (1) Adding columns for calculating the difference between precipitation
# and evapotranspiration (the amount of water that remains in an ecosystem
# after precipitation and evapotranspiration) and this difference as a fraction
# of precipitation (how much of precipitation remains in an ecosystem)
hydroData["precip - ET"] = hydroData["precip2normal"] - hydroData["AET"]
hydroData["(precip - ET)/precip"] = (hydroData["precip - ET"]
                                     / hydroData["precip2normal"])
newCols = hydroData.columns.tolist()


# (2) Analyzing the relationship between air temperature & PET by conducting
# a regression and plotting the relationship

# Conducting the regression
regressResults = linregress(hydroData["Tmaxnormal"], hydroData["PET"])
r2 = regressResults[2]**2
slope = regressResults[0]
yIntercept = regressResults[1]
relationship = hydroData["Tmaxnormal"]*slope + yIntercept
r2str = "R-squared: {0:.3f}".format(r2)

# Plotting the relationship
py.figure(num="Relationship between air temperature and PET", figsize=(8, 6))
py.subplot(1, 1, 1)
py.plot("Tmaxnormal", "PET", "oy", data=hydroData, label="Actual values")
py.plot(hydroData["Tmaxnormal"], relationship, "-r", label="Regression")
py.title("Relationship between air temperature and PET")
py.xlabel("Mean annual maximum temperature (degrees Celsius)")
py.ylabel("PET (mm/yr)")
py.text(2, 1500, r2str)
py.legend()


# (3) Calculating total runoff in the Sierra Nevada ecoregion
# Summing runoff for each ecoregion
runoffMeans = hydroData.groupby("CAecoregion4normal")["precip - ET"].mean()
sierraNevadaRunoffHeight = runoffMeans[5]  # units mm/yr
acreToM2 = 4046.86  # square meters in 1 acre
feetToM = 0.3048  # meters in 1 feet
SNrunoffV = sierraNevadaRunoffHeight*52/(acreToM2*feetToM)  # millions acre-ft
# %%
# Purpose: Analyzing the Kings River Basin
# Tasks:
# (1) Calculating means for various variables of the Kings River Basin
# (2) Writing a function to plot a figure with various subplots
# (3) Analyzing the relationships between elevation and various hydrographical
# variables by plotting them


# (1) Calculating means for various variables of the Kings River Basin
kingsRiver = hydroData[hydroData["HUC8"] == 40]
meansDict = {"Precip (mm/yr)": kingsRiver["precip2normal"].mean(),
             "Tmax (degrees C)": kingsRiver["Tmaxnormal"].mean(),
             "PET (mm/yr)": kingsRiver["PET"].mean(),
             "AET (mm/yr)": kingsRiver["AET"].mean(),
             "P - ET (mm/yr)": kingsRiver["precip - ET"].mean(),
             "(P - ET)/P": kingsRiver["(precip - ET)/precip"].mean()}

# (2) Writing a function for plotting scatter & line plots of 2 variables on
# a figure of a single plot


def plot2Vars(dataframe, plotOrder, figTitle, plotTitle,
              x, y, xTitle, yTitle, plotFormat, labelLegend=None):
    """Plots 2 variables on a single subplot of a figure. Can be called
    multiple times to either (1) plot several dependent variables on a single
    subplot or (2) make multiple subplots for different dependent variables

    Parameters
    ----------
    dataframe : Pandas dataframe
        Dataframe of the data that will be plotted
    plotOrder : list
        A list of integers that detail the position of a specific plot in the
        format of [row, column, indexed position].
    figTitle : str
        This string will be used as the figure title and will be used to
        "activate" a specific overall figure that had already been created to
        edit the figure or used in creating a new figure and setting its title
    plotTitle : str
        This string will be used to set the title of a specific plot
    x : str
        Variable to be plotted on the x-axis
    y : str
        Variable to be plotted on the y-axis
    xTitle : str
        Title for the x-axis
    yTitle : str
        Title for the y-axis
    plotFormat : str
        The format for the curve in the figure
    labelLegend : str, default None
        String that describes the dataset plotted in the legend

    Returns
    -------
    None.
    """
    py.figure(num=figTitle)
    py.subplot(plotOrder[0], plotOrder[1], plotOrder[2])
    py.plot(x, y, plotFormat, data=dataframe, label=labelLegend)
    py.title(plotTitle)
    py.xlabel(xTitle)
    py.ylabel(yTitle)
    return


# (3) Analyzing the relationships between elevation and various hydrographical
# variables by plotting them
# I'm gonna plot them using a figure with multiple subplots
kingsRiverTitle = "Elevation vs various hydrographical variables"
py.figure(num=kingsRiverTitle, figsize=(20, 15))
plot2Vars(kingsRiver, [2, 3, 1], kingsRiverTitle, "Kings River Precipitation",
          "DEMnormal", "precip2normal", "Elevation (m)",
          "Precipitation (mm/yr)", "oy")
plot2Vars(kingsRiver, [2, 3, 2], kingsRiverTitle, "Kings River PET",
          "DEMnormal", "PET", "Elevation (m)", "PET (mm/yr)", "hg")
plot2Vars(kingsRiver, [2, 3, 3], kingsRiverTitle, "Kings River AET",
          "DEMnormal", "AET", "Elevation (m)", "AET (mm/yr)", "sr")
plot2Vars(kingsRiver, [2, 3, 4], kingsRiverTitle, "Kings River P - ET",
          "DEMnormal", "precip - ET", "Elevation (m)", "precip - ET (mm/yr)",
          "*c")
plot2Vars(kingsRiver, [2, 3, 5], kingsRiverTitle, "(P - ET)/P", "DEMnormal",
          "(precip - ET)/precip", "Elevation (m)", "(P - ET)/P", "+m")

# %%
# Purpose: Calculating how much runoff will be produced by Kings River Basin
# with 6 degrees Celsius warming. This calculation is made on the basis of
# varying elevation and hydrographical variables that don't actually vary with
# time, so this estimate might be different from actual values that will come
# about with actual climate warming.
# (1) Doing linear regressions of precipitation and AET vs temperature in
# the Kings River Basin
# (2) Adding 6 degrees to temperature readings in each location in the
# watershed as well as adding the expected rise in AET calculated from the
# linear regressions
# (3) plotting original data (precip, AET, runoff) vs temperature and new
# data vs temperature along with their regressions. Each of these 3 variables
# will be plotted on a separate plot in the same figure as the other plots.
# (4) Summing up runoff (P - ET) if there's no temperature change
# (5) Calculating runoff for each point in the watershed if there's a
# temperature increase
# (6) Summing up runoff (P - ET) from the scenario of 6 degrees C increase
# (7) Subtracting the sums from step (5) and (3) to calculate the change in
# runoff

# (1) Doing linear regressions of precipitation and AET vs temperature in
# the Kings River Basin
precipRegress = linregress(kingsRiver["Tmaxnormal"],
                           kingsRiver["precip2normal"])
mPrecip = precipRegress[0]
bPrecip = precipRegress[1]
r2Precip = precipRegress[2]**2

etRegress = linregress(kingsRiver["Tmaxnormal"], kingsRiver["AET"])
mET = etRegress[0]
bET = etRegress[1]
r2ET = etRegress[2]**2


# (2) Adding 6 degrees to temperature readings in each location in the
# watershed as well as adding the expected rise in precipitation and AET
# calculated from the linear regressions


def etEstimate(temperature):
    """Provides an estimate of evapotranspiration in the Kings River watershed
    at a given temperature by using the regression
    results above.

    Parameters
    ----------
    temperature : float or array of numbers
        The temperature(s) of interest for which estimate(s) of
        evapotranspiration will be provided.

    Returns
    -------
    etEstimate
    """
    etEstimate = mET*temperature + bET
    return etEstimate


def pptEstimate(temperature):
    """Provides an estimate of temperature in the Kings River watershed
    at a given temperature by using the regression
    results above.

    Parameters
    ----------
    temperature : float or array of numbers
        The temperature(s) of interest for which estimate(s) of
        precipitation will be provided.

    Returns
    -------
    pptEstimate
    """
    pptEstimate = mPrecip*temperature + bPrecip
    return pptEstimate


kingsRiver["tempCC"] = kingsRiver["Tmaxnormal"] + 6
kingsETchange = etEstimate(6) - etEstimate(0)
kingsRiver["AET_CC"] = kingsRiver["AET"] + kingsETchange
kingsPptChange = pptEstimate(6) - pptEstimate(0)
kingsRiver["precipCC"] = kingsRiver["precip2normal"] + kingsPptChange

kingsRiver["runoffAET"] = kingsRiver["precip2normal"] - kingsRiver["AET_CC"]
kingsRiver["runoffPPT"] = kingsRiver["precipCC"] - kingsRiver["AET"]
kingsRiver["runoffCombined"] = kingsRiver["precipCC"] - kingsRiver["AET_CC"]


# (3) plotting original data (precip, AET, runoff) vs temperature and new
# data vs temperature along with their regressions. Each of these 3 variables
# will be plotted on a separate plot in the same figure as the other plots.
kingsCCtitle = "Kings River Basin's AET and runoff with climate change"
py.figure(num=kingsCCtitle, figsize=(8, 10))
kingsRiver["Theo Temp"] = np.linspace(3, 32, num=232)

# Plotting precipitation
# kingsRiver["Regress Precip"] = mPrecip*kingsRiver["Theo Temp"] + bPrecip
# plot2Vars(kingsRiver, [2, 2, 1], kingsCCtitle, "Precipitation", "Tmaxnormal",
#           "precip2normal", "Mean annual max temperature (degrees C)",
#           "Precipitation (mm/yr)", "ob", "Original Precipitation")
# plot2Vars(kingsRiver, [2, 2, 1], kingsCCtitle, "Precipitation", "tempCC",
#           "precipCC", "Mean annual max temperature (degrees C)",
#           "Precipitation (mm/yr)", "oy", "6 degrees C increase")
# plot2Vars(kingsRiver, [2, 2, 1], kingsCCtitle, "Precipitation", "Theo Temp",
#           "Regress Precip", "Mean annual max temperature (degrees C)",
#           "Precipitation (mm/yr)", "-m", "Regression")
# py.legend()

# Plotting evapotranspiration
kingsRiver["Regress ET"] = mET*kingsRiver["Theo Temp"] + bET
plot2Vars(kingsRiver, [2, 1, 1], kingsCCtitle, "Evapotranspiration",
          "Tmaxnormal", "AET", "Mean annual max temperature (degrees C)",
          "Evapotranspiration (mm/yr)", "sb", "Original Evapotranspiration")
plot2Vars(kingsRiver, [2, 1, 1], kingsCCtitle, "Evapotranspiration", "tempCC",
          "AET_CC", "Mean annual max temperature (degrees C)",
          "Evapotranspiration (mm/yr)", "sr", "6 degrees C increase")
plot2Vars(kingsRiver, [2, 1, 1], kingsCCtitle, "Evapotranspiration",
          "Theo Temp", "Regress ET", "Mean annual max temperature (degrees C)",
          "Evapotranspiration (mm/yr)", "-m", "Regression")  # Regression
py.legend()

# Plotting runoff
plot2Vars(kingsRiver, [2, 1, 2], kingsCCtitle, "Runoff", "Tmaxnormal",
          "precip - ET", "Mean annual max temperature (degrees C)",
          "Runoff (mm/yr)", "^b", "Original Runoff")  # Current data
plot2Vars(kingsRiver, [2, 1, 2], kingsCCtitle, "Runoff", "tempCC",
          "runoffAET", "Mean annual max temperature (degrees C)",
          "Runoff (mm/yr)", "^r", "6 degrees C increase")
py.legend()
