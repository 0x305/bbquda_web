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
    
class CSVUpload(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,  null= True)
    file = models.FileField(upload_to=upload_csv_file, validators=[csv_file_validator])
    name = models.CharField("File Name", max_length=50, null=True)
    date = models.DateField(_("Date"), default=datetime.date.today)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.user.username