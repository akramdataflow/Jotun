from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField


# Create your models here.

def image_upload(instance, filename):
    imagename, extension = filename.split('.')
    return "product/%s.%s" % (instance.id, extension)

class Category(models.Model):
    title = models.CharField(max_length=3000)

    def __str__(self):
        return self.title

class Products(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=image_upload)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    color = ColorField(default='#FFFFFF')

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"

    def get_total_price(self):
        return self.quantity * self.product.price