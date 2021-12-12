from django import forms
from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Category, Course, Customer, Teacher, ContactUs


class CreateUserForm (UserCreationForm):
    email = forms.EmailField(
        max_length=50, help_text='use a valid email', required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'username', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'Email {email}  is already in use')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f'Username {username}  is already in use')


class UserEditForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ["first_name", "last_name", "email", "username"]
    password = None

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            user = User.objects.get(email=email).exclude(pk=request.user.id)
        except Exception as e:
            return email
        raise forms.ValidationError(f'Email {email}  is already in use')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        try:
            user = User.objects.get(
                username=username).exclude(pk=request.user.id)
        except Exception as e:
            return username
        raise forms.ValidationError(f'Username {username}  is already in use')


COUNTRYS = (
    ('ir', 'Iran'),
    ('us', 'Usa'),
    ('ca', 'Canada'),
    ('ch', 'China'),
    ('in', 'India'),
)


class EditCustomerForm(forms.ModelForm):
    adress = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-line', 'rows': 3}))
    contry = forms.ChoiceField(
        widget=forms.Select,
        choices=COUNTRYS,
    )
    contry.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Customer
        fields = ['phone', 'contry', 'adress','profile_pic']

    def clean_phone(self):
        phone = self.cleaned_data['phone'].lower()
        try:
            user = Teacher.objects.get(phone=phone).exclude(
                pk=request.user.teacher.id)
        except Exception as e:
            return phone
        raise forms.ValidationError(f'phone {phone}  is already in use')

educations = (
        ('b', 'Bachelor'),
        ('bs', 'Bachelor Student'),
        ('m', 'Master'),
        ('ms', 'Master Student'),
        ('p', 'PHD'),
        ('ps', 'PHD Student'),
    )
class CreatTeacherForm(forms.ModelForm):
    lastEducation = forms.ChoiceField(
        widget=forms.Select,
        choices=educations,
    )
    lastEducation.widget.attrs['class'] = ' btn btn-secondary dropdown-toggle w-100'

    class Meta:
        model = Teacher
        fields = ['phone', 'fildOfStudy', 'university', 'lastEducation']

    def clean_phone(self):
        phone = self.cleaned_data['phone'].lower()
        try:
            user = Teacher.objects.get(phone=phone)
        except Exception as e:
            return phone
        raise forms.ValidationError(f'phone {phone}  is already in use')



class EditTeacherForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-line', 'rows': 3}))
    contry = forms.ChoiceField(
        widget=forms.Select,
        choices=COUNTRYS,
    )
    contry.widget.attrs['class'] = 'form-control'
    lastEducation = forms.ChoiceField(
        widget=forms.Select,
        choices=educations,
    )
    lastEducation.widget.attrs['class'] = ' btn btn-secondary dropdown-toggle w-100'
    class Meta:
        model = Teacher
        fields = ['phone','fildOfStudy','university','lastEducation', 'contry', 'address', 'profile_pic']

    def clean_phone(self):
        phone = self.cleaned_data['phone'].lower()
        try:
            user = Teacher.objects.get(phone=phone).exclude(
                pk=request.user.teacher.id)
        except Exception as e:
            return phone
        raise forms.ValidationError(f'phone {phone}  is already in use')

class CreatContactUsForm(forms.ModelForm):
    name = forms.CharField(max_length=30 ,required=True)
    email =forms.EmailField(max_length=50 , required=True)
    subject = forms.CharField(max_length=30 , required=True)
    message = forms.CharField( max_length=200,widget=forms.TextInput(
        attrs={"rows":3, "cols":10}) , required=True)
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'subject', 'message']
        widgets= { 'message': forms.Textarea(attrs={"rows":3, "cols":10}),}

class EditTeacherResume(forms.ModelForm):
    exteraInfo = forms.CharField( max_length=200,widget=forms.TextInput(
        attrs={"rows":3, "cols":10 , 'class' :'form-control form-control-line'}) , required=True)
    class Meta:
        model = Teacher
        fields = ['companiName1','jobSituation1','companiName2','jobSituation2',
         'courseTitle1', 'courseTime1','courseTitle2','courseTime2','documents','exteraInfo']

class AddCourseForm(forms.ModelForm):
    duration =forms.DurationField()
    
    category=forms.ChoiceField(
        widget=forms.Select,
        choices=[(categury.pk, categury) for categury in Category.objects.all()],
        required=True,
    )
    category.widget.attrs['class'] = 'form-select shadow-none form-control-line'
    subTittel =forms.CharField( max_length=200,widget=forms.TextInput(
        attrs={"rows":3, "cols":10}) , required=True)
    class Meta:
        model = Course
        fields =['name' ,'title','subTittel','category','price','duration','course_pic','fileZip', 'video'] 
