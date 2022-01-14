from datetime import datetime
from urllib import response
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
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import FileResponse
from django.template.loader import get_template
from django.template import Context
import cgi

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
            subject = 'Welcome to techCourse'
            message = f'''Hi {user.first_name}
                    You are successfully registered with the user name {user.username}
                    We are so happy that you have chosen us. Here you can learn with us and improve your skills.
                    Hope you enjoy studying with us,
                    The techCourse Team.'''
            send_mail(subject, message, EMAIL_HOST_USER,
                      [user.email], fail_silently=False)
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

    return render(request,"payment.html")


@login_required
@allowed_users("customer")
def userdashboard(request):
    customer = request.user.customer

    allCours = customer.transaction.all()
    freeCours = allCours.filter(price=0)
    
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
    transaction = teacher.transaction.all()[0:3]
    #logger.error(f'\n\n\n\n  {allCours}  --------------\n\n\n\n')
    coursePurchased = allCours.filter(price__gt=0)
    context = {
        "teacher": teacher,
        "allCours": allCours,
        "freeCours": freeCours,
        "freeCoursSize": len(freeCours),
        "coursePurchased": coursePurchased,
        "coursePurchasedSize": coursePurchased.count(),
        "transaction":transaction,
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
    transaction = teaacher.transaction.all()

    context = {
        "teacher": teaacher,
        "allCours": allCours,
        "freeCours": freeCours,
        "freeCoursSize": len(freeCours),
        "coursePurchased": coursePurchased,
        "coursePurchasedSize": coursePurchased.count(),
        "transaction":transaction,
    }
    return render(request, 'teacherdashboard-transaction.html' , context)

def courseDetailsView(request,course_id):
    
    try:
        course=Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return render(request , "course_doesnt_exist.html" )

    if course.stutus == 'd':
        return render(request , "course_doesnt_published.html" )
    try:
        
        customer = request.user.customer

        tr = customer.transaction.all()
        cr =tr.filter(course__id__exact=course_id) 
        if len(cr)>0:
            userBuy= True
        else :
            userBuy=False
        context={
        "course":course,
        "userBuy":userBuy,
    } 
            
    except :
       context={
          "course":course
        }
    return render(request,"course.html",context)


def showAllCourse(request):
    
    courses = Course.objects.filter(stutus='p')
    # if request.method =="All":
    #     logger.error("\n\n\n\n\n\n /n/n/n all  /n/n/n \n\n\n\n\n")
    #     courses = Course.objects.filter(stutus='p')
       
    # if request.method == "soon" :
    #     courses = Course.objects.order_by("-date_created").filter(stutus='p')
    #     logger.error("\n\n\n\n\n\n /n/n/n kosss anant /n/n/n \n\n\n\n\n")

        
    # if request.method == "Post":
    #     courses = Course.objects.order_by("name").filter(stutus='p')
    #     logger.error("\n\n\n\n\n\n /n/n/n  name /n/n/n  \n\n\n\n\n")
        
    # if request.method == "post":
    #     courses = Course.objects.filter(stutus='p',price__exact=0)[:1]        
    #     logger.error("\n\n\n\n\n\n  fre  \n\n\n\n\n")
       
     
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


@login_required
@allowed_users("customer")
def payment(request,course_id):
    try:
        course=Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return render(request , "course_doesnt_exist.html" , status=404)
#course_doesnt_exist.html
    if course.stutus == 'd':
        return HttpResponseNotFound("<h1>course dose not published</h1>") 

    customer = request.user.customer

    if request.method=="POST":
        course=Course.objects.get(id=course_id)
        teacher = course.teacher.all()[0]
        transaction =Transaction(price = course.price)
        transaction.save()
        transaction.course.add(course)
        transaction.teacher.add(teacher)
        transaction.customer.add(customer)
            
        # from django.template.loader import render_to_string
        # from django.core.files.storage import FileSystemStorage
        # from weasyprint import HTML
   
        # html_string = render_to_string('customerReport.html', {'transaction': transaction})
        # html = HTML(string=html_string)
        # html.write_pdf(target="transaction/"+filename);
        # fs = FileSystemStorage('/transaction')
        # with fs.open(filename) as pdf:
        #     response = HttpResponse(pdf, content_type='application/pdf')
        #     response['Content-Disposition'] = 'attachment; filename="'+ filename +'"'
        #     transaction.pdf=pdf
        # response["Content-Disposition"]=filename
        # template_path="customerReport.html"
        # template=get_template(template_path)            
        # html=template.render(
        #    { "transaction":transaction}
        # )
        # pisa.CreatePDF(html,dest=response)
        
        # from io import BytesIO , StringIO

        # result =  StringIO()
        # templatee = open(filename,'w+b')

        # pdf=pisa.CreatePDF(html,dest=response)
        # logging.error(f"\n\n\n\n {type(pdf)}  \n\n\n\n")
        # templatee.close()
        # converted =result.getvalue()
        
        #pdf = pisa.pisaDocument(str(html), dest=result) 
        #logging.error(f"\n\n\n\n {type(pdf)}  \n\n\n\n")

        # transaction.pdf=response.write(converted)

        
        # template_name="customerReport.html"        
        from django.conf import settings
        # from django.views.generic.base import TemplateView
        # from wkhtmltopdf.views import PDFTemplateResponse
        # response = PDFTemplateResponse(
        #     request=request,
        #     template=template_name,
        #     filename=filename,
        #     context={"transaction":transaction},
        #     cmd_options={'load-error-handling': 'ignore'})
        
        import os 
        # path = os.path.join(settings.MEDIA_ROOT, 'transaction') 
        # mode = 0o666
        # os.makedirs(path,mode=mode , exist_ok = True) 
        # import subprocess
        # subprocess.call('dir', shell=True)
        # with open( path+"\\" + filename, "x") as f:
        #     f.write(response.rendered_content)
        #     transaction.pdf=f
        path = os.path.join(settings.MEDIA_ROOT, 'transaction')
        filename=path+"/transaction"+\
                customer.user.username+\
                    str(datetime.now()).replace(":","-")+".pdf"
        response=HttpResponse(content_type= 'apllication/pdf')
        response["content-Disposition"]="attachment;"+filename
        template_path="customerReport.html"
        template=get_template(template_path)            
        html=template.render(
           { "transaction":transaction}
        )
        

    #filename = 'acte_de_naissance_' + str(BirthCertificate.lastname)

        file = open(filename, "w+b")
        pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
        from django.core.files import File

        file.seek(0)
        pdf = file.read()
        transaction.pdf.save("transaction"+\
                customer.user.username+\
                    str(datetime.now()).replace(":","-"),File(file))
        file.close()

        #pisa.CreatePDF(html,des=response)
        transaction.save()

        course.dlNumber+=1
        teacher.wallet +=course.price * 0.8
        
        teacher.save()
        course.save()
        
        
        subject = 'buy course form  techCourse'
        message = f'''Thank you for your purchase
On behalf of techcourse, I would like to thank you for [buying/using/service {course.name} ]. We sincerely hope that you will continue to enjoy {course.name}
If you have any questions or if we can further assist you in any way, please feel free to contact me.
I hope to hear from you soon!
Thank you once again'''
        send_mail(subject, message, EMAIL_HOST_USER,
                      [customer.user.email], fail_silently=False)
       # return HttpResponse(f"<h1>thank you for buy course {course.name} your Tracking Code is {transaction.id}<h1>")
        return redirect('course', course_id=course.id)
        
        #return response

    

    context={
        "course":course,
    }    
    return render(request,"payment.html",context)


def courseDoesntExist(request):
    
    
    return render(request , "course_doesnt_exist.html" , status=404)
    
    
    