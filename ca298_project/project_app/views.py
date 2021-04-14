from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .permissions import admin_required
from django.core import serializers as core_serializers
from rest_framework import viewsets
from .serializers import *


def index(request):
    return render(request, 'index.html')


def all_products(request):
    all_p = Product.objects.all()

    flag = request.GET.get('format', '')
    if flag == "json":
        serialised_products = core_serializers.serialize("json", all_p)
        return HttpResponse(serialised_products, content_type="application/json")
    else:
        return render(request, 'all_vegetables.html', {'products': all_p})


def singleproduct(request, prod_id):
    prod = get_object_or_404(Product, pk=prod_id)
    form = BasketItemForm
    return render(request, 'single_product.html', {'product': prod, 'form': form})


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
    products = []
    for item in user_basket:
        p = Product.objects.get(id=item.product_id)
        p.message = item.message
        p.basket_item_id = item.id
        products.append(p)
    price = sum([p.price for p in products])
    return render(request, 'basket.html', {'basket': user_basket, "products": products, "price": price})


@login_required
def remove_basket(request, item_id):
    BasketItems.objects.get(id=item_id).delete()
    return redirect("/basket/")


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
    message = request.POST.get("message")
    basket_item = BasketItems(basket_id=shopping_basket, product_id=product.id, message=message, price=product.price)
    basket_item.save()

    return redirect("/basket/")


@login_required
def order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            user = request.user
            basket_id = Basket.objects.get(user_id=user.id).id
            form = form.save()
            form.user_id = user
            form.save()
            for item in BasketItems.objects.filter(basket_id=basket_id):
                OrderItems(product=item.product, message=item.message, order_id=form.id).save()
                item.delete()
        return redirect(f"/view_order/{form.id}")
    else:
        form = OrderForm
        return render(request, 'orderform.html', {'form': form})


@login_required
def user_orders(request):
    orders = Order.objects.filter(user_id=request.user)
    completed_orders = CompletedOrder.objects.filter(user_id=request.user)
    return render(request, "user_orders.html", {"orders": orders, "comp_orders": completed_orders})


@login_required
def user_view_order(request, order_id):
    order_products = OrderItems.objects.filter(order_id=order_id)
    products = []
    for o in order_products:
        p = Product.objects.get(id=o.product_id)
        p.message = o.message
        products.append(p)
    return render(request, "user_single_order.html", {"products": products, "order": order_id})


@login_required
def user_view_complete_order(request, order_id):
    order_products = CompletedOrderItems.objects.filter(order_id=order_id)
    products = []
    for o in order_products:
        p = Product.objects.get(id=o.product_id)
        p.message = o.message
        products.append(p)
    return render(request, "user_single_order.html", {"products": products, "order": order_id})


@login_required
@admin_required
def all_orders(request):
    orders = [o for o in Order.objects.all()]
    return render(request, "all_orders.html", {"orders": orders})


@login_required
@admin_required
def view_order(request, order_id):
    order_products = OrderItems.objects.filter(order_id=order_id)
    products = []
    for o in order_products:
        p = Product.objects.get(id=o.product_id)
        p.message = o.message
        products.append(p)
    return render(request, "single_order.html", {"products": products, "order": order_id})


@login_required
@admin_required
def complete_order(request, order_id):
    o = Order.objects.get(id=order_id)
    order_products = OrderItems.objects.filter(order_id=o.id)
    print(len(order_products))
    comp_o = CompletedOrder(date_created=o.date_created, shipping_addr=o.shipping_addr, user_id=o.user_id)
    comp_o.save()
    o.delete()
    for oi in order_products:
        comp_oi = CompletedOrderItems(product_id=oi.product_id, order_id=comp_o.id, message=oi.message)
        print(comp_oi)
        comp_oi.save()
        oi.delete()
    return redirect("/admin_all_orders/")


def handler_404(request, *args, **kwargs):
    return render(request, "404.html")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = []
    permission_classes = []
