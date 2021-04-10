from django import forms 
from bbqudasite.models import CSVUpload, LogUpload, CustomTrail, HeatmapCSVSelection
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)

class CSVForm(forms.ModelForm): 
  
    class Meta: 
        model = CSVUpload 
        fields = ['name', 'file']

class LogForm(forms.ModelForm): 
    
    class Meta: 
        model = LogUpload  
        fields = ['name', 'file']
        
class TrailForm(forms.ModelForm): 
  
    class Meta: 
        model = CustomTrail 
        fields = ['name']

class HeatmapCSVForm(forms.ModelForm):
    filename = None

    class Meta:
        model = HeatmapCSVSelection
        fields = ['file', 'parameter']
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(HeatmapCSVForm, self).__init__(*args, **kwargs)
        self.fields['file'] = forms.ModelChoiceField(queryset=CSVUpload.objects.filter(user=self.request.user).values_list('file', flat=True).order_by('id'))


