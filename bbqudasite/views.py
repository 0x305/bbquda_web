from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import pandas as pd
import numpy as np
import os
from users.forms import RegistrationForm
from bbquda.forms import CSVForm, LogForm, TrailForm, HeatmapCSVForm
from .models import CSVUpload, LogUpload, Coordinate, CustomTrail, HeatmapCSVSelection
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.http import FileResponse
import csv
from rest_framework.decorators import api_view
from io import StringIO
from django.core.files.base import ContentFile
from django.core.files import File
from django.views.generic.edit import DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from data_visuals.kriging2D import *

# Create your views here.


def index(request):
    return render(request, 'homepage.html')

def contact(request):
    return render(request, 'contact.html')

#api page request 
def api_page(request):
    return render(request, 'developer_api.html')

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
        latitude = filtered_list['Latitude']
        return HttpResponse(latitude[0])

    elif csv_file.name.endswith('.csv'):
        df = pd.read_csv(csv_file)
        filtered_list = df[['Latitude', 'Longitude', 'Total Water Column (m)',
            'Temperature (c)', 'pH', 'ODO mg/L', 'Salinity (ppt)',
            'Turbid+ NTU', 'BGA-PC cells/mL']]
        #print(filtered_list) #just a check
        latitude = filtered_list['Latitude']
        return HttpResponse(latitude[0])

    else:
        messages.error(request, 'Please provide a .log or .csv formatted file')

def register(request):
    if request.user.is_authenticated:
        return redirect('my_missions')
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
        return redirect('login')

@login_required
def upload_csv(request):
    if request.user.is_authenticated:
        user = request.user

        if request.method =='POST':
            form = CSVForm(request.POST, request.FILES)
            if form.is_valid():
                csv = form.save(commit=False)
                csv.user = request.user
                csv.save()
                save_coordinate(csv)

                return redirect('my_missions')
        else:
            form = CSVForm()

        return render(request, 'upload_csv.html', {'form': form, 'user':user})
    return render(request, 'login.html')

@login_required
def upload_log(request):

    if request.user.is_authenticated:
        user = request.user

        if request.method =='POST':
            form = LogForm(request.POST, request.FILES)


            if form.is_valid():
                log = form.save(commit=False)
                log.user = request.user
                log.save()
                new_path = log.name + '.csv'
                with open(log.file.path, encoding="ISO-8859-1") as f, open(new_path, 'w') as f2:
                    writer = csv.writer(f2)

                    i = 0
                    for line in f:
                        writer.writerow([i] + line.rstrip().split(';'))
                        i += 1
                        if i == 10000:
                            break

                    new_csv = CSVUpload(user = request.user)
                    new_file = open(new_path)
                    new_csv.file = File(new_file)
                    new_csv.name = log.name
                    new_csv.save()
                    save_coordinate(new_csv)

                return redirect('my_missions')
        else:
            form = LogForm()

        return render(request, 'upload_log.html', {'form': form, 'user':user})
    return render(request, 'login.html')

def save_coordinate(input = CSVUpload):
    path = input.file.path
    df = pd.read_csv(path)
    for index, row in df.iloc[::50].iterrows():
        coordinate = Coordinate(csv_file = input)
        coordinate.longitude = row['Longitude']
        coordinate.latitude = row['Latitude']
        coordinate.water = row['Total Water Column (m)']
        coordinate.temp = row['Temperature (c)']
        coordinate.pH = row['pH']
        coordinate.odo = row['ODO mg/L']
        coordinate.salinity = row['Salinity (ppt)']
        coordinate.turbid = row['Turbid+ NTU']
        coordinate.bga = row['BGA-PC cells/mL']
        coordinate.save()


@staff_member_required
def mission_admin(request):
    missions = CSVUpload.objects.all()
    return render(request, 'mission_admin.html', {'missions': missions} )

@login_required
def my_missions(request):
    if request.user.is_authenticated:
        user = request.user
        missions = CSVUpload.objects.filter(user = user)

        return render(request, 'my_missions.html', { 'user': user,'missions': missions})
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def download(request, pk):
    mission = CSVUpload.objects.get(id=pk)
    filename = mission.file.path
    response = FileResponse(open(filename, 'rb'))
    return response

def download_custom(request, pk):
    trail = CustomTrail.objects.get(id=pk)
    filename = trail.file.path
    response = FileResponse(open(filename, 'rb'))
    return response

class MissionDelete(DeleteView):
    model = CSVUpload
    success_url = reverse_lazy('my_missions')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

@login_required
def logoutView(request):
    logout(request)
    return redirect('login')

def mission_stats(request, pk):
    mission = CSVUpload.objects.get(id=pk)
    path = mission.file.path
    df = pd.read_csv(path)
    water_count = df['Total Water Column (m)'].count()
    water_mean = df['Total Water Column (m)'].mean().round(2)
    water_std = df['Total Water Column (m)'].std().round(2)
    water_min = df['Total Water Column (m)'].min().round(2)
    water_max = df['Total Water Column (m)'].max().round(2)
    water_25 = df['Total Water Column (m)'].quantile(0.25).round(2)
    water_50 = df['Total Water Column (m)'].quantile(0.50).round(2)
    water_75 = df['Total Water Column (m)'].quantile(0.75).round(2)

    temp_count = df['Temperature (c)'].count()
    temp_mean = df['Temperature (c)'].mean().round(2)
    temp_std = df['Temperature (c)'].std().round(2)
    temp_min = df['Temperature (c)'].min().round(2)
    temp_max = df['Temperature (c)'].max().round(2)
    temp_25 = df['Temperature (c)'].quantile(0.25).round(2)
    temp_50 = df['Temperature (c)'].quantile(0.50).round(2)
    temp_75 = df['Temperature (c)'].quantile(0.75).round(2)

    pH_count = df['pH'].count()
    pH_mean = df['pH'].mean().round(2)
    pH_std = df['pH'].std().round(2)
    pH_min = df['pH'].min().round(2)
    pH_max = df['pH'].max().round(2)
    pH_25 = df['pH'].quantile(0.25).round(2)
    pH_50 = df['pH'].quantile(0.50).round(2)
    pH_75 = df['pH'].quantile(0.75).round(2)

    ODO_count = df['ODO mg/L'].count()
    ODO_mean = df['ODO mg/L'].mean().round(2)
    ODO_std = df['ODO mg/L'].std().round(2)
    ODO_min = df['ODO mg/L'].min().round(2)
    ODO_max = df['ODO mg/L'].max().round(2)
    ODO_25 = df['ODO mg/L'].quantile(0.25).round(2)
    ODO_50 = df['ODO mg/L'].quantile(0.50).round(2)
    ODO_75 = df['ODO mg/L'].quantile(0.75).round(2)

    salinity_count = df['Salinity (ppt)'].count().round(2)
    salinity_mean = df['Salinity (ppt)'].mean().round(2)
    salinity_std = df['Salinity (ppt)'].std().round(2)
    salinity_min = df['Salinity (ppt)'].min().round(2)
    salinity_max = df['Salinity (ppt)'].max().round(2)
    salinity_25 = df['Salinity (ppt)'].quantile(0.25).round(2)
    salinity_50 = df['Salinity (ppt)'].quantile(0.50).round(2)
    salinity_75 = df['Salinity (ppt)'].quantile(0.75).round(2)

    turbid_count = df['Turbid+ NTU'].count()
    turbid_mean = df['Turbid+ NTU'].mean().round(2)
    turbid_std = df['Turbid+ NTU'].std().round(2)
    turbid_min = df['Turbid+ NTU'].min().round(2)
    turbid_max = df['Turbid+ NTU'].max().round(2)
    turbid_25 = df['Turbid+ NTU'].quantile(0.25).round(2)
    turbid_50 = df['Turbid+ NTU'].quantile(0.50).round(2)
    turbid_75 = df['Turbid+ NTU'].quantile(0.75).round(2)

    BGA_count = df['BGA-PC cells/mL'].count()
    BGA_mean = df['BGA-PC cells/mL'].mean().round(2)
    BGA_std = df['BGA-PC cells/mL'].std().round(2)
    BGA_min = df['BGA-PC cells/mL'].min().round(2)
    BGA_max = df['BGA-PC cells/mL'].max().round(2)
    BGA_25 = df['BGA-PC cells/mL'].quantile(0.25).round(2)
    BGA_50 = df['BGA-PC cells/mL'].quantile(0.50).round(2)
    BGA_75 = df['BGA-PC cells/mL'].quantile(0.75).round(2)

    return render(request, 'mission_stats.html', {'mission': mission, 'water_count': water_count, 'water_mean': water_mean, 'water_std':water_std,
    'water_min':water_min, 'water_max':water_max, 'water_25':water_25, 'water_50':water_50, 'water_75':water_75, 'temp_count':temp_count,
    'temp_mean':temp_mean, 'temp_std':temp_std, 'temp_min':temp_min, 'temp_max':temp_max, 'temp_25':temp_25, 'temp_50':temp_50, 'temp_75':temp_75,
    'pH_count':pH_count, 'pH_mean':pH_mean, 'pH_std':pH_std, 'pH_min':pH_min, 'pH_max':pH_max, 'pH_25':pH_25, 'pH_50':pH_50, 'pH_75':pH_75,
    'ODO_count':ODO_count, 'ODO_mean':ODO_mean, 'ODO_std':ODO_std, 'ODO_min':ODO_min, 'ODO_max':ODO_max, 'ODO_25':ODO_25, 'ODO_50':ODO_50, 'ODO_75':ODO_75,
    'salinity_count':salinity_count, 'salinity_mean':salinity_mean, 'salinity_std':salinity_mean, 'salinity_std':salinity_std, 'salinity_min':salinity_min,
    'salinity_max':salinity_max, 'salinity_25':salinity_25, 'salinity_50':salinity_50, 'salinity_75':salinity_75, 'turbid_count':turbid_count,
    'turbid_mean':turbid_mean, 'turbid_std':turbid_std, 'turbid_min':turbid_min, 'turbid_max':turbid_max, 'turbid_25':turbid_25, 'turbid_50':turbid_50, 'turbid_75':turbid_75,
    'BGA_count':BGA_count, 'BGA_mean':BGA_mean, 'BGA_std':BGA_std, 'BGA_min':BGA_min, 'BGA_max':BGA_max, 'BGA_25':BGA_25, 'BGA_50':BGA_50, 'BGA_75':BGA_75} )

def map(request, pk):
    mission = CSVUpload.objects.get(id=pk)
    coordinates = Coordinate.objects.filter(csv_file = mission)

    return render(request, 'map.html', {'mission':mission, 'coordinates':coordinates})

def map_custom(request, pk):
    trail = CustomTrail.objects.get(id = pk)
    trail_path = trail.file.path
    print(trail_path)
    df = pd.read_csv(trail_path)
    lats =[]
    lons =[]
    for index, row in df.iterrows():
        lons.append(row['Longitude'])
        lats.append(row['Latitude'])

    return render(request, 'map_custom.html', {'lats':lats, 'lons':lons, 'trail':trail})

def kriging_heatmap(request):
    #mission = CSVUpload.objects.get(id=pk)
    #path = mission.file.path

    file =  request.GET.get("file", None)
    parameter = request.GET.get('parameter', None)
    lat1 = request.GET.get('max_lat', None)
    lng1 = request.GET.get('min_long', None)
    lat2 = request.GET.get('min_lat', None)
    lng2 = request.GET.get('max_long', None)

    form = HeatmapCSVForm(request.POST, request=request, initial={'file': file,'id_parameter': parameter })

    if file:

        path = "media/" + file
        filtered_data = selectParameterToKrige(path, parameter) #Using 'pH' until I can properly choose which parameter

        min_lat = filtered_data['Latitude'].min() #Defaults for now
        max_lat = filtered_data['Latitude'].max()
        min_lon = filtered_data['Longitude'].min()
        max_lon = filtered_data['Longitude'].max()

        if lat1 and lat2 and lng1 and lng2:

            fil_region_data = filterForKrigingRegion(filtered_data, min_lat, max_lat, min_lon, max_lon)

            gridx, gridy = createXYGrid(float(lat2), float(lat1), float(lng1), float(lng2))

            lat, lon, param = convertDFtoNP(fil_region_data, parameter)

            OK = createKrigingObject(lat, lon, param)
            z,ss = executeKrigging(OK, gridx, gridy)

            formatted_heatmap = formatInterpolatedData(z, gridx, gridy)

            return render(request, 'kriging_heatmap.html', {'heatmap_vals': formatted_heatmap, 'max_lat': max_lat, 'max_long': max_lon, 'min_lat': min_lat, 'min_long': min_lon, 'zoom': 15, 'form':form})
        return render(request, 'kriging_heatmap.html', {'heatmap_vals': [], 'max_lat': max_lat, 'max_long': max_lon, 'min_lat': min_lat, 'min_long': min_lon, 'zoom': 15, 'form':form})
    return render(request, 'kriging_heatmap.html', {'heatmap_vals': [], 'lat': 0, 'long': 0, 'zoom': 7, 'form':form})

@csrf_exempt
def trail_generator(request):
    user = request.user

    if request.method == 'POST':
        form = TrailForm(request.POST)
        data =  request.POST.getlist('list[]')

        trail = CustomTrail(name ="Custom_Trail")
        trail.user = request.user

        new_path = trail.name + '.csv'
        lat = []
        lon =[]

        index = 0
        for line in data:
            cur = index % 2
            index += 1
            if cur == 0:
                #txt_file.write(" ".join(line) + ", ")
                lat.append(line)

            else:
                #txt_file.write(" ".join(line) + "\n")
                lon.append(line)
        with open(new_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Latitude', 'Longitude'])
            writer.writerows(zip(lat, lon))

        new_file = open(new_path)
        trail.file = File(new_file)
        trail.save()
        return redirect('custom_trails')



    return render(request, 'trail_generator.html')

@login_required
def custom_trails(request):
    if request.user.is_authenticated:
        user = request.user
        trails = CustomTrail.objects.filter(user = user)

        return render(request, 'custom_trails.html', { 'user': user,'trails': trails})
    return redirect('login')

class TrailDelete(DeleteView):
    model = CustomTrail
    success_url = reverse_lazy('custom_trails')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

#get request for csv data
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_data(request, pk):
    #get a list of all csv files and store its contents
    csvs = {}
    datasets = CSVUpload.objects.all()

    for data in datasets:
        #media directory
        media_dir = os.path.join(os.path.dirname(__file__), "..", "media")
        #store csv contents into dataframe
        df = pd.read_csv(os.path.join(media_dir, str(data)))
        #append dataframe into list
        csvs[str(data)] = df.to_json()
    
    return JsonResponse(csvs)


