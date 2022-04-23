from django.shortcuts import render
from django.views import View

# Create your views here.
class dashboard(View):
    def get(self,request):
        return render(request, 'index.html')
class analytic(View):
    def get(self,request):
        return render(request, 'index1.html')