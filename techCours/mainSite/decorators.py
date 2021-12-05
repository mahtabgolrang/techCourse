from django.http import HttpResponse
from django.shortcuts import redirect
import logging

def unauthenticated_user(view_func):
    def wrapper_func(requset, *args , **kwargs):
        if requset.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(requset, *args , **kwargs)
    return wrapper_func
logger = logging.getLogger(__name__)

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(requset, *args , **kwargs):
            group = None
            if requset.user.groups.exists():
                group = requset.user.groups.all()[0].name
            if group == None:
                return HttpResponse("you are not authorized to view this page")
            if group in allowed_roles:
                 return view_func(requset, *args , **kwargs)
            else: 
                return HttpResponse("you are not authorized to view this page")
        return wrapper_func
    return decorator