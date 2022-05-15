from datetime import date, datetime
from django.shortcuts import render
from django.views import View
from menu.models import food, cart, category
from collections import defaultdict
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeekDay, ExtractDay

from dashboard.service.food import food_service
from dashboard.service.time import time_service
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
                query=food.objects.get(id = str(id_food), active=1)
                price=int(query.price)
                total_revenue +=price
                total_food_sold+=1
                categories_sold[query.category_food.category]+= 1 
        # get the total category
        total_category= category.objects.count()
        # get the total food sold item
        # get the total customer
        total_customer= cart.objects.values('user_name').distinct().count()

        # filter out top 5 food sold weekly(up to that day)
        # total category sold for each period
        category_list=[]
        for query in category.objects.values("category"):
            category_list.append(query['category'])
        total_carts = cart.objects.filter(paid_bill=True).annotate(year= ExtractYear("date_created")).order_by("year").values("year","id_foods")
        extra_area_chart_var_dict={}
        total_category_sold=0
        for cart_item in total_carts:
            if cart_item['year'] not in extra_area_chart_var_dict.keys():
                extra_area_chart_var_dict[cart_item['year']]=defaultdict(int)
            for id_food in cart_item["id_foods"].split(","):
                    query= food.objects.get(id=id_food)    
                    extra_area_chart_var_dict[cart_item['year']][query.category_food.category]+=1
                    total_category_sold+=1
        extra_area_chart_var_list=[]
        for i in extra_area_chart_var_dict.keys():
            var_dict= {
                "period": str(i)
            }
            for k,v in extra_area_chart_var_dict[i].items(): 
                var_dict[k]=v
            for category_item in category_list:
                if category_item not in var_dict.keys():
                    var_dict[category_item]=0
            extra_area_chart_var_list.append(var_dict)
        # calculate the percentage of category sold
        for category_ in category_list:
            categories_sold[category_]= round((categories_sold[category_] / total_category_sold) * 100)
        # get pending user cart
        pending_carts= cart.objects.filter(statement_bill=0).all()
        pending_cart_list=[]
        for cart_item in pending_carts:
            total_price=0
            name_food_boughts=[]
            for id_food in cart_item.id_foods.split(","):
                food_query= food.objects.get(id=id_food)
                name_food_boughts.append(food_query.name_food)
                total_price+=int(food_query.price)
            pending_cart_item= {
                "user_name": cart_item.user_name,
                "food_bought": ",".join(name for name in name_food_boughts),
                "total_price": total_price ,
                "status": cart.statement_bill_choice[0][1]
            }
            pending_cart_list.append(pending_cart_item)
        return render(request, 'index.html',
                {
                    "total_revenue": total_revenue,
                    "total_food_sold": total_food_sold,
                    "total_category": total_category,
                    "total_customer": total_customer,
                    "pending_cart_list": pending_cart_list,
                    "extra_area_chart_var_list": extra_area_chart_var_list,
                    "category_list": category_list,
                    "categories_sold": dict(categories_sold),
                })
class analytic(View):
    def get(self,request): 
        # total revenure
        season_map={
            1: range(1,4),
            2: range(4,7),
            3: range(7,10),
            4: range(10,12),
        }
        today= datetime.today()
        curr_year= today.year
        curr_month= today.month
        weekdays= time_service.get_all_weekday_to_now()
        curr_season=0
        curr_season_num=0
        for season in season_map:
            if curr_month in season_map[season]:
                curr_season=season_map[season]
                curr_season_num=season
                break
        # total year revenue
        total_revenue_year=0
        total_revenue_week_up_to_now=0
        total_revenue_month=0
        total_revenue_season=0
        total_cart_year= cart.objects.annotate(year= ExtractYear("date_created")).filter(year = curr_year)
        total_revenue_year= food_service.get_total_price_from_queryset(total_cart_year)
        total_cart_month= cart.objects.annotate(month= ExtractMonth("date_created"), year= ExtractYear("date_created")).filter(month = curr_month, year= curr_year, paid_bill=True)
        total_revenue_month= food_service.get_total_price_from_queryset(total_cart_month)
        for weekday in weekdays:
            total_cart_week= cart.objects.annotate(month= ExtractMonth("date_created"), year= ExtractYear("date_created"), day= ExtractDay("date_created")).filter(day = weekday, month= curr_month, year=curr_year, paid_bill=True)
            total_revenue_week_up_to_now+= food_service.get_total_price_from_queryset(total_cart_week)
        for month in curr_season:
            total_cart_season= cart.objects.annotate(month= ExtractMonth("date_created"), year= ExtractYear("date_created")).filter(month = month, year= curr_year, paid_bill=True)
            total_revenue_season+= food_service.get_total_price_from_queryset(total_cart_week)
        return render(request, 'index1.html',
                    {
                    "curr_year": curr_year,
                    "curr_month": curr_month,
                    "curr_season": curr_season_num,
                    "total_revenue_year": total_revenue_year,
                    "total_revenue_month": total_revenue_month,
                    "total_revenue_week_up_to_now": total_revenue_week_up_to_now,
                    "total_revenue_season": total_revenue_season,
                    })