from django.shortcuts import render

# Create your views here.
def home(request):
    username = request.user.username
    return render(request, 'home.html',{'username':username})