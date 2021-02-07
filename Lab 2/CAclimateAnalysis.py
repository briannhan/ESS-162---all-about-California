# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 19:26:35 2021

@author: Brian Chung
This script does some analysis of California's climate for Lab 2. Specifically,
it analyzes how latitude and altitude affects precipitation in California.
"""
import pandas as pd
import matplotlib.pyplot as py
py.style.use("dark_background")
# %%
# Purpose: Reading in & pre-processing CA climate data
# Reading in Excel spreadsheet of climate data of various locations in CA
climateDF = pd.read_excel("CAclimate.xlsx")

# Dropping empty & unnamed columns
oldColumns = climateDF.columns.tolist()
colsToDrop = oldColumns[7:]
climateDF = climateDF.drop(labels=colsToDrop, axis="columns")
# %%
# Function to make & save figures


def plotClimate(indepVar, xUnits, depVar, yUnits, dataframe):
    """Generates & saves plots of how various climate variables vary with
    environmental factors such as elevation, latitude, & topography

    Parameters
    ----------
    indepVar : str
        String that is the independent variable to be plotted on the x-axis
    depVar : str
        String that is the dependent variable to be plotted on the y-axis
    dataframe : Pandas dataframe
        Filtered dataframe containing x & y of a specific region

    Returns
    -------
    None.
    """
    dataframe = dataframe.sort_values(by=[indepVar])
    figTitle = "{1} vs. {0}".format(indepVar, depVar)
    py.figure(num=figTitle, figsize=(20, 12))
    py.subplot(1, 1, 1)
    py.plot(indepVar, depVar, data=dataframe)
    py.scatter(indepVar, depVar, data=dataframe)
    xAxis = "{0} ({1})".format(indepVar, xUnits)
    yAxis = "{0} ({1})".format(depVar, yUnits)
    py.xlabel(xAxis)
    py.ylabel(yAxis)
    py.title(figTitle)
    py.savefig(fname=figTitle + ".jpg")
    return


# %%
# Analyzing how precipitation changes with latitude in ecoregions 1 & 12
# between altitudes of 0 - 200 m
ecoregionBool = climateDF["Eco Region"].isin([1, 12])
latPptDF = climateDF[ecoregionBool & (climateDF["Elevation"] <= 200)]
# Plotting precipitation as a function of latitude
plotClimate("Latitude", "decimal degrees", "Precip", "mm/yr", latPptDF)

# %%
# Analyzing how daytime temperature in the Central Valley varies with latitude
CVEcoRegionbool = climateDF["Eco Region"].isin([7])
CVlatTempDF = climateDF[CVEcoRegionbool & (climateDF["Elevation"] <= 200)]
# Plotting daytime temperature in the Central Valley as a function of latitude
plotClimate("Latitude", "decimal degrees", "Tmax", "degrees C", CVlatTempDF)

# %%
# Purpose: analyze how various variables vary with longitude in the latitude
# band 36.8 - 37.2 degrees North
latBool = (climateDF["Latitude"] >= 36.8) & (climateDF["Latitude"] <= 37.2)
constantLatDF = climateDF[latBool]

# Plotting elevation vs longitude
plotClimate("Longitude", "decimal degrees East",
            "Elevation", "m", constantLatDF)

# Plotting temperature vs longitude
plotClimate("Longitude", "decimal degrees East",
            "Tmax", "degrees C", constantLatDF)

# Plotting precipitation vs longitude
plotClimate("Longitude", "decimal degrees East",
            "Precip", "mm/yr", constantLatDF)
