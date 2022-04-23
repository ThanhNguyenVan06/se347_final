from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .models import food,cart
from django.http import JsonResponse 

# Create your views here.
class menu(View):
    def get(self,request):
        user = request.user.username
        all_food = food.objects.all()
        goods_user = cart.objects.filter(user_name = user , active = 0)
        if (goods_user.count() == 0):
            count_begin = ''
        else:
            count_begin = len(goods_user[0].id_foods.split(','))
        return render(request, 'menu_base.html',{'all_food':all_food,'count_begin':count_begin})
    def post(self,request):
        return HttpResponse("hello")
class add_to_cart(View):
    def get(self,request):
        id_food = request.GET.get("button_value")
        user = request.user.username
        goods_user = cart.objects.filter(user_name = user , active = 0)
        if (goods_user.count() == 0):
           creat_cart =  cart.objects.create(user_name = user,id_foods = id_food)
           creat_cart.save()
        else:
            goods = goods_user[0].id_foods + ',' + str(id_food)
            goods_user.update(id_foods=goods)
        count = len(goods_user[0].id_foods.split(','))
        return JsonResponse({'count':count,'id':id_food},status=200)
   