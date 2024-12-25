from django.shortcuts import render, get_object_or_404
from .models import *
import stripe
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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



def card(request):

    # جلب جميع التصنيفات
    categorys = Category.objects.all()

    # جلب أو إنشاء عربة التسوق للمستخدم
    cart, created = Cart.objects.get_or_create(user=request.user)

    # جلب العناصر المرتبطة بالعربة
    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)

    context = {
        'categorys': categorys,
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'card.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # تحقق إذا كان المنتج موجودًا في السلة
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        # زيادة الكمية إذا كان المنتج موجودًا مسبقًا
        cart_item.quantity += 1
        cart_item.save()

    return redirect('card')  # توجيه المستخدم إلى صفحة السلة





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