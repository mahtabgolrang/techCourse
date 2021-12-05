from django.contrib.messages.api import info
from django.forms.models import construct_instance
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from .models import *
from .forms import CreateUserForm, CreatTeacher
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users
import logging
from techCourse.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

# Create your views here.


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            messages.info(request, 'Account was created for')
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            customer = Customer.objects.create(user=user)
            customer.save()
            # subject = 'Welcome to techCourse'
            # message = f'''Hi {user.first_name}
            #         You are successfully registered with the user name {user.username}
            #         We are so happy that you have chosen us. Here you can learn with us and improve your skills.
            #         Hope you enjoy studying with us,
            #         The techCourse Team.'''
            # send_mail(subject, message, EMAIL_HOST_USER,
            #           [user.email], fail_silently=False)
            messages.success(request, 'Account was created for' + username)
            return redirect('main')

    return render(request, 'register.html', {'form': form})


logger = logging.getLogger(__name__)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        user1= authenticate(request, email=username, password=password)
        if user is not None or user1 is not None:
            login(request,user)
            return redirect('/')
        else: messages.info(request,'user name or password is incorrect...!')
    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def main(request):
    context = {

    }
    return render(request, 'main.html', context)


def workwithus(request):

    form = CreateUserForm()
    formTeacher = CreatTeacher()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        formTeacher = CreatTeacher(request.POST)
        if form.is_valid() and formTeacher.is_valid():
            messages.info(request, 'Account was created for')
            user = form.save()
            teacher = formTeacher.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='teacher')
            user.groups.add(group)
            teacher.user = user
            teacher.save()
            messages.success(request, 'Account was created for' + username)
            return redirect('main')
    context = {
        'form': form,
        'formTeacher': formTeacher
    }
    return render(request, 'workwithus.html', context)


def test(request):

    return render(request, 'test.html')


@login_required
@allowed_users("customer")
def userdashboard(request):
    customer = request.user.customer
    allCours = customer.course.all()
    freeCours =list(filter(lambda course :course.price==0 ,allCours))
    logger.error(f'\n\n\n\n  {allCours}  --------------\n\n\n\n')
    coursePurchased = list(filter(lambda course :course.price>0,customer.course.all()))
    context = {
        "customer": customer,
        'allCours': allCours,
        'freeCours': freeCours,
        'freeCoursSize': len(freeCours),
        'coursePurchased': coursePurchased,
        'coursePurchasedSize': len(coursePurchased),
    }
    return render(request, 'userdashboard.html', context)
