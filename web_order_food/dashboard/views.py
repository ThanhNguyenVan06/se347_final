from datetime import  datetime
import locale
import logging
from collections import defaultdict

from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay

from menu.models import food, cart, category
from dashboard.service.food import food_service
from dashboard.service.time import time_service
from django.core.paginator import Paginator
from common.currency import Currency

DEFAULT_AVATAR="/static/home/image/default-user.png"


LOG= logging.getLogger('info')

class dashboard(View):
    def get(self,request):
        # get the total profit weekly up to that date, monthly, seasonaly
        LOG.info(f"{request.user} acessed dashboard page")
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
            total_revenue_season+= food_service.get_total_price_from_queryset(total_cart_season)

        # user=User.objects.filter(username = request.user)
        return render(request, 'index.html',
                {
                    "total_revenue": Currency.convert_currency(total_revenue),
                    "total_food_sold": Currency.convert_currency(total_food_sold),
                    "total_category": total_category,
                    "total_customer": total_customer,
                    "extra_area_chart_var_list": extra_area_chart_var_list,
                    "category_list": category_list,
                    "categories_sold": dict(categories_sold),
                    "curr_year": curr_year,
                    "curr_month": curr_month,
                    "curr_season": curr_season_num,
                    "total_revenue_year": Currency.convert_currency(total_revenue_year),
                    "total_revenue_month": Currency.convert_currency(total_revenue_month),
                    "total_revenue_week_up_to_now": Currency.convert_currency(total_revenue_week_up_to_now),
                    "total_revenue_season": Currency.convert_currency(total_revenue_season),
                    "user_name": request.user,
                    "user_avatar": DEFAULT_AVATAR # will fix when user have avatar attribute
                })


class analytic(View):
    def get(self,request):
        LOG.info(f"{request.user} acessed analytic page")
        carts=None
        cart_list=None
        page_cart=None
        filter_value= request.GET.get("filter_value")
        if filter_value == None or filter_value == "1" :
            carts= cart.objects.filter(statement_bill__in=[0,1])
        elif filter_value =="2":
            carts= cart.objects.filter(statement_bill=0)
        elif filter_value =="3":
            carts= cart.objects.filter(statement_bill=1)
        if carts:
            paginator = Paginator(carts,10 ) # Show 25 contacts per page.

            toggle_id=request.GET.get("button_value")
            toggle_type=request.GET.get("type")
            page_number = request.GET.get('page',1)

            page_cart= paginator.get_page(page_number)
            cart_list=[]
            food_name_counts= defaultdict(int)
            int_to_status= {0: "pending", 1: "delivering", 2: "delivered"}

            for cart_item in page_cart:
                total_price=0
                name_food_boughts=[]
                for id_food in cart_item.id_foods.split(","):
                    food_query= food.objects.get(id=id_food)
                    name_food_boughts.append(food_query.name_food)
                    total_price+=int(food_query.price)
                if toggle_id != None and int(toggle_id)== cart_item.id:
                    if toggle_type == "status":
                        cart_item.statement_bill+=1
                        LOG.info(f'{request.user} change the status bill of {toggle_id}')
                    else:
                        cart_item.paid_bill=cart_item.paid_bill
                        LOG.info(f'{request.user} change the status bill of {toggle_id}')
                    cart_item.save()
                cart_item_statuses= {
                    "id": cart_item.id,
                    "user_name": cart_item.user_name,
                    "food_bought": ",".join(name for name in name_food_boughts),
                    "total_price": Currency.convert_currency(total_price) ,
                    "status":  int_to_status[cart_item.statement_bill],
                    "paid_bill": cart_item.paid_bill
                }
                cart_list.append(cart_item_statuses)
            carts= cart.objects.all()
            for cart_item in carts:
                for id_food in cart_item.id_foods.split(","):
                    food_query= food.objects.get(id=id_food)
                    food_name_counts[food_query.name_food]+=1
            food_name_counts = sorted(food_name_counts.items(),key=(lambda i: i[1]))
        # get the total revenue of each category following months
        today= datetime.today
        curr_month= today().month
        curr_year= today().year
        categories_sold_months=[0 for _ in range(0, curr_month)]
        query_set= cart.objects.annotate(year= ExtractYear("date_created"), month= ExtractMonth("date_created")).filter(year=curr_year, month__in=[m for m in range(1, curr_month+1)])
        for query in query_set:
            categories_sold_months[query.month-1]+= len(query.id_foods.split(","))
        order_statuses = {
            0:0,
            1:0,
            2:0,
        }
        for k in order_statuses.keys():
            order_statuses[k]= cart.objects.filter(statement_bill=k).count()
        return render(request, 'index1.html',
                    {
                        "first_best_seller": {"name":food_name_counts[-1][0],"value":food_name_counts[-1][1]},
                        "second_best_seller": {"name":food_name_counts[-2][0],"value":food_name_counts[-2][1]},
                        "third_best_seller": {"name":food_name_counts[-3][0],"value":food_name_counts[-3][1]},
                        "order_statuses": order_statuses,
                        "cart_list": cart_list,
                        "page_cart": page_cart,
                        "categories_sold_months": categories_sold_months,
                        "month_list": [m for m in range(1,curr_month+1)],
                        "filter_value": filter_value,
                        "user_name": request.user,
                        "user_avatar": DEFAULT_AVATAR # will fix when user have avatar attribute
                    })
