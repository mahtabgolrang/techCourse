from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.main, name="main"),
    path('accounts/login/', views.loginPage, name="login"),
    path('accounts/register/', views.registerPage, name="register"),
    path('accounts/workwithus/', views.workwithus, name="workwithus"),
    path('accounts/userdashbord/', views.userdashboard, name="userdashboard"),
    path('accounts/logout/', views.logoutUser, name="logout"),
    path('test/', views.test, name="test"),

    

]
