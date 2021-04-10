from django.urls import path

from . import views
from rest_framework.authtoken.views import obtain_auth_token
app_name = "bbqudasite"

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.formhtml, name='formhtml'),
    path('getData/', views.get_data, name='getData'),
    path('login', obtain_auth_token, name='login'),
]