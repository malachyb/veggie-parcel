from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import *
from .models import *
from django.views.generic import CreateView
from django.contrib.auth import login


class UserSignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'user_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


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
