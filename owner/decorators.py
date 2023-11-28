from django.shortcuts import redirect
def super_sign_in_required(fn):
    def wrapperfn(request,*args,**kwargs):
        if request.user.is_superuser:
            return fn(request,*args,**kwargs)
        else:
            return redirect('login')
    return wrapperfn