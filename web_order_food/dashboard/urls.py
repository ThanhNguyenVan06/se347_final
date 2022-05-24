
from django.urls import path
from . import views
app_name = 'admin-dashboard'
urlpatterns = [
    path('dashboard/',views.dashboard.as_view(),name='main'),
    path('analytics/',views.analytic.as_view(),name='analytics'),
]
