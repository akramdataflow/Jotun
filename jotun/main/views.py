from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .models import Products, Category, Cart, CartItem, Order, OrderItem, Color
from .forms import SignupForm
import stripe
import json
import requests
import uuid
import hmac
import hashlib
from requests.auth import HTTPBasicAuth

# Stripe API Key
stripe.api_key = settings.STRIPE_SECRET_KEY


def payment_webhook(request):
    if request.method == 'POST':
        # التحقق من التوقيع
        secret_key = settings.PAYMENT_WEBHOOK_SECRET
        signature = request.headers.get('X-Signature')
        payload = request.body

        expected_signature = hmac.new(
            secret_key.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_signature, signature):
            return JsonResponse({"error": "Invalid signature"}, status=400)

        # معالجة البيانات
        try:
            data = json.loads(payload)
            event_type = data.get('event_type')
            payment_id = data.get('payment_id')

            if event_type == 'payment_success':
                # تحديث حالة الطلب
                return HttpResponse("Webhook received: Payment successful", status=200)
            elif event_type == 'payment_failed':
                # تحديث حالة الطلب
                return HttpResponse("Webhook received: Payment failed", status=200)
            else:
                return JsonResponse({"error": "Unknown event type"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)

# Utility Functions
def get_user_cart(user):
    """Utility function to get or create a cart for the user."""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

def add_to_cart(user, product_id, color='0001'):
    """Utility function to add a product to the user's cart."""
    product = get_object_or_404(Products, id=product_id)
    cart = get_user_cart(user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created or not cart_item.color:
        cart_item.color = color
    cart_item.save()
    return cart_item

def remove_from_cart(user, product_id):
    """Utility function to remove a product from the user's cart."""
    cart = get_user_cart(user)
    cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
    if cart_item:
        cart_item.delete()
    return cart

# Views
def main_view(request):
    """Home page view displaying all products."""
    products = Products.objects.all()
    context = {'products': products}
    return render(request, 'index.html', context)

def products(request):
    """View to display products, optionally filtered by category."""
    categories = Category.objects.all()
    selected_category = request.GET.get('category', None)
    
    if selected_category:
        category = get_object_or_404(Category, id=selected_category)
        products = Products.objects.filter(category=category)
    else:
        products = Products.objects.all()

    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'products.html', context)

def details(request, name):
    """View to display details of a specific product."""
    product = get_object_or_404(Products, name=name)
    context = {'product': product}
    return render(request, 'details.html', context)

@login_required
def card(request):
    """View to display the user's shopping cart."""
    categories = Category.objects.all()
    cart = get_user_cart(request.user)
    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)
    colors = Color.objects.all()

    context = {
        'categories': categories,
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
        'colors': colors,
    }
    return render(request, 'card.html', context)

@login_required
def add_to_cart_view(request, product_id):
    """View to add a product to the cart."""
    color = request.POST.get('color', '0001')  # Default color if not provided
    add_to_cart(request.user, product_id, color)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def increase_quantity(request, product_id):
    """View to increase the quantity of a product in the cart."""
    cart = get_user_cart(request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('card')

@login_required
def decrease_quantity(request, product_id):
    """View to decrease the quantity of a product in the cart."""
    cart = get_user_cart(request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('card')

@login_required
def remove_from_cart_view(request, product_id):
    """View to remove a product from the cart."""
    remove_from_cart(request.user, product_id)
    previous_url = request.META.get('HTTP_REFERER', 'home')
    return redirect(previous_url)

@login_required
def payment_page(request):
    """View to handle the payment process."""
    cart = get_user_cart(request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.quantity * item.product.price for item in cart_items)

    if request.method == 'POST':
        request_id = str(uuid.uuid4())
        username = settings.PAYMENT_GATEWAY_USERNAME
        password = settings.PAYMENT_GATEWAY_PASSWORD

        headers = {
            "Content-Type": "application/json",
            "X-Terminal-Id": settings.PAYMENT_GATEWAY_TERMINAL_ID
        }

        data = {
            "requestId": request_id,
            "amount": float(total_price),
            "currency": "IQD",
            "locale": "en_US",
            "finishPaymentUrl": "https://merchant.net/finish",
            "notificationUrl": "https://merchant.net/notification",
        }

        try:
            response = requests.post(
                "https://uat-sandbox-3ds-api.qi.iq/api/v1/payment", 
                headers=headers, 
                data=json.dumps(data),
                auth=HTTPBasicAuth(username, password)
            )
            response.raise_for_status()
            payment_data = response.json()
            return redirect(payment_data.get("formUrl"))
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": "Payment request failed", "details": str(e)}, status=500)

    return render(request, 'payment_page.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def success(request):
    """View to handle successful payment and create an order."""
    cart = get_user_cart(request.user)
    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)

    # Create an order
    order = Order.objects.create(
        user=request.user,
        total_price=total_price
    )
    
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.get_total_price(),
            color=item.color
        )
    
    # Clear the cart
    cart.items.all().delete()

    return redirect('home')

@login_required
def cancel(request):
    """View to handle payment cancellation."""
    return render(request, 'cancel.html')

def signup(request):
    """View to handle user registration."""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def contact(request):
    """View to display the contact page."""
    return render(request, 'contact.html')

def about(request):
    """View to display the about page."""
    return render(request, 'about.html')

def color(request):
    """View to display available colors."""
    colors = Color.objects.all()
    context = {'colors': colors}
    return render(request, 'color.html', context)

@login_required
def update_color(request, item_id):
    """View to update the color of a cart item."""
    if request.method == 'POST':
        new_color_value = request.POST.get('new_color')
        if new_color_value:
            cart_item = get_object_or_404(CartItem, id=item_id)
            cart_item.color = new_color_value
            cart_item.save()
            return redirect('cart')
    return redirect('cart')