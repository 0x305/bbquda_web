#%%
import numpy as np
import pykrige.kriging_tools as kt
from pykrige.ok import OrdinaryKriging
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
#%%
water_parameters = {0 : "Latitude",
                    1 : "Longitude",
                    2 : "Time hh:mm:ss",
                    3 : "Total Water Column (m)",
                    4 : "Temperature (c)",
                    5 : "pH",
                    6 : "ODO mg/L",
                    7 : "Salinity (ppt)",
                    8 : "Turbid+ NTU",
                    9 : "BGA-PC cells/mL"}

def selectParameterToKrige(csv_data, parameter):
    all_data = pd.read_csv(csv_data)

    try:
        filtered_data = all_data[["Latitude", "Longitude", parameter]]
        print("Parameter Selected")
    except ValueError:
        print("Invalid parameter chosen, please try again...")

    return filtered_data

#%%
def filterForKrigingRegion(df, min_lat, max_lat, min_lon, max_lon):
    return df[df['Latitude'].between(min_lat, max_lat, inclusive=True) & df['Longitude'].between(min_lon, max_lon, inclusive=True)]

def createXYGrid(min_lat, max_lat, min_lon, max_lon, lat_step_size=6/364000, lon_step_size=6/288200):
    # We are assuming interpolation along 6ft steps. The lat_step_size and lon_step_size are the default 
    # conversion from 6ft to the respective degree values.
    gridx = np.arange(min_lon, max_lon, lon_step_size)
    gridy = np.arange(min_lat, max_lat, lat_step_size)
    print(gridx)
    return gridx, gridy

def convertDFtoNP(df, parameter):
    lat = np.array(df['Latitude'].values.tolist())
    lon = np.array(df['Longitude'].values.tolist())
    parameter = np.array(df[parameter].values.tolist())
    return lat, lon, parameter

def createKrigingObject(lat, lon, parameter, var_model="linear"):
    krigged_data = OrdinaryKriging(
            lon,
            lat,
            parameter,
            variogram_model=var_model,
            verbose=False,
            enable_plotting=False,
        )
    return krigged_data

def executeKrigging(krigged_data, gridx, gridy):
    z, ss = krigged_data.execute('grid', gridx, gridy)
    return z, ss

def formatInterpolatedData(z, gridx, gridy):
    # Leaflet Heatmap takes data in the form of [[Lat, Lon, Val], ...]
    # gridy is lat, gridx is lon, z is val
    formatted_heatmap = []
    scaler = MinMaxScaler()
    scaler.fit(z)
    z = scaler.transform(z)
    #print(z)
    for i in range(len(gridx)):
        for j in range(len(gridy)):
            formatted_heatmap.append([gridy[j], gridx[i], z[j][i]])
    return formatted_heatmap

#%%
