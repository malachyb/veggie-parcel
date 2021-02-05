from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import *
from .models import *


def index(request):
    return render(request, 'index.html')


def register(request):
    return HttpResponse("Hello from registration page")


def all_products(request):
    all_p = Product.objects.all()
    return render(request, 'all_vegetables.html', {'products': all_p})


def singleproduct(request, prod_id):
    prod = get_object_or_404(Product, pk=prod_id)
    return render(request, 'single_product.html', {'product': prod})


def product_form(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            prod = form.save()
            return render(request, 'single_product.html', {'product': prod})
    else:
        form = ProductForm()
        return render(request, 'form.html', {'form': form})
