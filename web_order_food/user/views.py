from django.shortcuts import render

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
from django.core.mail import send_mail
import random
import logging

LOG= logging.getLogger('info')
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
        LOG.info(f"{user_name} successfully logged in the web")
        login(request,my_user)
        return redirect("home_page:home")
class register(View):
    def get(self,request):
         return render(request, 'register.html')
    def post(self,request):
        context = {}
        full_name = request.POST.get('fullname')
        user_name = request.POST.get('username')
        if (User.objects.filter(username = user_name).exists()):
            context['error'] = "Tên đăng nhập đã tồn tại"
            return render(request, 'register.html' ,{'context' : context})
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        my_email = request.POST.get('email')

        try:
            validate_email(my_email)
            if (password == repassword):
                my_user_name = User.objects.create_user(user_name,my_email,password)
                my_user_name.save()
                create_user = user.objects.create(fullname = full_name,user_name = my_user_name)
                create_user.save()
                LOG.info(f"{my_email} successfully create account: {user_name} in the web")
                return render(request, 'login.html')
            context['error'] = "Mật khẩu không khớp"
            return render(request, 'register.html' ,{'context' : context} )
        except ValidationError:
            context['email'] = "Email không hợp lệ"
        if (password != repassword):
            context['error'] = "Mật khẩu không khớp"
        return render(request, 'register.html' ,context)
class reset(View):
    def get(self, request):
        return render(request, 'reset_password.html')
    def post(self, request):
        content = request.POST.get('username_or_email')
        if (User.objects.filter(username=content).exists()):
            user_reset  = User.objects.get(username=content)
            email = user_reset.email
            password = str(random.randint(100000, 999999))
            user_reset.set_password(password)
            LOG.info(f"{email} successfully reset password for account: {content} in the web")
            a=send_mail('Reset your password','Your password: ' + password,'tenytdhn01@gmail.com',[str(email)])
            return render(request,'sendmail.html')

        return render(request, 'reset_pass_wrong.html')
