from django.shortcuts import render
from django.views import View
from menu.models import food, cart, category
from collections import defaultdict
def get_12_month_prev():
    pass
def get_season_prev():
    pass
# Create your views here.
class dashboard(View):
    def get(self,request):
        # get the total profit weekly up to that date, monthly, seasonaly
        total_revenue=0
        categories_sold=defaultdict(int)
        total_food_sold=0
        carts= cart.objects.only('id_foods').filter(paid_bill = True).all()
        for cart_item in carts:
            id_foods= cart_item.id_foods.split(",")
            for id_food in id_foods:
                price=int(food.objects.get(id = str(id_food), active=1).price)
                total_revenue +=price
                total_food_sold+=1
                categories_sold[id_food]+= price
        # get the total category
        total_category= category.objects.count()
        # get the total food sold item
        # get the total customer
        total_customer= cart.objects.values('user_name').distinct().count()
        # filter out top 5 food sold weekly(up to that day)

        # get pending user cart
        pending_carts= cart.objects.filter(statement_bill=0).all()
        pending_carts_list=[]
        for cart_item in pending_carts:
            total_price=0
            name_food_boughts=[]
            for id_food in cart_item.id_foods:
                food_query= food.objects.get(id=id_food)
                name_food_boughts.append(food_query.name_food)
                total_price+=int(food_query.price)
            pending_cart_item= {
                "user_name": cart_item.user_name,
                "Food bought": ",".join(name for name in name_food_boughts),
                "Total price": total_price ,
                "Status": cart.statement_bill_choice[0][1]
            }
            pending_carts_list.append(pending_cart_item)
            
        return render(request, 'index.html',
                {
                    "total_revenue": total_revenue,
                    "total_food_sold": total_food_sold,
                    "total_category": total_category,
                    "total_customer": total_customer,
                    "pending_cart_list": pending_carts_list
                })
class analytic(View):
    def get(self,request):
        total_revenue_week_up_to_now=0
        total_revenue_monthly=0
        total_revenue_seasonaly=0
        return render(request, 'index1.html')