from django.urls import path

from . import views

app_name = "bbqudasite"

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.formhtml, name='formhtml'),
    path('getData/', views.get_data)
]