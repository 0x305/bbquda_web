from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Researcher
from django.utils.translation import gettext_lazy as _

class ResearcherCreationForm(UserCreationForm):

    class Meta:
        model = Researcher
        fields = ( 'email',)

class ResearcherChangeForm(UserChangeForm):

    class Meta:
        model = Researcher
        fields = UserChangeForm.Meta.fields

class RegistrationForm(UserCreationForm):
    
    email = forms.EmailField(max_length=254, help_text='Add a valid email address.', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField( max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'placeholder': 'Retype Password'}))

    class Meta:
        model = Researcher
        fields = ( 'first_name','last_name','email',  'username', 'password1', 'password2', )
        help_texts = {
            'first_name': _('First Name'),
        }