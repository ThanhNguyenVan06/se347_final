from django.shortcuts import render
from django.core.paginator import Paginator
from .models import news
# Create your views here.
def render_news(request):
    all_posts = news.objects.all()
    posts_paginator = Paginator(all_posts,4)
    index_page = request.GET.get('page')
    page = posts_paginator.get_page(index_page)
    context = { 'count' : posts_paginator.count,
               'page':page,
        
    }
    return render(request, 'news.html', context)