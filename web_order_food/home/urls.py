
from django.urls import path,include
from . import views
app_name = 'home_page'
urlpatterns = [
   
    path('',views.home,name='home'),
    path('logout/',views.logout_user,name = 'logout'),
    path('purchase/',views.purchase_user,name = 'purchase'),
    path('profile/',views.profile,name = 'profile'),
    path('profile/setProfile',views.change_profile,name = 'change_profile'),
    
    path('profile/password/',views.changePassword.as_view(),name = 'change_password'),
    #listed bill 
    path('listbill/',views.all_bill,name='listbill'),
    #detail bill(url:listbill/detail/?billcode=(billcode))
    path('listbill/detail/',views.detail_bill,name='detailbill'),
]
