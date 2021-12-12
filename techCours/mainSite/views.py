from django.contrib.messages.api import info
from django.core import paginator
from django.forms.models import construct_instance
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator ,PageNotAnInteger , EmptyPage
# Create your views here.
from .models import *
from .forms import CreateUserForm, CreatTeacherForm, EditCustomerForm, UserEditForm, CreatContactUsForm, EditTeacherForm , EditTeacherResume,AddCourseForm
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
from django.http import HttpResponse, HttpResponseNotFound

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
        #logger.error(f'\n\n\n\n\n {username}  {password}   -------------------------------------\n\n\n\n\n')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'user name or password is incorrect...!')
    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def main(request):
    course = Course.objects.filter(stutus='p')
    showSomeCourse = course[:4]
    courseNumber = course.count()
    category = Category.objects.all()
    showCategory = category[:5]
    customerNumber = Customer.objects.all().count()
    teacherNumber = Teacher.objects.all().count()
    form = CreatContactUsForm()
    if request.method == 'POST':
        form = CreatContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'your message send to us')

            
    context = {
        "showSomeCourse": showSomeCourse,
        "showCategory": showCategory,
        "customerNumber": customerNumber,
        "teacherNumber": teacherNumber,
        "courseNumber": courseNumber,
        "form": form,
    }
    return render(request, 'main.html', context)


def workwithus(request):

    form = CreateUserForm()
    formTeacher = CreatTeacherForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        formTeacher = CreatTeacherForm(request.POST)
        
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

    return render(request,"course.html")


@login_required
@allowed_users("customer")
def userdashboard(request):
    customer = request.user.customer
    allCours = customer.course.all()
    freeCours = allCours.filter(price=0)
    #logger.error(f'\n\n\n\n  {allCours}  --------------\n\n\n\n')
    coursePurchased = allCours.filter(price__gt=0)
    context = {
        "customer": customer,
        "allCours": allCours,
        "freeCours": freeCours,
        "freeCoursSize": len(freeCours),
        "coursePurchased": coursePurchased,
        "coursePurchasedSize": coursePurchased.count(),
    }
    return render(request, 'userdashboard.html', context)


@login_required
@allowed_users("customer")
def userDashboardProfile(request):
    customer = request.user.customer

    if request.method == 'POST':
        formCustomer = EditCustomerForm(
            request.POST, instance=request.user.customer)
        formUser = UserEditForm(request.POST , request.FILES, instance=request.user)
        if formCustomer.is_valid() and formUser.is_valid():
            formCustomer.save()
            formUser.save()

            messages.success(
                request, 'your profile hase change  ' + request.user.username)
            return redirect("/")
    else:
        formCustomer = EditCustomerForm(instance=request.user.customer)
        formUser = UserEditForm(instance=request.user)

    context = {
        "customer": customer,
        "formCustomer": formCustomer,
        "form": formUser
    }

    return render(request, 'userdashboard-profile.html', context)

@login_required
@allowed_users("teacher")
def teacherDashboard(request):
    teacher =request.user.teacher
    allCours = teacher.course.all()
    freeCours = allCours.filter(price=0)
    #logger.error(f'\n\n\n\n  {allCours}  --------------\n\n\n\n')
    coursePurchased = allCours.filter(price__gt=0)
    context = {
        "teacher": teacher,
        "allCours": allCours,
        "freeCours": freeCours,
        "freeCoursSize": len(freeCours),
        "coursePurchased": coursePurchased,
        "coursePurchasedSize": coursePurchased.count(),
    }
    return render(request, 'teacherdashboard.html' , context)

@login_required
@allowed_users("teacher")
def TeacherDashboardProfile(request):
    teacher = request.user.teacher
    if request.method == 'POST':
        formTeacher = EditTeacherForm(request.POST , request.FILES, instance=request.user.teacher)
        formUser = UserEditForm(request.POST, instance=request.user)
        if formTeacher.is_valid() and formUser.is_valid():
            

            formTeacher.save()
            formUser.save()
            
            messages.success(
                request, 'your profile hase change  ' + request.user.username)
        else: 
            messages.error(request , 'somthing worng')   
     
    else:
        formTeacher = EditTeacherForm(instance=request.user.teacher)
        formUser = UserEditForm(instance=request.user)

    context = {
        "teacher": teacher,
        "formTeacher": formTeacher,
        "form": formUser
    }
    return render(request, 'teacherdashboard-profile.html', context)

@login_required
@allowed_users("teacher")
def teacherDashboardCreateCourse(request):
    teacher = request.user.teacher
    
    if  not teacher.accepted :
        return HttpResponseNotFound("<h1>you haven't access for creat a new  course </h1>")
    
    if request.method=="POST":
        addCourse =AddCourseForm( request.POST , request.FILES)
        if addCourse.is_valid():
            course =addCourse.save()
            teacher.course.add(course)
            
    else:
        addCourse =AddCourseForm()

    context ={
        "teacher":teacher,
        "addCourse":addCourse
    }
    return render(request, 'teacherdashboard-createcourse.html', context)

@login_required
@allowed_users("teacher")
def teacherDashboardResume(request):
    teacher = request.user.teacher

    if request.method=="POST":
        editeTeacher =EditTeacherResume( request.POST , request.FILES, instance=request.user.teacher)
        if editeTeacher.is_valid():
            editeTeacher.save()
    else:
        editeTeacher=EditTeacherResume(instance=request.user.teacher)

    context={
        "teacher":teacher,

        "editeTeacher":editeTeacher,
        
    }
    return render(request, 'teacherdashboard-resume.html' , context)

@login_required
@allowed_users("teacher")
def teacherDashboardTransaction(request):
    teaacher =request.user.teacher
    allCours = teaacher.course.all()
    freeCours = allCours.filter(price=0)
    #logger.error(f'\n\n\n\n  {allCours}  --------------\n\n\n\n')
    coursePurchased = allCours.filter(price__gt=0)
    context = {
        "teacher": teaacher,
        "allCours": allCours,
        "freeCours": freeCours,
        "freeCoursSize": len(freeCours),
        "coursePurchased": coursePurchased,
        "coursePurchasedSize": coursePurchased.count(),
    }
    return render(request, 'teacherdashboard-transaction.html' , context)

def courseDetailsView(request,course_id):
    
    try:
        course=Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return HttpResponseNotFound("<h1>course dose not exist</h1>")
        
    context={
        "course":course
    }

    return render(request,"course.html",context)


def showAllCourse(request):
    courses = Course.objects.filter(stutus='p')

    paginator = Paginator(courses ,10)
    page = request.GET.get("page" ,1)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1) 
    except EmptyPage:
        result = paginator.page(paginator.num_pages)   

    context={
        "result":result
    }
    return render(request ,"all-course.html" ,context )        