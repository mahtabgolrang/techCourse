from django import forms
from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Customer


class CreateUserForm (UserCreationForm):
   class Meta:
        model=User
        fields=['first_name','email','username','password1']
        widgets = {
        'password': forms.PasswordInput(),
        }