
from django.urls import path,include
from . import views
app_name = 'user'
urlpatterns = [
   
    path('login/',views.login_func.as_view(),name='login'),
    path('register/',views.register.as_view(),name='register'),
    path('reset/',views.reset.as_view(),name='reset'),
]
