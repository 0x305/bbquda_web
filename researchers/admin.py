from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.db import models
from .models import CustomUser
from bbqudasite.models import Coordinate, CSVUpload
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

admin.site.register(CustomUser, CustomUserAdmin)

class CoordinateAdmin(admin.ModelAdmin):
    model = Coordinate
admin.site.register(Coordinate, CoordinateAdmin)

class MissionAdmin(admin.ModelAdmin):
    model = CSVUpload
admin.site.register(CSVUpload, MissionAdmin)

