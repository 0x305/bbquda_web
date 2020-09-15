from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import pandas as pd
import os
from users.forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
# Create your views here.

#Currently playing with the latitude paramter to make sure i can read a csv file properly
def index(request):
    mission_file = open('20190611_103011_greg_map_loc_surface_modified_IVER2-218.csv')
    df = pd.read_csv(mission_file)
    latitude = df['Latitude']
    print(latitude[0])
    context = {'latitude': latitude}
    #return HttpResponse(latitude)
    return render(request, 'index.html', context)

#function for removing outliers
def clean(csv_file):
    return

#useful for allowing files that have periods in the name before an extension
def getName(strArr):
    name = ''
    for i in range(0, len(strArr) - 2):
        name = name + i 
    return name

def formhtml(request):
    #user just landed for the first time so show them the upload html
    if request.method == "GET":
        return render(request, 'form.html')
    
    #in the html called the uploaded file 'file'
    csv_file = request.FILES['file']

    #if we need to get the name of the file for organization reasons
    csv_file_string = csv_file.name.split('.') #array of the title of the uploaded file
    csv_file_name = getName(csv_file_string)
    df = None #need to declare the dataframe varaible so i can load it in the if

    #need seperate statements because need to specify delimiter with log file
    if csv_file.name.endswith('.log'):
        df = pd.read_csv(csv_file, delimiter=';')
        filtered_list = df[['Latitude', 'Longitude', 'Total Water Column (m)',
            'Temperature (c)', 'pH', 'ODO mg/L', 'Salinity (ppt)',
            'Turbid+ NTU', 'BGA-PC cells/mL']]
        #print(filtered_list) #just a check
        latitude = filtered_list['Latitude']
        print(df)
        return HttpResponse(latitude[0])

    elif csv_file.name.endswith('.csv'):
        df = pd.read_csv(csv_file)
        filtered_list = df[['Latitude', 'Longitude', 'Total Water Column (m)',
            'Temperature (c)', 'pH', 'ODO mg/L', 'Salinity (ppt)',
            'Turbid+ NTU', 'BGA-PC cells/mL']]
        #print(filtered_list) #just a check
        latitude = filtered_list['Latitude']
        print(df)
        return HttpResponse(latitude[0])

    else:
        messages.error(request, 'Please provide a .log or .csv formatted file')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False) 
            profile.save()
            login(request, profile)
            next = request.POST.get('next', '/') #redirect to where user wanted to go

            return HttpResponseRedirect(next)           
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def logoutView(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
