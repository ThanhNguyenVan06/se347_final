from django.shortcuts import render

# Create your views here.
def render_news(request):
    return render(request, 'news.html')