from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def register(request):
    return HttpResponse("Hello from registration page")
