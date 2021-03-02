from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.db import models
from .models import Researcher
from bbqudasite.models import Coordinate, CSVUpload
from .forms import ResearcherCreationForm, ResearcherChangeForm


class ResearcherAdmin(UserAdmin):
    model = Researcher
    add_form = ResearcherCreationForm
    form = ResearcherChangeForm

admin.site.register(Researcher, ResearcherAdmin)

class CoordinateAdmin(admin.ModelAdmin):
    model = Coordinate
admin.site.register(Coordinate, CoordinateAdmin)

class MissionAdmin(admin.ModelAdmin):
    model = CSVUpload
admin.site.register(CSVUpload, MissionAdmin)

