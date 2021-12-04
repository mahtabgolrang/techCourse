from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.main, name="main"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('workwithus/', views.workwithus, name="workwithus"),
    path('logout/', views.logoutUser, name="logout"),
    path('test/', views.test, name="test"),
    

]
