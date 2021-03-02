from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view
from ..bbqudasite.models import CSVUpload
@api_view(["GET"])
def get_data(request):
    datasets = CSVUpload.objects.all()
    return JsonResponse(datasets)