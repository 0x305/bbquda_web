from __future__ import unicode_literals
import csv
import os
import io
from django.db import models
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
from django.contrib.auth import get_user_model
import uuid
import datetime
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError





def upload_csv_file(instance, filename):
    qs = instance.__class__.objects.filter(user=instance.user)
    if qs.exists():
        num_ = qs.last().id + 1
    else:
        num_ = 1
    return f'csv/{num_}/{instance.user.username}/{filename}'

def csv_file_validator(value):
    filename, ext = os.path.splitext(value.name)
    if  str(ext) != '.csv':
         raise ValidationError("Must be a csv file")
    decoded_file = value.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    reader = csv.reader(io_string, delimiter=';', quotechar='|')
    
    return True

def log_file_validator(value):
    filename, ext = os.path.splitext(value.name)
    if  str(ext) != '.log':
         raise ValidationError("Must be a log file")
    
    return True
    
class CSVUpload(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,  null= True)
    file = models.FileField(upload_to= 'csv/', validators=[csv_file_validator])
    name = models.CharField("File Name", max_length=50, null=True)
    date = models.DateField(_("Date"), default=datetime.date.today)

    def __str__(self):
        return self.user.username

class LogUpload(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,  null= True)
    file = models.FileField(upload_to= 'log/', validators=[log_file_validator])
    name = models.CharField("File Name", max_length=50, null=True)
    date = models.DateField(_("Date"), default=datetime.date.today)

    def __str__(self):
        return self.user.username

class Coordinate(models.Model):
    csv_file = models.ForeignKey(CSVUpload, on_delete=models.CASCADE,  null= True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    water = models.FloatField()
    temp = models.FloatField()
    pH = models.FloatField()
    odo = models.FloatField()
    salinity = models.FloatField()
    turbid = models.FloatField()
    bga = models.FloatField()

class CustomTrail(models.Model):
    file = models.FileField(upload_to= 'custom_trails/')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,  null= True)
    date = models.DateField(_("Date"), default=datetime.date.today)
    name = models.CharField("File Name", max_length=50, null=True)


class HeatmapCSVSelection(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,  null= True)
    file = models.FileField(upload_to= 'csv/', validators=[csv_file_validator])
    name = models.CharField("File Name", max_length=50, null=True)
    date = models.DateField(_("Date"), default=datetime.date.today)

    PARAM_CHOICES = (
    ("Total Water Column (m)","Total Water Column (m)"),
    ("Temperature (c)","Temperature (c)"),
    ("pH", "pH"),
    ("ODO mg/L", "ODO mg/L"),
    ("Salinity (ppt)", "Salinity (ppt)"),
    ("Turbid%2B NTU", "Turbid+ NTU"),
    ("BGA-PC cells/mL", "BGA-PC cells/mL")
    )

    parameter = models.CharField(max_length=22, choices=PARAM_CHOICES)

    def __str__(self):
        return self.user.username
