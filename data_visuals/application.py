
#%%
from flask import Flask, flash, redirect, render_template, request,  session, abort,send_from_directory,send_file,jsonify
import pandas as pd
import json
from kriging2D import *

#%%
#2. Declare application
app= Flask(__name__)
 
@app.route("/main",methods=["GET","POST"])
#We are defining a home page function below. We will get the #CountryName and the Year from the form we defined in the html 
def homepage():
     return render_template("index.html")

@app.route("/main/get-heatmap", methods=["GET"])
def get_heatmap_default(csv = "C:/Users/aerod/Desktop/CapstoneII/bbquda_web/mission.csv", parameter ="pH"):
     filtered_data = selectParameterToKrige(csv, parameter)
    
     min_lat = filtered_data['Latitude'].min()
     max_lat = filtered_data['Latitude'].max()
     min_lon = filtered_data['Longitude'].min()
     max_lon = filtered_data['Longitude'].max()
     
     fil_region_data = filterForKrigingRegion(filtered_data, min_lat, max_lat, min_lon, max_lon)

     gridx, gridy = createXYGrid(min_lat, max_lat, min_lon, max_lon)
     
     lat, lon, pH = convertDFtoNP(fil_region_data, parameter)

     OK = createKrigingObject(lat, lon, pH)
     z,ss = executeKrigging(OK, gridx, gridy)

     formatted_heatmap = formatInterpolatedData(z, gridx, gridy)

     return jsonify(formatted_heatmap)


if __name__ == "__main__":
    app.run(debug=True)
