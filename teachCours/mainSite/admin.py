from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Tag)
class adminTag(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Category)
class adminCategory(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Videos)
class adminVideos(admin.ModelAdmin):
    list_display = ['title','demo']


@admin.register(Course)
class adminCourse(admin.ModelAdmin):
    list_display = ['name','title','price','date_created']


@admin.register(Document)
class adminDocument(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Customer)
class adminCustomer(admin.ModelAdmin):
    list_display = ['name','familyName','user']


@admin.register(Teacher)
class adminTeacher(admin.ModelAdmin):
    list_display = ['name','familyName','user']
