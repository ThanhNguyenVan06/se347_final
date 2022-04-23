from django.shortcuts import render
from django.views import View
from menu.models import cart,food
from django.http import HttpResponse
import collections
from django.http import JsonResponse 
# Create your views here.
class check_cart(View):
    def get(self, request):
        user = request.user.username
        goods_user = cart.objects.filter(user_name = user , active = 0)
        if (goods_user.count() == 0):
            return HttpResponse("Khong co san pham")
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
        
        goods_user.update(id_foods = string_id_items)
        
        return HttpResponse(string_id_items)
class check_cart_html(View):
    def get(self, request):
        return render(request, 'checkout.html')
    def post(self, request):
        return render(request, 'checkout.html')