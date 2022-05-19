from django.shortcuts import render
from matplotlib.style import context
from . import views
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from .models import user
from django.contrib.auth.models import User
import home
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
class login_func(View):
    def get(self,request):
         return render(request, 'login.html')
    def post(self,request):
        user_name = request.POST.get('username')
        user_password = request.POST.get('password')
        my_user = authenticate(username = user_name,password = user_password)
        if my_user is None:
            context = "Tài khoản hoặc mật khẩu không đúng"
            return render(request, 'login.html', {'context':context})
        login(request,my_user)
        return redirect("home_page:home")
class register(View):
    
    def get(self,request):
         return render(request, 'register.html')
    def post(self,request):
        full_name = request.POST.get('fullname')
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        my_email = request.POST.get('email')
        context = {}
        try: 
            validate_email(my_email)
            if (password == repassword):
                my_user_name = User.objects.create_user(user_name,my_email,password)
                my_user_name.save()
                create_user = user.objects.create(fullname = full_name,user_name = my_user_name)
                create_user.save()
                return render(request, 'login.html')
            context['repassword'] = "Mật khẩu không khớp"
            return render(request, 'register.html' ,{'context' : context} )    
        except ValidationError:
            context['email'] = "Email không hợp lệ"
        if (password != repassword):  
            context['repassword'] = "Mật khẩu không khớp"
        return render(request, 'register.html' ,context)