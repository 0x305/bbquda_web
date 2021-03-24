from django.urls import path

from . import views
from rest_framework.authtoken import views as rest_views
app_name = "bbqudasite"

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.formhtml, name='formhtml'),
    path('getData/', views.get_data),
    path('api-token-auth/',rest_views.obtain_auth_token, name='api-token-auth')
]