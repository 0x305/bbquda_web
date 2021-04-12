from bbqudasite.models import Coordinate, CSVUpload
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

admin.site.site_header = "Administrative Portal"


class CustomUserAdmin(UserAdmin):
    list_display = ('date_joined', 'email', 'first_name', 'last_name', 'is_active', 'is_staff',
                    'is_superuser', 'last_login', 'username', 'password')

    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm


class CoordinateAdmin(admin.ModelAdmin):
    model = Coordinate


admin.site.register(Coordinate, CoordinateAdmin)


class MissionAdmin(admin.ModelAdmin):
    model = CSVUpload


admin.site.register(CSVUpload, MissionAdmin)
