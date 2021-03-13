from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import Product, User, Basket, BasketItems
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .permissions import admin_required


def index(request):
    return render(request, 'index.html')


def register(request):
    return render(request, 'registration.html')


def all_products(request):
    all_p = Product.objects.all()
    return render(request, 'all_vegetables.html', {'products': all_p})


def singleproduct(request, prod_id):
    prod = get_object_or_404(Product, pk=prod_id)
    return render(request, 'single_product.html', {'product': prod})


@login_required
@admin_required
def product_form(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_prod = form.save()
            return render(request, 'single_product.html', {'product': new_prod})
    else:
        form = ProductForm()
        return render(request, 'form.html', {'form': form})


@login_required
def basket(request):
    user = request.user
    basket_id = Basket.objects.get(user_id=user.id).id
    user_basket = BasketItems.objects.filter(basket_id=basket_id)
    products = [Product.objects.get(id=item.product_id) for item in user_basket]
    for p in products:
        print(p.name)
    return render(request, 'basket.html', {'basket': user_basket, "products": products})


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


class AdminSignupView(CreateView):
    model = User
    form_class = AdminSignupForm
    template_name = 'admin_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class Login(LoginView):
    template_name = 'login.html'


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def add_to_basket(request, prod_id):
    user = request.user
    try:
        shopping_basket = Basket.objects.get(user_id=user)
    except:
        shopping_basket = Basket(user_id=user)
        shopping_basket.save()

    product = Product.objects.get(pk=prod_id)
    basket_items = BasketItems.objects.filter(basket_id=shopping_basket.id, product_id=product.id).first()

    if basket_items is None:
        basket_items = BasketItems(basket_id=shopping_basket, product_id=product.id).save()
    else:
        basket_items.quantity = basket_items.quantity + 1
        basket_items.save()

    return render(request, 'single_product.html', {'product': product, 'added': True})
