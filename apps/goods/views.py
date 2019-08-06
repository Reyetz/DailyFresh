from django.shortcuts import render

# Create your views here.


# /localhost
def index(request):
    '''首页'''
    return render(request, 'index.html')
