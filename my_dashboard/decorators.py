from django.contrib.auth.decorators import user_passes_test
from . import urls
from django.shortcuts import redirect

def admin_only(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            return redirect('scan')  
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap