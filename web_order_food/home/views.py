from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from menu.models import cart
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
    contexts = {'haha': 'haho'}
    i = 0
    for receipt in receipts:
        context = {'billCode':receipt.bill_code,}
        contexts[i] = context
        i += 1
    print()
    return HttpResponse(contexts[0]['billCode'], 200)