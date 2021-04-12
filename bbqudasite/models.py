from __future__ import unicode_literals

import csv
import datetime
import io
import os

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _


def upload_csv_file(instance, filename):
    qs = instance.__class__.objects.filter(user=instance.user)
    if qs.exists():
        num_ = qs.last().id + 1
    else:
        num_ = 1
    return f'csv/{num_}/{instance.user.username}/{filename}'


def csv_file_validator(value):
    filename, ext = os.path.splitext(value.name)
    if str(ext) != '.csv':
        raise ValidationError("Must be a csv file")
    decoded_file = value.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    reader = csv.reader(io_string, delimiter=';', quotechar='|')

    return True


def log_file_validator(value):
    filename, ext = os.path.splitext(value.name)
    if str(ext) != '.log':
        raise ValidationError("Must be a log file")

    return True


class CSVUpload(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)  # username
    name = models.CharField("File Name", max_length=50, null=True)
    file = models.FileField(upload_to="csv/", validators=[csv_file_validator])
    date = models.DateField(_("Date"), default=datetime.date.today)

    # helper to get file name
    def filename(self):
        return os.path.basename(self.file.name)

    # returns the file location of each csv
    def __str__(self):
        return self.file.name


class LogUpload(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='log/', validators=[log_file_validator])
    name = models.CharField("File Name", max_length=50, null=True)
    date = models.DateField(_("Date"), default=datetime.date.today)

    def __str__(self):
        return self.user.username


class Coordinate(models.Model):
    csv_file = models.ForeignKey(CSVUpload, on_delete=models.CASCADE, null=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    water = models.FloatField()
    temp = models.FloatField()
    pH = models.FloatField()
    odo = models.FloatField()
    salinity = models.FloatField()
    turbid = models.FloatField()
    bga = models.FloatField()

    def __str__(self):
        return str(set(self.csv_file.name))


class CustomTrail(models.Model):
    file = models.FileField(upload_to='custom_trails/')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    date = models.DateField(_("Date"), default=datetime.date.today)
    name = models.CharField("File Name", max_length=50, null=True)

    def __str__(self):
        return self.user


class HeatmapCSVSelection(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='csv/', validators=[csv_file_validator])
    name = models.CharField("File Name", max_length=50, null=True)
    date = models.DateField(_("Date"), default=datetime.date.today)

    PARAM_CHOICES = (
        ("Total Water Column (m)", "Total Water Column (m)"),
        ("Temperature (c)", "Temperature (c)"),
        ("pH", "pH"),
        ("ODO mg/L", "ODO mg/L"),
        ("Salinity (ppt)", "Salinity (ppt)"),
        ("Turbid%2B NTU", "Turbid+ NTU"),
        ("BGA-PC cells/mL", "BGA-PC cells/mL")
    )

    parameter = models.CharField(max_length=22, choices=PARAM_CHOICES)

    def __str__(self):
        return self.user.username


class Cleanup(models.Model):
    help = 'Delete objects older than 5 years'

    def handle(self, *args, **options):
        LogUpload.objects.filter(posting_date__lte=datetime.now() - timedelta(weeks > 261)).delete()
        self.stdout.write('Deleted objects older than 5 years')
