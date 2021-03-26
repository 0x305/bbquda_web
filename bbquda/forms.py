from django import forms
from bbqudasite.models import CSVUpload, LogUpload, CustomTrail

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
