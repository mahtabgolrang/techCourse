from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Tag (models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, null=True)
    category_pic = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Videos(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='video/%y')
    demo =models.BooleanField()
    def __str__(self):
        return self.title


class Course(models.Model):
    name = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=1000)
    price = models.FloatField(null=True)
    category = models.ManyToManyField(Category)
    description = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
   # demo_videos = models.ManyToManyField(Videos)
    course_videos = models.ManyToManyField(Videos)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Document(models.Model):
    title = models.CharField(max_length=1000)
    profile_pic = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title


class Customer (models.Model):
    #name = models.CharField(max_length=200, null=True)
    #familyName = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    #email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    user = models.OneToOneField(User, null=True,on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, blank=True)
    course = models.ManyToManyField(Course)

   

class Teacher (models.Model):
    #name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    #email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, blank=True)
    course = models.ManyToManyField(Course)
    documents = models.OneToOneField(Document, on_delete=models.CASCADE, null=True)
