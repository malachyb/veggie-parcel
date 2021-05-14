import json

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core import serializers as core_serializers
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BaseAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from django.forms.models import model_to_dict
from django.core.serializers import serialize
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *
from .permissions import admin_required
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


@authentication_classes([SessionAuthentication, BaseAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def product_form(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_prod = form.save()
            return render(request, 'single_product.html', {'product': new_prod})
    else:
        form = ProductForm()
        return render(request, 'form.html', {'form': form})


# @login_required
@authentication_classes([SessionAuthentication, BaseAuthentication])
@permission_classes([IsAuthenticated])
def basket(request):
    user = request.user
    if user.is_anonymous:
        token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        user = Token.objects.get(key=token).user
    basket_id = Basket.objects.get(user_id=user.id).id
    user_basket = BasketItems.objects.filter(basket_id=basket_id)
    products = []
    for item in user_basket:
        p = Product.objects.get(id=item.product_id)
        p.message = item.message
        p.basket_item_id = item.id
        products.append(p)
    price = sum([p.price for p in products])
    flag = request.GET.get('format', '')  # url?format=json&name=John   {'format':'json', 'name':'John'}
    if flag == "json":
        basket_array = []
        for p in products:
            item = {"picture": p.picture.url, "product": p.name, "price": f"{float(p.price):.2f}", "message": p.message}
            basket_array.append(item)
        return HttpResponse(json.dumps({'items': basket_array}), content_type="application/json")

    return render(request, 'basket.html', {'basket': user_basket, "products": products, "price": price})


# @login_required
@authentication_classes([SessionAuthentication, BaseAuthentication])
@permission_classes([IsAuthenticated])
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


# @login_required
@authentication_classes([SessionAuthentication, BaseAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def add_to_basket(request, prod_id):
    user = request.user
    if user.is_anonymous:
        token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        user = Token.objects.get(key=token).user
    try:
        shopping_basket = Basket.objects.get(user_id=user)
    except:
        shopping_basket = Basket(user_id=user)
        shopping_basket.save()

    flag = request.GET.get('format', '')  # url?format=json&name=John   {'format':'json', 'name':'John'}
    product = Product.objects.get(pk=prod_id)
    message = request.POST.get("message") if flag != "json" else json.loads(request.body).get("message")
    basket_item = BasketItems(basket_id=shopping_basket, product_id=product.id, message=message, price=product.price)
    basket_item.save()
    if flag == "json":
        return JsonResponse({'status': 'success'})
    return redirect("/basket/")


# @login_required
@authentication_classes([SessionAuthentication, BaseAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def order(request):
    if request.method == "POST":
        if not request.POST:  # if the data is not inside the request.POSt, it is inside the body
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            form = OrderForm(body)
        else:
            form = OrderForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.is_anonymous:
                token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
                user = Token.objects.get(key=token).user
            basket_id = Basket.objects.get(user_id=user.id).id
            form = form.save()
            form.user_id = user
            form.save()
            for item in BasketItems.objects.filter(basket_id=basket_id):
                OrderItems(product=item.product, message=item.message, order_id=form.id).save()
                item.delete()
        flag = request.GET.get('format', '')  # url?format=json&name=John   {'format':'json', 'name':'John'}
        if flag == "json":
            return JsonResponse({"status": "success"})
        return redirect(f"/view_order/{form.id}")
    else:
        form = OrderForm
        return render(request, 'orderform.html', {'form': form})


# @login_required
@authentication_classes([SessionAuthentication, BaseAuthentication])
@permission_classes([IsAuthenticated])
def user_orders(request):
    orders = Order.objects.filter(user_id=request.user)
    completed_orders = CompletedOrder.objects.filter(user_id=request.user)
    return render(request, "user_orders.html", {"orders": orders, "comp_orders": completed_orders})


# @login_required
@authentication_classes([SessionAuthentication, BaseAuthentication])
@permission_classes([IsAuthenticated])
def user_view_order(request, order_id):
    order_products = OrderItems.objects.filter(order_id=order_id)
    products = []
    for o in order_products:
        p = Product.objects.get(id=o.product_id)
        p.message = o.message
        products.append(p)
    return render(request, "user_single_order.html", {"products": products, "order": order_id})


# @login_required
@authentication_classes([SessionAuthentication, BaseAuthentication])
@permission_classes([IsAuthenticated])
def user_view_complete_order(request, order_id):
    order_products = CompletedOrderItems.objects.filter(order_id=order_id)
    products = []
    for o in order_products:
        p = Product.objects.get(id=o.product_id)
        p.message = o.message
        products.append(p)
    return render(request, "user_single_order.html", {"products": products, "order": order_id})


@authentication_classes([SessionAuthentication, BaseAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def all_orders(request):
    orders = [o for o in Order.objects.all()]
    flag = request.GET.get('format', '')  # url?format=json&name=John   {'format':'json', 'name':'John'}
    if flag == "json":
        return HttpResponse(json.dumps({'orders': json.loads(core_serializers.serialize("json", orders))}),
                            content_type="application/json")
    return render(request, "all_orders.html", {"orders": orders})


@authentication_classes([SessionAuthentication, BaseAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def view_order(request, order_id):
    order_products = OrderItems.objects.filter(order_id=order_id)
    products = []
    for o in order_products:
        p = Product.objects.get(id=o.product_id)
        p.message = o.message
        products.append(p)
    return render(request, "single_order.html", {"products": products, "order": order_id})


@authentication_classes([SessionAuthentication, BaseAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
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


@authentication_classes([SessionAuthentication, BaseAuthentication])
@permission_classes([IsAuthenticated])
def api_view_order(request, order_id):
    order_products = OrderItems.objects.filter(order_id=order_id)
    products = json.loads(core_serializers.serialize("json", [Product.objects.get(id=o.product_id) for o in order_products]))
    for o, p in zip(order_products, products):
        p["message"] = o.message
    return HttpResponse(json.dumps({'products': products, "order": order_id}), content_type="application/json")
