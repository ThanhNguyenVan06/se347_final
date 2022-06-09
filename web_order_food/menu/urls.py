
from django.urls import path,include
from . import views
from .views import menu,add_to_cart
app_name = 'menu'
urlpatterns = [
   
    path('',views.menu.as_view(),name='menu'),
    path('cart/',views.add_to_cart.as_view(),name='add_to_cart'),
    path('search/',views.search,name = 'search'),
    path('search/cart/',views.add_to_cart.as_view(),name='add_to_cart_search'),
]
