import collections
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.views import View
from menu.models import cart
from user.models import user,User
from django.contrib.auth import authenticate,login

from menu.models import food
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
    loggedUser = User.objects.get(username = user_name)
    profile[0].email = loggedUser.email
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
            return JsonResponse({'message': 'Cập nhật mật khẩu thành công', 'status': 'success'},status=200)
        else:
            # return HttpResponse("Sai password")
            return JsonResponse({'message': 'Sai mật khẩu', 'status': 'fail'},status=403)
    def get(self,request):
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        user_name = request.user.username
        return render(request, 'changepass.html',{'user_name':user_name})
def all_bill(request):
    username = request.user.username
    bill_code_list = cart.objects.filter(user_name = username, active = 1)
    dict_bill_code = {}
    for i in range (len(bill_code_list)):
        dict_bill_code[i] = bill_code_list[i].bill_code
    return JsonResponse(dict_bill_code)
def detail_bill(request):
    bill_code = request.GET.get('billCode')
    detail_bill_code = cart.objects.filter(bill_code=bill_code)
    if (detail_bill_code.count() > 0):
        arr_items= []
        if (detail_bill_code[0].user_name == request.user.username) :
            items = detail_bill_code[0].id_foods
            address = detail_bill_code[0].address_ship
            reciver = detail_bill_code[0].reciver
            statement_bill = detail_bill_code[0].statement_bill
            statement_bill_content = ""
            if (statement_bill == 0):
                statement_bill_content  = "Đang xác nhận"
            elif (statement_bill == 1):
                statement_bill_content = "Đang giao hàng"
            else:
                statement_bill_content = "Đã giao hàng"
            arr_id = items.split(",")
            id_count = collections.Counter(arr_id)
            for key,value in id_count.items():
                item = food.objects.get(id = key)
                 
                arr_items.append({'id_food':key,
                                  'quantity':value,
                                  'name_food' : item.name_food,
                                  'image_url': item.image.url,
                                  'price' : item.price })
            return JsonResponse({'arr_items': arr_items,'reciver':reciver,'address':address,'statement_bill_content':statement_bill_content},status=200)
def change_profile(request):
    fullname = request.POST.get('fullname') 
    address = request.POST.get('address')
    email = request.POST.get('email')
    print("fullname: ", fullname);
    print("address: ", address )
    old_profile = user.objects.get(user_name__username = request.user.username)
    user_reset  = User.objects.get(username= request.user.username)

    old_profile.address = address
    old_profile.fullname = fullname
    user_reset.email = email
    old_profile.save()
    user_reset.save()
    # return HttpResponse("Update thành công")
    # return redirect("home_page:home")
    return JsonResponse({'message': 'Cập nhật thông tin thành công', 'status': 'success'},status=403)

# def bestSeller(self, request):
                   
