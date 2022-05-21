from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,HttpResponseRedirect
from .models import food,cart
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
import time 
# Create your views here.
class menu(View):
    def get(self,request):
        user = request.user.username
        all_food = food.objects.all()
        all_food_panigation = Paginator(all_food,1)
        index_page = request.GET.get('page')
        page = all_food_panigation.get_page(index_page)
        goods_user = cart.objects.filter(user_name = user , active = 0)
        if (goods_user.count() == 0):
            count_begin = ''
        else:
            count_begin = len(goods_user[0].id_foods.split(','))
        return render(request, 'menu_base.html',{'all_food':page,'count_begin':count_begin})
    def post(self,request):
        return HttpResponse("hello")
class add_to_cart(View):
    
    def get(self,request):
        
        if not request.user.is_authenticated:
            return JsonResponse({'count':-1})
        else:
            id_food = request.GET.get("button_value")
            user = request.user.username
            goods_user = cart.objects.filter(user_name = user , active = 0)
            if (goods_user.count() == 0):
                bill_code_temp = str(time.time()) + str(user)
                creat_cart =  cart.objects.create(user_name = user,id_foods = id_food,bill_code = bill_code_temp)
                creat_cart.save()
            else:
                goods = goods_user[0].id_foods + ',' + str(id_food)
                goods_user.update(id_foods=goods)
            count = len(goods_user[0].id_foods.split(','))
            return JsonResponse({'count':count,'id':id_food},status=200)
def search(request):
    content_search = request.GET.get('search')
    
    foods_search = food.objects.filter(name_food__contains = content_search) 
    all_food_panigation = Paginator(foods_search,2)
    index_page = request.GET.get('page')
    page = all_food_panigation.get_page(index_page)
    
    user = request.user.username
    
    
    goods_user = cart.objects.filter(user_name = user , active = 0)
    if (goods_user.count() == 0):
        count_begin = ''
    else:
        count_begin = len(goods_user[0].id_foods.split(','))
    return render(request, 'menu_search.html',{'all_food':page,'search':content_search,'count_begin':count_begin})    
   