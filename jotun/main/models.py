from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField
import csv


# Create your models here.

class Color(models.Model):
    name = models.CharField(max_length=100)  # Color name (e.g., "Red")
    number = models.CharField(max_length=100)  # Color number, can be used for a color code
    hex_value = models.CharField(max_length=10)  # Hex value of the color (e.g., "#FF0000" for red)

    @staticmethod
    def import_colors_from_csv(csv_file_path):
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                color, created = Color.objects.get_or_create(
                    number=row['Colour Number'],
                    name=row['Colour Name'],
                    hex_value=row['Hex']
                )
                if created:
                    print(f"تم إضافة اللون: {row['Colour Name']} ({row['Colour Number']})")
                else:
                    print(f"اللون {row['Colour Name']} موجود بالفعل.")

    def __str__(self):
        return f"{self.name} - {self.number} - {self.hex_value}"

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
    color = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"

    def get_total_price(self):
        return self.quantity * self.product.price
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    color = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for {self.order.user.username}"
    
    