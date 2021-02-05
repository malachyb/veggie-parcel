from django.http import HttpResponse
from django.shortcuts import render
from .models import *


def index(request):
    return render(request, 'index.html')


def register(request):
    return HttpResponse("Hello from registration page")


def all_products(request):
    all_p = Product.objects.all()
    return render(request, 'all_vegetables.html', {"products": all_p})


def singleproduct(request, prod_id):
    prod = Product.objects.get(pk=prod_id)
    return render(request, 'single_product.html', {'product': prod})
