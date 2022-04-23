
from django.urls import path,include
from . import views
from .views import dashboard, analytic
app_name = 'admin-dashboard'
urlpatterns = [
    path('dashboard/',views.dashboard.as_view(),name='main'),
    path('analytics/',views.analytic.as_view(),name='analytics'),
]
