from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)


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
