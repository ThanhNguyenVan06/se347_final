from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.views import View
from menu.models import cart
from user.models import user,User
from django.contrib.auth import authenticate,login
# Create your views here.
def home(request):
    username = request.user.username
    return render(request, 'home.html',{'username':username})
def logout_user(request):
    logout(request)
    return redirect('home_page:home')
def purchase_user(request):
    user_name = request.user.username
    receipts = cart.objects.filter(user_name = user_name , active = 1)
    contexts = {}
    i = 0
    for receipt in receipts:
        context = {'billCode':receipt.bill_code,}
        contexts[i] = context
        i += 1
    return HttpResponse(contexts[0]['billCode'], 200)
def profile (request):
    user_name = request.user.username
    profile = user.objects.filter(user_name__username=user_name)
    return render(request, 'profile.html', {'profile':profile[0]})
    # return HttpResponse(profile[0])
class changePassword(View):
    def post(self, request):
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        user_name = request.user.username
        user_current = User.objects.get(username=user_name)
        
        if user_current.check_password(current_password):
            user_current.set_password(new_password)
            user_current.save()
            my_user = authenticate(username = user_name,password = new_password)
            login(request,my_user)
            return render(request, 'changepass.html')
        else:
            return HttpResponse("Sai password")
    def get(self,request):
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        user_name = request.user.username
        return render(request, 'changepass.html',{'user_name':user_name})
        
