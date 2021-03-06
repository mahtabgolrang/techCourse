from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.main, name="main"),
    path('accounts/login/', views.loginPage, name="login"),
    path('accounts/register/', views.registerPage, name="register"),
    path('accounts/workwithus/', views.workwithus, name="workwithus"),
    path('test/', views.test, name="test"),
    path('accounts/userdashbord/main',
         views.userdashboard, name="userdashboard-main"),
    path('accounts/userdashbord/profile',
         views.userDashboardProfile, name="userdashboard-profile"),
    path('accounts/logout/', views.logoutUser, name="logout"),
    path('accounts/teacherdashboard/main',
         views.teacherDashboard, name="teacherdashboard-main"),
    path('accounts/teacherdashboard/profile',
         views.TeacherDashboardProfile, name="teacherdashboard-profile"),
    path('accounts/teacherdashboard/create-course',
         views.teacherDashboardCreateCourse, name="teacherdashboard-create-course"),
    path('accounts/teacherdashboard/resume',
         views.teacherDashboardResume, name="teacherdashboard-resume"),
    path('accounts/teacherdashboard/transaction',
         views.teacherDashboardTransaction, name="teacherdashboard-transaction"),
    path('course/<int:course_id>/', views.courseDetailsView, name="course"),
    path('allcourse/', views.showAllCourse, name="allcourse"),
    path('accounts/' ,include('django.contrib.auth.urls')),
    path('payment/<int:course_id>/',views.payment ,name="payment")     

]
