from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.db import models
from .models import CustomResearcher
from bbqudasite.models import Coordinate, CSVUpload
from .forms import CustomResearcherCreationForm, CustomResearcherChangeForm


class CustomUserAdmin(UserAdmin):
    model = CustomResearcher
    add_form = CustomResearcherCreationForm
    form = CustomResearcherChangeForm

admin.site.register(CustomResearcher, CustomUserAdmin)

class CoordinateAdmin(admin.ModelAdmin):
    model = Coordinate
admin.site.register(Coordinate, CoordinateAdmin)

class MissionAdmin(admin.ModelAdmin):
    model = CSVUpload
admin.site.register(CSVUpload, MissionAdmin)

