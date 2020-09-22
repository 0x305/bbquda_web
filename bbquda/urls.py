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
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', views.logoutView, name = 'logout'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^upload_csv/$', views.upload_csv, name ='upload_csv'),
    url(r'^mission_admin/$', views.mission_admin, name = 'mission_admin'),
    url(r'^my_missions/$', views.my_missions, name ='my_missions'),
    url(r'^download/(?P<pk>[\w-]+)/$', views.download, name ='download'),
    url(r'^test/$', views.test, name ='test'),
    
    




]
