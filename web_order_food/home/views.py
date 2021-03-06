import collections
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.views import View
from menu.models import cart
from user.models import user,User
from django.contrib.auth import authenticate,login
from django.core.paginator import Paginator
from collections import defaultdict

import logging
from common.currency import Currency

LOG= logging.getLogger('info')
NUM_BILL_PER_PAGE = 5
from menu.models import food
# Create your views here.
def home(request):
    username = request.user.username
    food_name_counts= defaultdict(int)
    images = []
    prices = []
    carts= cart.objects.all()
    for cart_item in carts:
        for id_food in cart_item.id_foods.split(","):
            food_query= food.objects.get(id=id_food)
            food_name_counts[food_query.name_food]+=1
    food_name_counts = sorted(food_name_counts.items(),key=(lambda i: i[1]))

    # get properties of three best sellers food
    food_query=food.objects.get(name_food=food_name_counts[-1][0])
    first_best_seller= {'name': food_query.name_food, 'price': Currency.convert_currency(food_query.price), 'image': food_query.image}
    food_query=food.objects.get(name_food=food_name_counts[-2][0])
    second_best_seller= {'name': food_query.name_food, 'price': Currency.convert_currency(food_query.price), 'image': food_query.image}
    food_query=food.objects.get(name_food=food_name_counts[-3][0])
    third_best_seller= {'name': food_query.name_food, 'price': Currency.convert_currency(food_query.price), 'image': food_query.image}

    data={
        "first_best_seller": first_best_seller,
        "second_best_seller": second_best_seller,
        "third_best_seller": third_best_seller,
    }

    return render(request, 'home.html',{'username':username, 'food_best_seller': data})
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
            LOG.info(f'{user_name} successfully reset the password')
            return JsonResponse({'message': 'C????p nh????t m????t kh????u tha??nh c??ng', 'status': 'success'},status=200)
        else:
            return JsonResponse({'message': 'Sai m????t kh????u', 'status': 'fail'},status=403)
    def get(self,request):
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        user_name = request.user.username
        return render(request, 'changepass.html',{'user_name':user_name})
def all_bill(request):
    username = request.user.username
    page = 1
    if request.GET.get('page') != None:
        page = request.GET.get('page')
    else:
        page = 1
    bill_code_list = cart.objects.filter(user_name = username, active = 1)
    totalPage = bill_code_list.count();
    p = Paginator(bill_code_list, NUM_BILL_PER_PAGE)
    bill_code_list = p.page(page).object_list
    dict_bill_code = []
    for i in range (len(bill_code_list)):
        dict_bill_code.append({
            'code': bill_code_list[i].bill_code,
            'address': bill_code_list[i].address_ship,
            'status': bill_code_list[i].statement_bill,
            })
    pages = range(1, p.num_pages + 1)
    return render(request, 'list_bill.html', {'listBill': dict_bill_code, 'totalPage': pages})
def detail_bill(request):
    bill_code = request.GET.get('billCode')
    detail_bill_code = cart.objects.filter(bill_code=bill_code)

    if (detail_bill_code.count() > 0):
        arr_items= []
        if (detail_bill_code[0].user_name == request.user.username) :
            items = detail_bill_code[0].id_foods
            arr_id = items.split(",")
            id_count = collections.Counter(arr_id)
            for key,value in id_count.items():
                item = food.objects.get(id = key)

                arr_items.append({'id_food':key,
                                  'quantity':value,
                                  'name_food' : item.name_food,
                                  'image_url': item.image.url,
                                  'price' : item.price })
            return JsonResponse({'arr_items': arr_items,
            'billCode': bill_code,
            'address': detail_bill_code[0].address_ship,
            'status': detail_bill_code[0].statement_bill,},status=200)
def change_profile(request):
    fullname = request.POST.get('fullname')
    address = request.POST.get('address')
    email = request.POST.get('email')
    old_profile = user.objects.get(user_name__username = request.user.username)
    user_reset  = User.objects.get(username= request.user.username)

    old_profile.address = address
    old_profile.fullname = fullname
    user_reset.email = email
    old_profile.save()
    user_reset.save()
    LOG.info(f"{request.user.username} successfully update the profile")
    return JsonResponse({'message': 'C????p nh????t th??ng tin tha??nh c??ng', 'status': 'success'},status=403)
