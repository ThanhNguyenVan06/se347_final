
from django.urls import path,include
from . import views
app_name = 'news'
urlpatterns = [
   
    path('',views.render_news,name='render_news'),
]
