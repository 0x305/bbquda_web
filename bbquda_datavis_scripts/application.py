
from flask import Flask, flash, redirect, render_template, request,  session, abort,send_from_directory,send_file,jsonify
import pandas as pd
import json
 
#2. Declare application
app= Flask(__name__)
 
@app.route("/",methods=["GET","POST"])
#We are defining a home page function below. We will get the #CountryName and the Year from the form we defined in the html 
def homepage():
     return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
