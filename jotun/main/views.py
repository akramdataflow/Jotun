from django.shortcuts import render, get_object_or_404
from .models import *
import stripe
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
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

    # إعادة المستخدم إلى الصفحة السابقة
    previous_url = request.META.get('HTTP_REFERER', 'home')
    return redirect(previous_url)

@login_required
def increase_quantity(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    # زيادة العدد بمقدار 1
    cart_item.quantity += 1
    cart_item.save()

    return redirect('card')  # توجيه المستخدم إلى صفحة السلة

@login_required
def decrease_quantity(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    if cart_item.quantity > 1:
        # تقليل العدد بمقدار 1
        cart_item.quantity -= 1
        cart_item.save()
    else:
        # إذا كان العدد 1، احذف العنصر من السلة
        cart_item.delete()

    return redirect('card')  # توجيه المستخدم إلى صفحة السلة

@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.filter(user=request.user).first()
    
    if cart:
        # حاول الحصول على العنصر من السلة
        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if cart_item:
            cart_item.delete()  # حذف العنصر

    # إعادة المستخدم إلى الصفحة السابقة
    previous_url = request.META.get('HTTP_REFERER', 'home')
    return redirect(previous_url)




@login_required
def payment_page(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)

    if request.method == "POST":
        # تحويل المبلغ إلى سنتات
        total_price_cents = int(total_price * 100)

        # إنشاء جلسة دفع
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],  # دعم الدفع بالبطاقات
            line_items=[{
                "price_data": {
                    "currency": "usd",  # العملة
                    "product_data": {
                        "name": "Cart Payment",  # اسم المنتج
                    },
                    "unit_amount": total_price_cents,  # المجموع بالسنتات
                },
                "quantity": 1,  # الكمية
            }],
            mode="payment",
            success_url="http://127.0.0.1:8000/success/",  # رابط النجاح
            cancel_url="http://127.0.0.1:8000/cancel/",    # رابط الإلغاء
        )
        return redirect(session.url)  # إعادة التوجيه إلى صفحة الدفع الجاهزة

    return render(request, 'payment_page.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def success(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)

    # حفظ تفاصيل الطلب
    order = Order.objects.create(
        user=request.user,
        total_price=total_price
    )
    
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.get_total_price()
        )
    
    # تنظيف السلة
    cart.items.all().delete()

    return render(request, 'index.html', {'order': order})

@login_required
def cancel(request):
    return render(request, 'cancel.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # تشفير كلمة المرور
            user.save()
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def color(request):
    colores = Color.objects.all()
    context = {'colores':colores}
    return render(request, 'color.html', context)


