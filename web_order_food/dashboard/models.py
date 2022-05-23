from django.db import models
from django.views.generic import ListView
from menu.models import cart
# Create your models here.

class CartListView(ListView):
    paginate_by= 10
    model= cart
    template_name= "index1.html"