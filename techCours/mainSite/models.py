from typing import Counter
from django.core.checks import messages
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# class Tag (models.Model):
#     name = models.CharField(max_length=200, null=True)

#     def __str__(self):
#         return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, null=True)
    category_pic = models.ImageField(upload_to='category/coverPictures/' ,null=True, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=1000)
    price = models.FloatField(default=0)
    category = models.ManyToManyField(Category, related_name='category')
    subTittel = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    datepublished = models.DateTimeField(null=True)
    stutuses = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )
    stutus = models.CharField(max_length=1, choices=stutuses, default='d')
    course_pic = models.ImageField(upload_to='courses/coverPictures/' ,null=True, blank=True)
    duration = models.DurationField(max_length=100, null=True)
    fileZip = models.FileField(
        upload_to='courses/zipFile/', null=True, blank=True)
    dlNumber = models.IntegerField(default=0)
   # demo_videos = models.ManyToManyField(Videos)
    video = models.FileField(
        upload_to='courses/video/%y', null=True, blank=True)

    class Meta:
        ordering = ["-dlNumber"]

    def __str__(self):
        return self.name


COUNTRYS = (
    ('ir', 'Iran'),
    ('us', 'Usa'),
    ('ca', 'Canada'),
    ('ch', 'China'),
    ('in', 'India'),
)


class Customer (models.Model):
    #name = models.CharField(max_length=200, null=True)
    #familyName = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, unique=True)
    #email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    contry = models.CharField(
        max_length=2, choices=COUNTRYS, blank=True, default='ir')
    adress = models.CharField(max_length=50, null=True)
    user = models.OneToOneField(
        User, null=True, on_delete=models.CASCADE, related_name='customer')
    profile_pic = models.ImageField(null=True, blank=True)
    #course = models.ManyToManyField(Course, related_name='course')

    def __str__(self):
        return self.user.username


class Teacher (models.Model):
    #name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, unique=True)
    #email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    user = models.OneToOneField(
        User, null=True, on_delete=models.CASCADE, related_name='teacher')
    profile_pic = models.ImageField(
        upload_to='teacher/profile/picture/', null=True, blank=True)
    course = models.ManyToManyField(Course, related_name='teacher')
    fildOfStudy = models.CharField(max_length=60, null=True)
    university = models.CharField(max_length=60, null=True)
    educations = (
        ('b', 'Bachelor'),
        ('bs', 'Bachelor Student'),
        ('m', 'Master'),
        ('ms', 'Master Student'),
        ('p', 'PHD'),
        ('ps', 'PHD Student'),
    )
    address=models.CharField(max_length=50, null=True)
    lastEducation = models.CharField(
        max_length=2, choices=educations, default='bs')
    documents = models.FileField(
        upload_to='teacher/documents/', null=True, blank=True)
    companiName1= models.CharField(max_length=50, null=True)
    jobSituation1= models.CharField(max_length=50, null=True)
    companiName2= models.CharField(max_length=50, null=True)
    jobSituation2= models.CharField(max_length=50, null=True)
    courseTitle1= models.CharField(max_length=50, null=True)
    courseTime1= models.CharField(max_length=50, null=True)
    courseTitle2= models.CharField(max_length=50, null=True)
    courseTime2= models.CharField(max_length=50, null=True)
    exteraInfo =models.CharField(max_length=200 , null=True)
    accepted =models.BooleanField(default=False)
    wallet=models.FloatField(default=0)

    def __str__(self):
        return self.user.username


class ContactUs(models.Model):
    name = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=50, null=True)
    subject = models.CharField(max_length=30, null=True)
    message = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return self.name + "   " + self.email

class Transaction(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    price =models.FloatField(default=0)
    course = models.ManyToManyField(Course, related_name='transaction')
    tacher = models.ManyToManyField(Teacher, related_name='transaction')
    customer= models.ManyToManyField(Customer, related_name='transaction')
    class Meta:
        ordering = ["-date_created"]
