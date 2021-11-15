from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(requset, *args , **kwargs):
        if requset.user.is_authenticated:
            return redirect('main')
        else:
            return view_func(requset, *args , **kwargs)
    return wrapper_func