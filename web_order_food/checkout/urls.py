
from django.urls import path,include
from . import views

app_name = 'checkout'
urlpatterns = [
   
    path('',views.check_cart_html.as_view(),name='check_cart_html'),
    path('checkout_process/',views.check_cart.as_view(),name='check_cart'),
    path('confirm/',views.confirm_infor.as_view(),name='confirm'),
    path('confirm/success/',views.success,name = 'pay_success'),
    path('confirm/success_v2/',views.success_v2,name = 'buy_success'),
    path('emptycart/',views.emptycart,name = 'empty_cart'),
    #delete item in checkout
    path('delete/',views.delete_item,name = 'delete_item'),
    path('changegood/',views.change_good,name = 'change_good')
    
]
