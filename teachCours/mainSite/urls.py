from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),

]
