import functools
from django.shortcuts import redirect

def store_manager_role_required(view_func, redirect_url="/order-manager/error/403"):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role == 'store_manager':
            return view_func(request, *args, **kwargs)
        return redirect(redirect_url)  
    return wrapper