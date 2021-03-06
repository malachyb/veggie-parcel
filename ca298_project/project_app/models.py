from django.db import models
from django.contrib.auth.models import AbstractUser


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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def price(self):
        return self.product.price * self.quantity


class Vegetable(models.Model):
    id = models.AutoField(primary_key=True)
    veg_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
