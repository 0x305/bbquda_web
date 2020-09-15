from django import forms 
from bbqudasite.models import CSVUpload
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)

class CSVForm(forms.ModelForm): 
  
    class Meta: 
        model = CSVUpload 
        
        fields = ['name', 'file']