from django.contrib import admin
from .models import *

# Register your models here.




@admin.register(Category)
class adminCategory(admin.ModelAdmin):
    list_display = ['name']




@admin.register(Course)
class adminCourse(admin.ModelAdmin):
    list_display = ['name','title','price','date_created']


@admin.register(Customer)
class adminCustomer(admin.ModelAdmin):
    list_display = ['user',]


@admin.register(Teacher)
class adminTeacher(admin.ModelAdmin):
    list_display = ['user',]

@admin.register(ContactUs)
class adminCustomer(admin.ModelAdmin):
    list_display = ['name', 'email' , 'subject']
