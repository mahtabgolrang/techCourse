from django.contrib.messages.api import info
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from .models import *
from .forms import  CreateUserForm 
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user
import logging
from techCourse.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

# Create your views here.
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form= CreateUserForm(request.POST)
        if form.is_valid():
             messages.info(request,'Account was created for')   
             user=form.save()
             username= form.cleaned_data.get('username')
             group = Group.objects.get(name='customer')
             user.groups.add(group)
             customer = Customer.objects.create(user=user)
             customer.save()
             subject = f'Hi {user.first_name}'
             message = f'tnx for register to techCourse your user name is {username}'
             send_mail(subject, message, EMAIL_HOST_USER,[user.email], fail_silently = False)
             messages.success(request,'Account was created for' + username)   
             return redirect('home')
    
    return render(request , 'register.html',{'form':form})
    
logger = logging.getLogger(__name__)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            subject = f'Hi {user.first_name}'
            message = 'Hope you are enjoying your Django Tutorials'
            send_mail(subject, 
            message, EMAIL_HOST_USER,[user.email], fail_silently = False)
            login(request,user)
        else:
            messages.info(request,'user name or password is incorrect...!')
    context = {}
    return render(request , 'login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def main(request):
    context={
        
    }
    return render(request ,'main.html',context)


def test(request):
   
    context={
    }
    return render(request , 'test.html', context)
