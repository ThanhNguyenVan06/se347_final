from django.shortcuts import render
from django.core.paginator import Paginator
from .models import discounts
from django.http import HttpResponse, JsonResponse
# Create your views here.

def render_discount(request):
    coupons = discounts.objects.all()
    coupons_paginator = Paginator(coupons,2)
    index_page = request.GET.get('page')
    page = coupons_paginator.get_page(index_page)
    context = { 'count' : coupons_paginator.count,
               'page':page,
        
    }
    return render(request, 'discount.html', context)
