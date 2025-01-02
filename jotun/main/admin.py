from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Products)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Color)
admin.site.register(OrderItem)