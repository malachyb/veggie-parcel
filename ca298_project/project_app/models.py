from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)


class ProductCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    picture = models.FileField(upload_to='product_images/', blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_created = models.DateField(auto_now_add=True, null=True)
    shipping_addr = models.CharField(max_length=200, null=True)
    credit_card_number = models.IntegerField(max_length=16)
    ccv = models.IntegerField(max_length=3)
    expiry_date = models.CharField(max_length=7)


class OrderItems(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Basket(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)


class BasketItems(models.Model):
    id = models.AutoField(primary_key=True)
    basket_id = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)


class CompletedOrder(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_created = models.DateField(auto_now_add=True, null=True)
    shipping_addr = models.CharField(max_length=200, null=True)


class CompletedOrderItems(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    order = models.ForeignKey(CompletedOrder, on_delete=models.CASCADE)
