from django.dispatch import receiver
from django.shortcuts import render
from django.views import View
from menu.models import cart,food
from discount.models import discounts
from django.http import HttpResponse, HttpResponseRedirect
import collections
from django.http import JsonResponse 
from django.shortcuts import redirect
from user.models import user
# Create your views here.
class check_cart(View):
    def get(self, request):
        
        user = request.user.username
        goods_user = cart.objects.filter(user_name = user , active = 0)
        if (goods_user.count() == 0):
            return HttpResponse(0)
        elif(len(goods_user[0].id_foods) == 0):
            goods_user[0].delete()
            return HttpResponse(0)
        
        else:
            arr_items= []
            items = goods_user[0].id_foods
            arr_id = items.split(",")
            id_count = collections.Counter(arr_id)
            for key,value in id_count.items():
                item = food.objects.get(id = key)
                 
                arr_items.append({'id_food':key,
                                  'quantity':value,
                                  'name_food' : item.name_food,
                                  'price' : item.price })
            
            return JsonResponse({'arr_items': arr_items},status=200)
        
    def post(self, request):
        user = request.user.username
        goods_user = cart.objects.filter(user_name = user , active = 0)
        if (goods_user.count() == 0):
            return render(request, 'empty_cart.html')
        items = goods_user[0].id_foods
        arr_id = items.split(",")
        item_set = set(arr_id)
        arr_items= []
        string_id_items = ""
        for i in range(len(item_set)):
            if (str(i+1) not in request.POST):
                pass
            else:
                for j in range(int(request.POST[str(i+1)])):
                    arr_items += str(i+1)
                    string_id_items =','.join(arr_items)
                    string_id_items =','.join(arr_items)
        if (string_id_items.isspace()):
            goods_user[0].delete()
            print(string_id_items)
            return render(request, 'empty_cart.html')
        # else :
        #     goods_user.update(id_foods = string_id_items)   
        return redirect('checkout:confirm')
class check_cart_html(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('user:login')
        return render(request, 'checkout.html')
class confirm_infor(View):
    def get(self, request):
        raw_price = 0
        name = request.user.username
        fullname_ = user.objects.get(user_name__username=name)
        fullname = fullname_.fullname
        goods_user = cart.objects.filter(user_name = name , active = 0)
        if (goods_user.count() == 0):
            return HttpResponse("Khong co san pham")
        # elif(goods_user[])
        else:
            arr_items= []
            items = goods_user[0].id_foods
            if(len(goods_user[0].id_foods) == 0):
                goods_user[0].delete()
                return render(request,'empty_cart.html')
            arr_id = items.split(",")
            id_count = collections.Counter(arr_id)
            print(id_count)
            for key,value in id_count.items():
                item = food.objects.get(id = key)
                raw_price += item.price*value
                arr_items.append({'id_food':key,
                                  'quantity':value,
                                  'name_food' : item.name_food,
                                  'price' : item.price,
                                  'image_food': item.image})
            goods_user.update(raw_price = raw_price, final_price = raw_price)  
        return render(request, 'comfirm.html',{'fullname':fullname,'raw_price':raw_price})
        # return HttpResponse(fullname)
    
    def post(self, request):
        name = request.user.username
        # fullname_ = user.objects.get(user_name__username=name)
        # fullname = fullname_.fullname
        raw_price,final_price = 0,0
        goods_user = cart.objects.filter(user_name = name , active = 0)
        receiver = request.POST.get("receiver")
        telephone_number = request.POST.get("nt")
        address = request.POST.get("address")
        discount = request.POST.get("discount")
        if (len(discount)  == 0 ):
            goods_user.update(receiver= receiver,number_telephone = telephone_number, address_ship = address)
        elif discounts.objects.filter(title = discount).exists():
            flag = 1
            goods_user.update(receiver= receiver,number_telephone = telephone_number, address_ship = address,coupon_code = discount)
            discount_percent = discounts.objects.filter(title = discount)[0].percent
            raw_price = goods_user[0].raw_price
            raw_prices = int(float(raw_price))
            #raw_price = int(raw_price)
            final_price = raw_prices*int(discount_percent)/100
            goods_user.update(final_price = final_price)
        else:
            goods_user.update(receiver= receiver,number_telephone = telephone_number, address_ship = address)
        return render(request, 'payment.html')
def success( request):
    name = request.user.username
    goods_user = cart.objects.filter(user_name = name , active = 0)
    goods_user.update(paid_bill = True,active = 1)
    
    return render(request, 'success.html')
def success_v2(request):
    name = request.user.username
    goods_user = cart.objects.filter(user_name = name , active = 0)
    goods_user.update(active = 1)
    return render(request, 'success.html')
def emptycart( request):
    return render(request, 'empty_cart.html')
def delete_item( request):
    id_del = request.GET['id']
    name = request.user.username
    goods_user = cart.objects.filter(user_name = name , active = 0)
    arr_items= []
    items = goods_user[0].id_foods
    arr_id = items.split(",") 
    arr_items = [item for item in arr_id if item != id_del]
    string_id_items =','.join(arr_items)
    goods_user.update(id_foods = string_id_items)
    return HttpResponse("SUcces")
def change_good(request):
    id_food = request.GET['name']
    quantity = request.GET['amount']
    name = request.user.username
    goods_user = cart.objects.filter(user_name = name , active = 0)
    arr_items= []
    items = goods_user[0].id_foods
    arr_id = items.split(",") 
    arr_items = [item for item in arr_id if item != id_food]
    for i in range(int(quantity)):
        arr_items.append(id_food)
    string_id_items =','.join(arr_items)
    goods_user.update(id_foods = string_id_items)
    food_price = food.objects.get(id = id_food).price
    total = int(quantity)*int(food_price)
    content = {
        'id':id_food,
        'price':food_price,
        "total" : total,
    }
    
    return JsonResponse ({
        'id':id_food,
        'price':food_price,
        "total" : total,
    })

