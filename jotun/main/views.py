from django.shortcuts import render, get_object_or_404
from .models import Products, Category
# Create your views here.
def main_view(request):
    products = Products.objects.all()
    context = {'products':products}
    return render(request,'index.html', context)

def products(request):
    categorys = Category.objects.all()
    context = {'categorys': categorys}
    return render(request, 'products.html', context)

def details(request,id):
    product = get_object_or_404(Products, id=id)
    context = {'product':product}
    return render(request,'details.html', context)  