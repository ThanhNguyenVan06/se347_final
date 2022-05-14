from django.shortcuts import render
from django.views import View
from menu.models import food, cart
def get_12_month_prev():
    pass
def get_season_prev():
    pass
# Create your views here.
class dashboard(View):
    def get(self,request):
        # get the total profit weekly up to that date, monthly, seasonaly
        total_revenue=0
        total_food_sold=0
        total_revenue_week_up_to_now=0
        total_revenue_monthly=0
        total_revenue_seasonaly=0
        id_foods= cart.objects.filter(statement_bill_choice = "delivered").only('id_foods')
        for id_food in id_foods:
            total_revenue += food.objects.filter(id_food = id_food).only('price')
            total_food_sold+=1
        # get the total category
        total_category= category.objects.count()
        # get the total food sold item
        # get the total customer
        total_customer= cart.objects.values('user_name').distinct().count()
        # filter out top 5 food sold weekly(up to that day)
        return render(request, 'index.html',
                {
                    "total_revenue": total_revenue,
                    "total_food_sold": total_food_sold,
                    "total_category": total_category,
                    "total_customer": total_customer,
                })
class analytic(View):
    def get(self,request):
        return render(request, 'index1.html')