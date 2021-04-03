"""bbquda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from rest_framework.authtoken import views

import bbqudasite as bsite

urlpatterns = [
    path('', include('bbqudasite.urls')),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('auth/', include('rest_authtoken.urls')),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^homepage/$', bsite.views.index, name='homepage'),
    url(r'^logout/$', bsite.views.logoutView, name='logout'),
    url(r'^register/$', bsite.views.register, name='register'),
    url(r'^upload_csv/$', bsite.views.upload_csv, name='upload_csv'),
    url(r'^upload_log/$', bsite.views.upload_log, name='upload_log'),
    url(r'^mission_admin/$', bsite.views.mission_admin, name='mission_admin'),
    url(r'^my_missions/$', bsite.views.my_missions, name='my_missions'),
    url(r'^download/(?P<pk>[\w-]+)/$', bsite.views.download, name='download'),
    url(r'^download_custom/(?P<pk>[\w-]+)/$', bsite.views.download_custom, name='download_custom'),
    url(r'^delete_mission/(?P<pk>\d+)/$', bsite.views.MissionDelete.as_view(), name='delete_mission'),
    url(r'^mission_stats/(?P<pk>[\w-]+)/$', bsite.views.mission_stats, name='mission_stats'),
    url(r'^map/(?P<pk>[\w-]+)/$', bsite.views.map, name='map'),
    url(r'^dashboard/$', bsite.views.dashboard, name='dashboard'),
    url(r'^map_custom/(?P<pk>[\w-]+)/$', bsite.views.map_custom, name='map_custom'),
    url(r'^trail_generator/$', bsite.views.trail_generator, name='trail_generator'),
    url(r'^custom_trails/$', bsite.views.custom_trails, name='custom_trails'),
    url(r'^delete_trail/(?P<pk>\d+)/$', bsite.views.TrailDelete.as_view(), name='delete_trail'),

]
