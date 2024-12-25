from django.shortcuts import render, get_object_or_404
from .models import Products, Category
import stripe
from django.conf import settings
from django.shortcuts import redirect, render

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def main_view(request):
    products = Products.objects.all()
    context = {'products':products}
    return render(request,'index.html', context)

def products(request):
    categorys = Category.objects.all()
    context = {'categorys': categorys}
    return render(request, 'products.html', context)

def details(request,name):
    product = get_object_or_404(Products, name=name)
    context = {'product':product}
    return render(request,'details.html', context)



# عرض صفحة الدفع
def payment_page(request):
    if request.method == "POST":
        # إنشاء جلسة دفع
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],  # دعم الدفع بالبطاقات
            line_items=[{
                "price_data": {
                    "currency": "usd",  # العملة
                    "product_data": {
                        "name": "Your Product Name",  # اسم المنتج
                    },
                    "unit_amount": 5000,  # السعر بالسنتات (50 دولار = 5000 سنت)
                },
                "quantity": 1,  # الكمية
            }],
            mode="payment",
            success_url="http://127.0.0.1:8000/success/",  # رابط النجاح
            cancel_url="http://127.0.0.1:8000/cancel/",    # رابط الإلغاء
        )
        return redirect(session.url)  # إعادة التوجيه إلى صفحة الدفع الجاهزة
    return render(request, "payment.html")


def success(request):
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html')