from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from odds.models import Todo

# Create your views here.
def home(request):
    return render(request, 'home.html')


def about_me(request):
    return render(request, 'about_me.html')