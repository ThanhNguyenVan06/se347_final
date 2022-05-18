
from django.urls import path,include
from . import views
app_name = 'home_page'
urlpatterns = [
   
    path('',views.home,name='home'),
    path('logout/',views.logout_user,name = 'logout'),
]
