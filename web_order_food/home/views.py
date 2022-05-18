from django.shortcuts import redirect, render
from django.contrib.auth import logout
# Create your views here.
def home(request):
    username = request.user.username
    return render(request, 'home.html',{'username':username})
def logout_user(request):
    logout(request)
    return redirect('home_page:home')