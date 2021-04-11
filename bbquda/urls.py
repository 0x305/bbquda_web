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
from django.contrib import admin
from django.urls import path, include, reverse, reverse_lazy
from django.conf.urls import url
from bbqudasite import views
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView


urlpatterns = [
    path('', include('bbqudasite.urls')),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path(r'^api_page/$', views.api_page, name="api_page"),
    url(r'^homepage/$', views.index, name = 'homepage'),
    url(r'^about/$', views.about, name = 'about'),
    url(r'^bbqudasite_api/(?P<pk>[\w-]+)/$', views.get_data, name='get_data'),
    url(r'^contact/$', views.contact, name = 'contact'),
    url(r'^homepage/$', views.index, name = 'homepage'),
    url(r'^logout/$', views.logoutView, name = 'logout'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^upload_csv/$', views.upload_csv, name ='upload_csv'),
    url(r'^upload_log/$', views.upload_log, name ='upload_log'),
    url(r'^mission_admin/$', views.mission_admin, name = 'mission_admin'),
    url(r'^my_missions/$', views.my_missions, name ='my_missions'),
    url(r'^download/(?P<pk>[\w-]+)/$', views.download, name ='download'),
    url(r'^download_custom/(?P<pk>[\w-]+)/$', views.download_custom, name ='download_custom'),
    url(r'^delete_mission/(?P<pk>\d+)/$', views.MissionDelete.as_view(), name='delete_mission'),
    url(r'^mission_stats/(?P<pk>[\w-]+)/$', views.mission_stats, name ='mission_stats'),
    url(r'^map/(?P<pk>[\w-]+)/$', views.map, name = 'map'),
    url(r'^dashboard/$', views.dashboard, name ='dashboard'),
    url(r'^map_custom/(?P<pk>[\w-]+)/$', views.map_custom, name = 'map_custom'),
    url(r'^trail_generator/$', views.trail_generator, name = 'trail_generator'),
    url(r'^custom_trails/$', views.custom_trails, name ='custom_trails'),
    url(r'^delete_trail/(?P<pk>\d+)/$', views.TrailDelete.as_view(), name='delete_trail'),
    url(r'^kriging_heatmap/$', views.kriging_heatmap, name='kriging_heatmap'),

]
