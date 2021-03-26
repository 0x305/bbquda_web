from django.shortcuts import render

# Create your views here.
import pandas as pd
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .. bbqudasite.models import CSVUpload
