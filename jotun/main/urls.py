from django.urls import path
from . import views


urlpatterns = [
    path('',views.main_view, name='home'),
    path('products',views.products, name='products'),
    path('products/<str:name>/',views.details, name='details'),
    path('payment/', views.payment_page, name='payment_page'),  # صفحة الدفع
    path('success/', views.success, name='success'),  # صفحة النجاح
    path('cancel/', views.cancel, name='cancel'), 
    path('card/', views.card, name='card'), 
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]

