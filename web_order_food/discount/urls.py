from django.urls import path,include
from . import views
app_name = 'discount'
urlpatterns = [
   
    path('',views.render_discount,name='renderDiscount'),
]
