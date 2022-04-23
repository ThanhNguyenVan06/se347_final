
from django.urls import path,include
from . import views

app_name = 'checkout'
urlpatterns = [
   
    path('',views.check_cart_html.as_view(),name='check_cart_html'),
    path('checkout_process/',views.check_cart.as_view(),name='check_cart'),
]
