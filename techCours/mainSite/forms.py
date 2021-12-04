from django import forms
from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Customer ,Teacher


class CreateUserForm (UserCreationForm):
   email= forms.EmailField(max_length=50 , help_text='use a valid email', required=True)
   agree = forms.BooleanField(required=True)
   
   class Meta:
      model = User
      fields = ['first_name','last_name', 'email', 'username', 'password1','password2', 'agree']

   def clean_email(self):
      email = self.cleaned_data['email'].lower()
      try:
         user= User.objects.get(email=email)
      except Exception as e :
         return email
      raise forms.ValidationError(f'Email {email}  is already in use' )

   def clean_username(self):
      username = self.cleaned_data['username'].lower()
      try:
         user= User.objects.get(username=username)
      except Exception as e:
         return username
      raise forms.ValidationError(f'Username {username}  is already in use' )

class CreatTeacher(forms.ModelForm):
   class Meta:
      model=Teacher
      fields=['phone','fildOfStudy','university','lastEducation']      
   def clean_phone(self):
      phone = self.cleaned_data['phone'].lower()
      try:
         user= Teacher.objects.get(phone=phone)
      except Exception as e:
         return phone
      raise forms.ValidationError(f'phone {phone}  is already in use' )


